# Doctor listing API App

## Requirements
1. Choice of Framework & Library:
    - django 4 (as fast to test + rich ecosystem support on python libraries)
        a. What are the benefits & drawbacks associated with that choice?
            - easy cli
                - setup projects, auto probe and do database migrations
                - testing
                    - easy to run specific API + component test to increase dev. speed without help from postman, etc
            - rich lib / features support
                - logging
                - api frameworks
                - database admin page
        b. What are the assumptions underlying that choice?
            - python runtime installed in the deployment server
    - docker
        - easy preconfig to deploy by one command
    - postgresql
        - unique feature of bulk create with returned id
        - good lib + frameworks: rest api framework
        - development loggings in web console
    - powerful api frameworks
        - [django ninja] (https://django-ninja.dev)
            - data schema validation on API input
            - auto API input params / query parsing by easy rules
            - data schema parsing on API output
            - auto 404 / other error response of certain errors
            - auto OpenAPI documentation with editor
                - API search
            - support pagination in other projects
            - api routing support in other porjects
            - authorization in other projects
            - exception handler
            - api versioning
    - pgcli
        - view sql tables
    
2. Potential Improvements:
    - much time wasting on debugging the API
        - to improve
            - use some python auto logger to help to debug

3. Production consideration:
    - installations
        - docker

4. Assumptions
    - Frontend can handle the correct use of Backend API
        - include
            - correct format of payload validated from Frontend as Backend currently not validate them

## App featues
- [o] CRUD + bulk_create
- [o] unit + model + API tests + bulk_create
    - [o] price range
    - [o] district
    - [o] lang
    - [o] category
- [o] well returned serialized data from domain models
- [o] app documentation

- [] CRUD v2 rest framework fast to use serializer
    - must with ninja?
    - using rest framework serializer + filtering

## App Architecture
- well designed entity CRUD pattern implementation in django ORM model layer
    - encapsulated entity serialization returns
- seperation of view + model components
- bulk_create with 1 sql query

## Setup Guideline
```sh
## setup steps are in ./scripts/setup.sh
docker-compose up -d
```

# Test Schemas
```sh
## test steps are in ./scripts/test.sh
./scripts/test.sh
```

# Difficulties
- much time wasting on debugging the API
- [*] refactoring a better version of the CRUD model serializers

## Future Improvements
- more assertion + testcases on postive and negative test cases