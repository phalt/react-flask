/*
THIS FILE IS AUTO-GENERATED, DO NOT ALTER MANUALLY.

Please see beckett_framework/src/apis/types_manager.py
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
    // beckett_framework/src/views/example.py
    "example.get_example": {request: undefined, response: ExampleGetExampleResponse}
}

// prettier-ignore
export interface POST_MAP {
    // beckett_framework/src/views/example.py
    "example.post_example": {request: ExamplePostExampleRequest, response: ExamplePostExampleResponse}
}
