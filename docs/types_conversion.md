# 🎹 Types conversion

> **Remember!** Beckett doesn't just convert one way.
>
> API requests going _into_ the Beckett Flask service will be checked for type consistency.

Beckett Framework uses [Beckett types](https://github.com/beckett-software/beckett-types) to manage types translation.

## Conversion chart

We translate Python TypeHints into these TypeScript types, and vice versa:

| Python | TypeScript |
|--------|------------|
| `str`  | `string`   |
| `int`  | `number`   |
| `float`           | `number`   |
| `decimal.Decimal` | `number`   |
| `dict`  | `Record<string, any>`   |

## Nested types

Nested `attrs` classes are converted infinitely:

```py linenums="1" title="example.py"

@attrs.define
class Subclass:
    hello: str

@attrs.define
class ExamplePageProps:
    test: Subclass
```

Which generates:

```ts linenums="1" title="types.ts"
// prettier-ignore
export interface Subclass {
    "hello": string
}

// prettier-ignore
export default interface PageProps {
    "test": Subclass
}

```
