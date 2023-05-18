import {GET_MAP, POST_MAP} from './types'
import {BaseDataContext, jsonReviver, jsonReplacer} from '~/beckett_page'
import {useMutation, useQuery, useQueryClient} from 'react-query'
import {useContext} from 'react'

export class APIError extends Error {
    status: number
    statusText: string
    constructor(response: Response) {
        super(`http_status=${response.status} fetching ${response.url}`)
        this.status = response.status
        this.statusText = response.statusText
    }
}

const processRequest = async (request: Request, options?: Partial<RequestInit>) => {
    const headers = new Headers()
    for (const [key, value] of request.headers.entries()) {
        headers.append(key, value)
    }

    const response = await fetch(request, {
        credentials: 'same-origin',
        headers,
        ...options,
    })
    if (!response.ok) {
        throw new APIError(response)
    }
    const text = await response.text()
    const json = JSON.parse(text, jsonReviver)

    return json
}

export async function get<T extends keyof GET_MAP>(
    _endpoint: T,
    path: string,
    ...args: GET_MAP[T]['request'] extends undefined ? [] : [GET_MAP[T]['request']]
): Promise<GET_MAP[T]['response']> {
    const url = new URL(path, window.location.href)

    const params = args[0] as {[k: string]: any} | undefined
    if (params) {
        Object.keys(params).forEach(k => {
            if (typeof params[k] === 'boolean') {
                url.searchParams.append(k, params[k] ? 'true' : '')
            } else {
                url.searchParams.append(k, String(jsonReplacer(undefined, params[k])))
            }
        })
    }

    return processRequest(
        new Request(String(url), {
            method: 'GET',
        }),
    )
}

const csrfToken = document.querySelector('html')?.dataset.csrfToken!

export async function post<T extends keyof POST_MAP>(
    _endpoint: T,
    path: string,
    body: POST_MAP[T]['request'],
): Promise<POST_MAP[T]['response']> {
    const url = new URL(path, window.location.href)

    return processRequest(
        new Request(String(url), {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRF-Token': csrfToken,
            },
            body: JSON.stringify(body, jsonReplacer),
        }),
    )
}

function generateQueryKey<T extends keyof GET_MAP>(endpoint: T, params: GET_MAP[T]['request']) {
    const queryKey: unknown[] = [endpoint]
    for (const key in params) {
        queryKey.push(jsonReplacer(undefined, (params as unknown as any)[key]))
    }
    return queryKey
}

export function useGet<T extends keyof GET_MAP>(
    endpoint: T,
    ...args: GET_MAP[T]['request'] extends undefined ? [] : [GET_MAP[T]['request']]
) {
    const {urlMap} = useContext(BaseDataContext)
    const url = urlMap[endpoint]

    const queryKey = generateQueryKey(endpoint, args[0])

    const result = useQuery({
        queryKey,
        queryFn: () => get(endpoint, url, ...args),
        suspense: true,
    })

    // Because we're using suspense data should always be set from the hook
    // user's perspective, this little dance makes it appear that way to the
    // caller.
    return {
        ...result,
        data: result.data! as GET_MAP[T]['response'],
    }
}

export function useInvalidate() {
    const queryClient = useQueryClient()

    return <T extends keyof GET_MAP>(
        endpoint: T,
        ...args: GET_MAP[T]['request'] extends undefined ? [] : [GET_MAP[T]['request']]
    ) => {
        queryClient.invalidateQueries(generateQueryKey(endpoint, args[0]))
    }
}

export function usePost<T extends keyof POST_MAP>(endpoint: T) {
    const {urlMap} = useContext(BaseDataContext)
    const url = urlMap[endpoint]

    const result = useMutation<POST_MAP[T]['response'], unknown, POST_MAP[T]['request'], unknown>(data =>
        post(endpoint, url, data),
    )

    return result
}
