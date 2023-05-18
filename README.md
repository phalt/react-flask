# 💫 Beckett

## A strongly-linked Python & Typescript Framework

### First things first: why?

Throughout my career I've seen tonnes of failed attempts to make an abstract domain language for
two very different programming languages to communicate over a bridge, for example - openapi.

However, nearly every single time I've seen this, it's been in a situation where it didn't feel like
the domain lanuage was needed, why not just maintain consistency between the two languages using their own
typing?

This solution does exactly that - instead of generating an abstract domain language, we instead pick one as the
source of truth (Python Type Hints, in this case), and then generate the other language's typing to match it.

## Set up

Getting the web server up:

```bash
python3.11 -m venv .venv
poetry install
make serve
```

Setting up the Frontend code:

```bash
nvm use
yarn
make web
```

## Usage

1. Add new pages in the `src/views` directory following the example.
2. Run the server with `make server`. Ensure development mode to generate any new types / pages.
3. To build the js run `make web`.
