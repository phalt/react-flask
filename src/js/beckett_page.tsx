import React from 'react'
import {createRoot} from 'react-dom/client'
import {QueryClient, QueryClientProvider} from 'react-query'
import {Loading} from './components/loading'

declare module 'react' {
    export function useTransition(): [boolean, (callback: () => void) => void]
}

export const jsonReviver = (_key: unknown, value: unknown) => {
    if (value instanceof Object) {
        if ('$decimal' in value && typeof value['$decimal'] === 'string') {
            return value['$decimal']
        }
    }
    return value
}

export function jsonReplacer(this: any, key: unknown, value: unknown) {
    const rawValue: unknown = this instanceof Object && typeof key === 'string' ? this[key] : value
    return rawValue
}

const queryClient = new QueryClient({
    defaultOptions: {
        queries: {
            refetchOnWindowFocus: false,
            retry: false,
        },
    },
})

interface BaseData {
    urlMap: {[endpoint: string]: string}
}

export const BaseDataContext = React.createContext<BaseData>({
    urlMap: {},
})

class ErrorBoundary extends React.Component<{}, {error?: Error; componentStack?: string}> {
    constructor(props: {}) {
        super(props)
        this.state = {}
    }

    static getDerivedStateFromError(error: Error) {
        return {error}
    }

    componentDidCatch(error: Error, {componentStack}: React.ErrorInfo) {
        // You can also log the error to an error reporting service
        this.setState({componentStack})
        console.error({error, componentStack})
    }

    render() {
        const {error, componentStack} = this.state

        if (error) {
            // You can render any custom fallback UI
            return (
                <>
                    <h1>Something went wrong.</h1>
                    <pre>{`${error}`}</pre>
                    <hr />
                    <pre>{componentStack}</pre>
                </>
            )
        }

        return this.props.children
    }
}

export function renderReactPage<P>(Component: React.FunctionComponent<P>, jsonProps: string, baseData: BaseData) {
    const props = JSON.parse(jsonProps, jsonReviver)

    return createRoot(document.getElementById('render-react-root')!).render(
        <BaseDataContext.Provider value={baseData}>
            <QueryClientProvider client={queryClient}>
                <ErrorBoundary>
                    <React.Suspense fallback={<Loading />}>
                        <Component {...props} />
                    </React.Suspense>
                </ErrorBoundary>
            </QueryClientProvider>
        </BaseDataContext.Provider>,
    )
}
