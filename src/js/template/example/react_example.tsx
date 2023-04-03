import React from 'react'
import PageProps from './react_example.type'
import {Container, Row} from 'react-bootstrap'
import {useGet} from '~/api/query'

const Page: React.FunctionComponent<PageProps> = ({good}) => {
    const getResponse = useGet('example.get_example')
    return (
        <Container>
            <Row className="mb-4 border-bottom">
                <p>Hello, React!</p>
                <p>
                    I was fed the following props from the Flask view: <code>good: {good}</code>
                </p>
                <p>
                    Here is the API result from an API call from this page (to a Flask view wrapped with
                    @api_get_route): {getResponse.data.__type__}
                </p>
            </Row>
        </Container>
    )
}

export default Page
