import React from 'react'
import PageProps from './react_example.type'
import {Container, Row} from 'react-bootstrap'

const Page: React.FunctionComponent<PageProps> = () => {
    return (
        <Container>
            <Row className="mb-4 border-bottom">
                <p>Hello, React-admin!</p>
                <p>
                    Make sure you update the <code>PageProps</code> import path to be correct.
                </p>
                <p>You can also rename this React function if it helps with better organisation.</p>
            </Row>
        </Container>
    )
}

export default Page
