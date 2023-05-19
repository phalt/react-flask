/*
THIS FILE IS AUTO-GENERATED, DO NOT ALTER MANUALLY.

Please see beckett_framework/src/beckett/types/types_manager.py
*/

// prettier-ignore
export interface PeopleGetPeopleResponse {
    "__type__": string
    "__http_status_code__": number
    "name": string
}

// prettier-ignore
export interface PeoplePostExampleRequest {
    "parameter_one": string
}

// prettier-ignore
export interface PeoplePostExampleResponse {
    "__type__": string
    "__http_status_code__": number
    "result": string
}

// prettier-ignore
export interface GET_MAP {
    // beckett_framework/src/views/people.py
    "people.get_people": {request: undefined, response: PeopleGetPeopleResponse}
}

// prettier-ignore
export interface POST_MAP {
    // beckett_framework/src/views/people.py
    "people.post_example": {request: PeoplePostExampleRequest, response: PeoplePostExampleResponse}
}
