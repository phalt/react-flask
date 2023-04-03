import React from 'react'
import Spinner from 'react-bootstrap/Spinner'

export type LoadingProps = {
    center?: boolean
    variant?: string
}

/*
Opinionated loading spinner. It always looks the same.

If you want a different spinner, use the Spinner component directly.

If you need this centred, use it like this:

    <Loading center />
 */
export const Loading: React.FunctionComponent<LoadingProps> = ({center, variant}) => {
    const spinner = <Spinner animation="border" variant={variant ? variant : 'primary'} />

    if (center) {
        return <div className="text-center">{spinner}</div>
    }

    return spinner
}
