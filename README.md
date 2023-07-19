# 💫 Beckett Framework

_The Framework for Building strictly-typed Python and React TypeScript Websites_

![Beckett maze](docs/banner.jpg)

Welcome to Beckett, a strictly-typed Flask and React TypeScript application template.

Beckett combines a [Flask](https://flask.palletsprojects.com/en/2.3.x/) server, with a robust [React TypeScript](https://www.typescriptlang.org/docs/handbook/react.html) UI, providing a comprehensive full stack framework.

Beckett features a sophisticated types manager that automatically synchronizes [Python Type hints](https://docs.python.org/3/library/typing.html) and [TypeScript interfaces](https://www.typescriptlang.org/docs/handbook/interfaces.html). This means that as you make changes to your code, Beckett diligently keeps the API interface in perfect harmony.

While Beckett is strongly opinionated, favoring specific design choices, it significantly enhances productivity by providing a cohesive development experience and reducing the time spent on manual synchronization.

![beckett features](docs/diagram.jpg)

## Built on popular tools

Both TypeScript and Python hold their positions as two of the [most widely used programming languages globally](https://www.statista.com/statistics/793628/worldwide-developer-survey-most-used-languages/). As a result, they are frequently combined in various projects.

However, setting up a smooth and efficient development environment that harmoniously integrates these languages can be a cumbersome and time-consuming process, often leading to a subpar developer experience. Thankfully, Beckett steps in to solve this challenge by tightly coupling TypeScript and Python into one cohesive framework.

## Unleasing Their Individual Potential

Beckett recognizes that each language excels in different domains and allows you to leverage their strengths as needed. 

You can continue to write Flask views just as you would in a typical Flask application.

In the same way - you can harness the power of React TypeScript for your frontend development. Write your React components and TypeScript code as you would in any other React application, and effortlessly incorporate any JavaScript library you desire by using `yarn add` to meet the specific requirements of your project.

## Set up

Fork the code, then run the build and dev command to get started:

```bash
git clone git@github.com:beckett-software/beckett-framework.git
cd beckett-framework
make build
make dev
```
