import React from 'react'
// Note: you'll need to update this path!
import PageProps from './test_page.type'
import {Container, Row} from 'react-bootstrap'

const Page: React.FunctionComponent<PageProps> = props => {
    return (
        <Container>
            <Row className="mb-4 border-bottom">
                <h1>Hello, React!</h1>
                <p>
                    Hello: <code>{props.good}</code>
                </p>
            </Row>
        </Container>
    )
}

export default Page
