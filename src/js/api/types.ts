/*
THIS FILE IS AUTO-GENERATED, DO NOT ALTER MANUALLY.

Please see beckett_framework/src/beckett/types/types_manager.py
*/

// prettier-ignore
export interface PeopleGetPeopleResponse {
    "status_code": number
    "name": string
}

// prettier-ignore
export interface PeoplePostExampleRequest {
    "parameter_one": string
}

// prettier-ignore
export interface PeoplePostExampleResponse {
    "status_code": number
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
