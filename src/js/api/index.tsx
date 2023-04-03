import React from 'react'
import type {QueryObserverResult} from 'react-query'
import Alert from 'react-bootstrap/Alert'
import {Loading} from '~/components/loading'
import {csrfToken} from '~/components/csrf'
import {useGet} from '~/api/query'
import {GET_MAP} from '~/api/types'

/*
Common headers you'll probably need
*/
export const csrfHeader = ['X-CSRFToken', csrfToken]
export const jsonContentTypeHeader = ['Content-Type', 'application/json']

export type SuccessProps = {
    data: any
}

export type ErrorProps = {
    error: unknown
}

type APIQueryProps<T extends keyof GET_MAP> = {
    path: T
    args: GET_MAP[T]['request'] extends undefined ? [] : [GET_MAP[T]['request']]
    SuccessState: React.FunctionComponent<SuccessProps>
    LoadingState: React.FunctionComponent
    ErrorState: React.FunctionComponent<ErrorProps>
}

/*
    A React component that makes an API Query and handles loading/error states for you
    - path: the absolute path for the API query you want to make.
    - SuccessState: the components to render when the query is finished. Receives API response data.
    - LoadingState: the component to show when the API query is loading.
    - ErrorState: the component to show when the API query fails or a wrong HTTP status code is received. Receives error.
*/
export const APIQuery = <T extends keyof GET_MAP>({
    SuccessState,
    LoadingState,
    ErrorState,
    path,
    args,
}: APIQueryProps<T>) => {
    const {isLoading, error, data, isFetching} = useGet(path, ...args)

    if (isLoading || isFetching) {
        return <LoadingState />
    }
    if (error) {
        return <ErrorState error={error} />
    }
    if (data) {
        return <SuccessState data={data} />
    }
    return null
}

type APIQueryRenderProps = {
    useQuery: QueryObserverResult<any, unknown>
    SuccessState: React.FunctionComponent
    LoadingState?: React.FunctionComponent
    ErrorState?: React.FunctionComponent
    errorMessage?: string
}

export const APIQueryRender: React.FunctionComponent<APIQueryRenderProps> = props => {
    const {useQuery, SuccessState} = props
    let {LoadingState, ErrorState, errorMessage} = props

    if (useQuery.isLoading || useQuery.isFetching) {
        if (!LoadingState) {
            LoadingState = () => <Loading center />
        }
        return <LoadingState />
    }
    if (useQuery.error) {
        if (!ErrorState) {
            if (!errorMessage) {
                errorMessage = 'API call failed'
            }

            ErrorState = () => {
                return (
                    <Alert variant="danger" className="text-center">
                        {errorMessage}
                    </Alert>
                )
            }
        }
        return <ErrorState />
    }
    if (useQuery.isSuccess) {
        return <SuccessState />
    }
    return null
}
