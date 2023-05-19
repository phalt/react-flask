# 💫 Beckett framework

_A strongly-linked Python & Typescript Framework_

![beckett logo](banner.jpg)

Beckett framework is the fastest way to build a type-safe Python webserver and React TypeScript website with consistent typing interfaces in languages.

Beckett bundles a Flask application and a React web server into one full stack framework, and tightly-couples the Typed API interface without the need for an intermediary domain language.
At it's core, Beckett provides a types manager that keeps the Python Type hints and TypeScript interfaces in sync for you as you make changes. THis means that changes can be deployed confidentally without worrying if the API interface defintions in either language will drift - Beckett just won't let them.

Because it is strongly-linked it also automatically provides `Props` to React pages from the Flask view linked to it.

It is strongly opinionated, but it boosts productivity.
