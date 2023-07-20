# 📝 Tutorial

## Early days

Before this becomes a fully fledged package, this project exists as a template you can fork and build from. My advice for getting started is to build ontop of what already exists, and use the existing routes until you understand it, then you can delete it!

!!! note

    This example will work you through making a simple Bookshop app and API.

## Add your first view

In `src.views` add a new file called `books.py` and add the following code:

```py title="src/views/books.py" linenums="1"
from src.app import app
from src.beckett.blueprint import BeckettBlueprint

beckett = BeckettBlueprint("books", __name__, url_prefix="/books")

@beckett.route("/")
def home():
    return dict(title="My books")

app.register_blueprint(beckett)
```

Then in `src.views.__init__` we just need to do a small update as seen on line 2:

```py title="src/views/__init__.py" hl_lines="2" linenums="1"
from src.views import people, index  # noqa
from .books import *
```

This small import will let the Flask/BeckettApp know to include your views file in the application.

At this point you can now visit [http://localhost:9000/books/](http://localhost:9000/books/) to see a simple API response.

## Turn it into a React page

Let's make this simple API response become something far more interesting - a whole react page!

We only need to make a few changes:

```py title="src/views/books.py" linenums="1" hl_lines="3 8 9 10 11 13 14 15"
from src.app import app
from src.beckett.blueprint import BeckettBlueprint
from src.beckett.types import PageProps

beckett = BeckettBlueprint("books", __name__, url_prefix="/books")


class HomePageProps(PageProps):
    title: str


@beckett.route("/")
@beckett.page()
def home() -> HomePageProps:
    return HomePageProps(title="My books")


app.register_blueprint(beckett)
```

Quite a few interesting things should happen when you save the file - you'll see two brand new files appear in the `src/js/templates` directory.
I know you want to inspect them and see what has changed, but for now let us go over the changes in the `books.py` file first:

```py
from src.beckett.types import PageProps
```

The `PageProps` baseclass should be used for all React pages.

```py
class HomePageProps(PageProps):
    title: str
```

This is the response type of your React page, and will be transformed into an equivalent Typescript interface. You can inspect the sibling interface now in `src/js/template/books/home.type.ts`:

```ts
export default interface PageProps {
    "title": string
}
```

Notice how the name of the interface has changed? This is because each React page in Beckett only has one set of initial props for a page load, and this naming convention helps to pick it out.

```py
@beckett.page()
def home() -> HomePageProps:
    return HomePageProps(title="My books")
```

Here you will see we have updated the Flask view function with a return type, our `HomePageProps`, that we wrote earlier.

We have also updated the return line to return an instance of that class.

The one line of code that makes this all magically generate the files is `beckett.page()`. This decorator inspects all the associated pages when the server is in development mode, and if it can't find a related TypeScript file for it, it will generate it for you. 

Here are the files it has generated for us:

* `src/js/template/books/home.tsx`
* `src/js/template/books.home.type.ts`

Notice how Beckett has intelligently figured out the directory and the file name from the name of the python file and the view function.

!!! note

    Sometimes when a new file is generated you need to run `make web` again for the page to load - this is only a problem the first time and we're working to fix that bug.

If you refresh your browser at [http://localhost:9000/books/](http://localhost:9000/books/) you should see a react page with the default template information from `src/js/template/books/home.tsx`.

## Add an API view

React is most useful when we can make concurrent API requests to our application server and return content.

Beckett manages API views that we can be used in our React pages. Let's make one now.

Add this just the `home` view function:

```py title="src/views/books.py" linenums="17"
from src.beckett.types import APIResponse

class BookResponse(APIResponse):
    name: str
    author: str


@beckett.api_get("/details")
def details() -> BookResponse:
    return BookResponse(name="Gideon the Ninth", author="Tamsyn Muir.")


```
Hit save and you should see some files change again (that happens a lot with Beckett). Let's go over this change quickly.

```py
from src.beckett.types import APIResponse
```

All of Beckett's API Views must return a subclass of `APIResponse`. There are a few generic helpers in `src.beckett.types` too if you want to return common responses like `Forbidden` or `NotFound`.

```py
class BookResponse(APIResponse):
    name: str
    author: str
```

The `BookResponse` is the response class we're using for our API. You'll see in `src/js/api/types.ts` that this gets transformed into a TypeScript interface:

```ts title="src/js/api/types.ts" linenums="6"
export interface BooksDetailsResponse {
    "status_code": number
    "name": string
    "author": string
}
```

This all happens because of the decorator function `beckett.api_get`:

```py
@beckett.api_get("/details")
def details() -> BookResponse:
    return BookResponse(name="Gideon the Ninth", author="Tamsyn Muir.")
```

Similar to `beckett.api` - this decorator will inspect the view functions when in development mode, and generate appropriate TypeScript interfaces for you.

This interface is available in our TypeScript code now, but we don't acutally need to plug it into our APIClient, because Beckett has done that already for us! 

Have a look further down the `types.ts` file:

```ts title="src/js/api/types.ts" linenums="32" hl_lines="2 3"
export interface GET_MAP {
    // beckett_framework/src/views/books.py
    "books.details": {request: undefined, response: BooksDetailsResponse}
    // beckett_framework/src/views/people.py
    "people.get_people": {request: undefined, response: PeopleGetPeopleResponse}
}
```

The `GET_MAP` has updated to include the request (currently none) and response types for this API endpoint. So how do we use it?

## Using the API Client

Let's write some typescript shall we?

Open up `src/js/template/books/home.tsx` and make these changes:

```ts title="src/js/template/books/home.tsx" linenums="1" hl_lines="4 7 22-27"
import React from 'react'
import PageProps from './home.type'
import {Container, Row} from 'react-bootstrap'
import { useGet } from '~/api/query'

const Page: React.FunctionComponent<PageProps> = props => {
    const {data} = useGet("books.details")
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
                <p>
                    Book name: {data.name}
                </p>
                <p>
                    Book author: {data.author}
                </p>
            </Row>
        </Container>
    )
}

export default Page
```

Let's go over these changes so they make sense.

```ts
import { useGet } from '~/api/query'
```

`useGet` is a [React Hook](https://react.dev/reference/react) that provides access to all the registered API views in our Beckett application.

It uses the `GET_MAP` to make sure the request and responses remain consistent.

```ts
const {data} = useGet("books.details")
```

We do not need to provide any inputs to the `useGet` function except for the API view we want to call - in this case it will always be the `file_name.view_function` pattern. In fact, if you typed the example out letter by letter you would've noticed that it provided autocomplete!

Because Beckett's React pages use [React suspense](https://react.dev/reference/react/Suspense) - it gracefully handles the loading state for you. This means that the page will not render until the API call has returned a response.

```ts
<p>
    Book name: {data.name}
</p>
<p>
    Book author: {data.author}
</p>
```

Because we don't need to worry about the loading state, we can safely apply the values from the API call into our React page.

## APIs with input parameters

Let's grow our API functionality even more by making it require an input value. We'll update the API View first:


```py title="src/views/books.py" linenums="23" hl_lines="2 3"
@beckett.api_get("/details")
def details(name: str) -> BookResponse:
    return BookResponse(name=name, author="Tamsyn Muir.")
```

The only thing we've changed here is we've added an input parameter `name`, which is a `str`, and then returned it in our API Response. This is just a simple demonstrative example, but you could imagine making database queries or doing some complex maths here - it's just Python after all!

When you save this, you'll notice a new TypeScript interface will be generated in `src/js/api/types.ts`:

```ts title="src/js/api/types.ts" linenums="8"
export interface BooksDetailsRequest {
    "name": string
}
```

This new request interface will be mapped to the `GET_MAP` in the same file:

```ts title="src/js/api/types.ts" linenums="37" hl_lines="3"
export interface GET_MAP {
    // beckett_framework/src/views/books.py
    "books.details": {request: BooksDetailsRequest, response: BooksDetailsResponse}
    // beckett_framework/src/views/people.py
    "people.get_people": {request: undefined, response: PeopleGetPeopleResponse}
}
```

In fact, if you try and refresh the browser at [http://localhost:9000/books/](http://localhost:9000/books/) you'll see this take affect immediately - the page will crash! This is because the `name` value in the request is a required parameter.

Let's update our React app so we can send input data to our API Client.

```ts title="src/js/template/books/home.tsx" linenums="1" hl_lines="7"
import React from 'react'
import PageProps from './home.type'
import {Container, Row} from 'react-bootstrap'
import { useGet } from '~/api/query'

const Page: React.FunctionComponent<PageProps> = props => {
    const {data} = useGet("books.details", {name: "My book"})
    ...
```

For the sake of brevity we've removed a bunch of this code in the tutorial. The only change needed is to pass an object with the required parameters to the API and then the page should load fine. You'll notice as you type of the object it will give you hints as to the expected input parameters.

Magic, eh?

## API Post requests

Now that we've built an API that accepts data and returns it, let's build something more functional. How about an HTTP POST API View?

What's the difference between a POST view and a GET view in Beckett?

* HTTP GET views format the input parameters as query parameters and are great for loading content quickly.
* HTTP POST views receive their inputs as JSON in the HTTP Body and accept much more content.
* HTTP POST views are preferred when we want to make state changes to our application.

First things first, let's add a new View to our API:


```py title="src/views/books.py" linenums="28"
class BookUpdateResponse(APIResponse):
    name: str
    author: str


@beckett.api_post("/add")
def add(name: str, author: str) -> BookUpdateResponse:
    # Imagine database persistence happens here
    return BookUpdateResponse(name=name, author=author)
```

This should all be looking very familiar now. The one small difference from the previous API is we are using `beckett.api_post` instead of `beckett.api_get`.

Just like before, this will have generated two new interfaces for us:

```ts title="src/js/api/types.ts" linenums="8"

export interface BooksAddRequest {
    "name": string
    "author": string
}

export interface BooksAddResponse {
    "status_code": number
    "name": string
    "author": string
}
```

You will also see the `POST_MAP` will have been updated:

```ts title="src/js/api/types.ts" linenums="58" hl_lines="2 3"
export interface POST_MAP {
    // beckett_framework/src/views/books.py
    "books.add": {request: BooksAddRequest, response: BooksAddResponse}
    // beckett_framework/src/views/people.py
    "people.post_example": {request: PeoplePostExampleRequest, response: PeoplePostExampleResponse}
}
```

Similar to the `GET_MAP`, the `POST_MAP` allows us to manage the API Client nicely.

Let's add a form that uses this API to our `home.tsx` file:

```ts title="src/js/template/books/home.tsx" linenums="1" hl_lines="4 8-15 33-62"
import React, {useState} from 'react'
import PageProps from './home.type'
import {Container, Row} from 'react-bootstrap'
import {useGet, usePost} from '~/api/query'

const Page: React.FunctionComponent<PageProps> = props => {
    const {data} = useGet('books.details', {name: 'My book'})
    const addBook = usePost('books.add')
    interface Book {
        name: string
        author: string
    }
    const [allBooks, setAllBooks] = useState<Book[]>([{name: 'First book', author: 'No one'}])
    const [formName, setName] = useState<string>('')
    const [formAuthor, setAuthor] = useState<string>('')
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
                <p>Book name: {data.name}</p>
                <p>Book author: {data.author}</p>
            </Row>
            <Row>
                <h1>Add book</h1>
                <p>
                    Name: <input value={formName} onChange={v => setName(v.target.value)} />
                </p>
                <p>
                    Author: <input value={formAuthor} onChange={v => setAuthor(v.target.value)} />
                </p>
                <button
                    onClick={() =>
                        addBook.mutate(
                            {name: formName, author: formAuthor},
                            {
                                onSuccess: response => {
                                    allBooks?.push({name: response.name, author: response.author})
                                    setAllBooks(Array.from(allBooks))
                                },
                                onError: () => console.log(addBook.error),
                            },
                        )
                    }
                >
                    Add
                </button>
            </Row>
            <Row>
                <ul>
                {allBooks.map(book => <li>{book.name} by {book.author}</li>)}
                </ul>
            </Row>
        </Container>
    )
}

export default Page

```

I appreciate that quite a lot of lines have been added here. This may look a bit intimdating if you're not used to React but don't worry it'll all make sense.

Let's break down each section bit by bit.

```ts
const addBook = usePost('books.add')
```

The `usePost` hook behaves very differently to the `useGet` hook. This is because we often want to trigger to hook after a state change or button press.

Under the hood, the `usePost` hook provides a [TanStack Query](https://tanstack.com/query/latest) hook for managing the API request.

```ts
interface Book {
    name: string
    author: string
}
const [allBooks, setAllBooks] = useState<Book[]>([{name: 'First book', author: 'No one'}])
const [formName, setName] = useState<string>('')
const [formAuthor, setAuthor] = useState<string>('')
```

This code sets ups some state using React's state library. We'll use it for the form and the list on the page.

```ts
<button
    onClick={() =>
        addBook.mutate(
            {name: formName, author: formAuthor},
            {
                onSuccess: response => {
                    allBooks?.push({name: response.name, author: response.author})
                    setAllBooks(Array.from(allBooks))
                },
                onError: () => console.log(addBook.error),
            },
        )
    }
>
    Add
</button>
```

The `button` logic is the most interesting part of this change - it is where we trigger our POST API request!

The [mutate](https://tanstack.com/query/v4/docs/react/guides/mutations#promises) method is the standard TanStack one, but Beckett forces the input data to match the `BookAddRequest` interface it generated earlier.

The rest of this code follows the standard `useMutation` side effects from Tanstack which you can read about [here](https://tanstack.com/query/v4/docs/react/guides/mutations#mutation-side-effects).

When you read the page at [http://localhost:9000/books/](http://localhost:9000/books/) you will notice the new form is available. If you enter some content in it and hit "Add" - the UI updates, but if you open your network tab in the developer console (right click -> Inspect -> Network) you will see API requests being issued to the Flask server when you click the button.

Want to see how the input validation works in real time? Set the input fields to be empty and hit enter, and you will see some API errors in the console tab.

## Refreshing requests

If you want to refresh a request you can do this using the `useInvalidate` hook:

```ts
const invalidate = useInvalidate()
<button onClick={
    () => invalidate('books.details', {name: 'New book'})
}>Update book</button>
```
