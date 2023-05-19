# 💫 Beckett

![Beckett maze](docs/banner.jpg)

## A strongly-linked Python & Typescript Framework

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
