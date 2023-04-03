/*
THIS FILE IS AUTO-GENERATED, DO NOT ALTER MANUALLY.

Please see flask_render_react/src/apis/types_manager.py
*/

// prettier-ignore
export interface ExampleGetExampleResponse {
    "__type__": string
    "__http_status_code__": number
    "kia": string
}

// prettier-ignore
export interface ExamplePostExampleRequest {
    "parameter_one": string
}

// prettier-ignore
export interface ExamplePostExampleResponse {
    "__type__": string
    "__http_status_code__": number
    "result": string
}

// prettier-ignore
export interface GET_MAP {
    // flask_render_react/src/views/example.py
    "example.get_example": {request: undefined, response: ExampleGetExampleResponse}
}

// prettier-ignore
export interface POST_MAP {
    // flask_render_react/src/views/example.py
    "example.post_example": {request: ExamplePostExampleRequest, response: ExamplePostExampleResponse}
}
