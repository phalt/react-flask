# 📄 Features

## Built on great tools

Beckett bundles a [Flask web server](https://flask.palletsprojects.com/en/2.3.x/) and a [React](https://react.dev/) [TypeScript](https://www.typescriptlang.org/) frontend into one framework.

TypeScript and Python are two of the [most used programming languages in the world](https://www.statista.com/statistics/793628/worldwide-developer-survey-most-used-languages/), and so are often used together in projects.
Despite this; getting them set up to work together nicely is tedious and time consuming, and often a poor developer experience.

Beckett solves this problem by strongly-linking them together as one framework.

## ...and you can continue to use them

Beckett doesn't expect you to use Python to control the frontend, when React TypeScript offers a better solution, and vice versa.

You still write Flask views like a normal flask app, and you can install and use any other Python library that works nicely with Flask.

You still write React TypeScript like any other React application, and you can `yarn add` any JS library you like to meet the needs of your project.

## Strongly-linked types

When we built Beckett we decided that if we're going to bundle the languages together, why not link them strongly and find extra benefits?

The first major feature we built was strongly-linked types.

Beckett takes your [Python Typehints](https://docs.python.org/3/library/typing.html) and auto-generates [TypeScript interfaces](https://www.typescriptlang.org/docs/handbook/interfaces.html) to maintain type integrity across both languages. It does this automatically for any API endpoints in the Flask web server using the Beckett decorators.

```py title="src/views/people.py" linenums="1"
import attrs
from src.app import app
from src.beckett.blueprint import BeckettBlueprint
from src.beckett.types import APIResponse

blueprint = BeckettBlueprint("people", __name__, url_prefix="/people")

@attrs.define
class GetPeopleResponse(APIResponse):
    name: str

@blueprint.api_get("/get")
def get_people() -> GetPeopleResponse:
    """
    This is an example API GET route.
    """
    return GetPeopleResponse(name="Paul")

app.register_blueprint(blueprint)
```

When the Beckett flask server is running, this will autogenerate the following TypeScript interface:

```ts title="js/api/types.ts" linenums="1"
/*
THIS FILE IS AUTO-GENERATED, DO NOT ALTER MANUALLY.
*/

// prettier-ignore
export interface PeopleGetPeopleResponse {
    "__type__": string
    "__http_status_code__": number
    "name": string
}

...
```

Beckett automatically adds additional parameters to any `APIResponse` object it such as `__type__` and `__http_status_code__`. Beckett's TypeScript API Client uses these fields to introspect the API response and handle errors gracefully for you.

Under the hood, we use [attrs](https://www.attrs.org/en/stable/examples.html) and [cattrs](https://github.com/python-attrs/cattrs) to take the types in the classes we define and transform them into their TypeScript equivalents.

## React pages

Beckett will auto-generate any new React page when you register a new Beckett page in the Flask service, when you are in development mode. Beckett's is built such that a Flask _route_ (defined through the URL of a Flask view function) can be linked directly to a React _page_ on the frontend.

```py title="src/views/people.py" linenums="1"

import attrs

from src.app import app
from src.beckett.blueprint import BeckettBlueprint
from src.beckett.renderer.typescript_react.renderer import beckett_page

blueprint = BeckettBlueprint("people", __name__, url_prefix="/people")

# Hiding other endpoints for clarity
...

@attrs.define
class ExamplePageProps:
    hello: str

@blueprint.route("/")
@beckett_page()
def example_page() -> ExamplePageProps:
    return ExamplePageProps(hello="world")

app.register_blueprint(blueprint)
```

When the Beckett Flask server is running in development mode it will recognise a new endpoint has been registered, and it makes a new React page linked to the Flask view.
This is all handled by applying the `@beckett_page()` decorator.

The generated page will start something like this:

```ts linenums="1" title="src/js/template/people/example_page.tsx"
import React from 'react'
import PageProps from './example_page.type'
import {Container, Row} from 'react-bootstrap'

const Page: React.FunctionComponent<PageProps> = (props) => {
    return (
        <Container>
            <Row className="mb-4 border-bottom">
                <h1>Hello, React!</h1>
                <p>
                    here are my props: <code>{props}</code>
                </p>
            </Row>
        </Container>
    )
}

export default Page
```

The template can be customised by setting the `BECKETT_REACT_PAGE_TEMPLATE` environment variable to a path.

Once this has been generated you are free to go and develop the frontend using any React library you want.

## Props for React pages

As well as the base page, `beckett_page` also generates a `PageProps` interface. The response returned by the Flask view are injected as props into this page for you automatically.
The generated file for the example above looks something like this:

```ts linenums="1" title="src/js/template/people/example_page.type.ts"
// This file is generated by @beckett_page

// prettier-ignore
export default interface PageProps {
    "hello": string
}

```

This file will update automatically as you make changes to the Flask view response class and the server is in development mode.

## API Client

TODO

## Refresh API queries

TODO

## Run it all together at once

Instead of maintaining multiple terminals running two different servers, Beckett provides a single development command to run both the Flask service and React server in development mode.
Both are these run in "hot reload" - any code changes will restart each server so changes happen immediately.

```sh
make dev
```
