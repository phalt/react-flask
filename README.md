# 💫 React Flask (RF)

### Fully typed Flask and React applications

![maze](/docs/banner.jpg)

Welcome to RF, a _strongly-linked_ Flask and React application template.

RF combines a [Flask](https://flask.palletsprojects.com/en/2.3.x/) server, with a [React TypeScript](https://www.typescriptlang.org/docs/handbook/react.html) UI into a comprehensive full-stack framework for building modern web applications.

RF features a sophisticated types manager that automatically synchronizes [Python Type hints](https://docs.python.org/3/library/typing.html) and [TypeScript interfaces](https://www.typescriptlang.org/docs/handbook/interfaces.html). This means that as you make changes to your API code in the server, RF diligently keeps the API Client up to date.

## Built on popular tools

We use cutting edge Python tools including:

* [Pydantic 2.0](https://docs.pydantic.dev/latest/)
* [Flask 2.3](https://flask.palletsprojects.com/en/2.3.x/)

And our TypeScript is modern too:

* [Node 18.17.0](https://nodejs.org/en)
* [React 18](https://react.dev/)
* [TypeScript 5.1](https://www.typescriptlang.org/)

Both TypeScript and Python hold their positions as two of the [most widely used programming languages globally](https://www.statista.com/statistics/793628/worldwide-developer-survey-most-used-languages/). As a result, they are frequently combined in various projects.

However, setting up a smooth and efficient development environment that integrates these languages can be a cumbersome and time-consuming process, often leading to a subpar developer experience. Thankfully, RF steps in to solve this challenge by through it's sophisticated types manager.

## Type-safe productivity boost

RF provides:

* A types manager which keeps the API interface type-safe.
* React: A collection of type-safe API hooks for querying the HTTP API.
* React: No single page app, so bundled JS for the client loads faster.
* Flask: A manager for generating new React pages without any manual effort.
* Flask: View-based routing to reduce the bundle size of JS on page loads.

## Currently in development

Before this becomes a fully fledged package, it exists as a decent template that can be forked when you start a new project and worked on from there.

## Set up

Fork the code, then run the build and dev command to get started:

```bash
git clone git@github.com:beckett-software/react-flask.git
cd react-flask
make build
make dev
```
