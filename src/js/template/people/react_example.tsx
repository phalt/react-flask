import React from 'react'
import PageProps from './react_example.type'
import {Container, Row} from 'react-bootstrap'

const Page: React.FunctionComponent<PageProps> = props => {
    return (
        <Container>
            <Row className="mb-4 border-bottom">
                <h1>Hello, React!</h1>
                <p>
                    Here are your props:{' '}
                    <code>
                        {Object.keys(props).map(p => (
                            <p>
                                {p} : {props[p]}
                            </p>
                        ))}
                    </code>
                </p>
            </Row>
        </Container>
    )
}

export default Page
