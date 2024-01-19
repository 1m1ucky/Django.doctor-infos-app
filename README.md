# Necktie Doctor listing API App

## Purpose
- demonstrate the power of Django 4 python on a doctor listing app

## Requirements
1. Choice of Framework & Library:
    - [o] django 4 + python3.9
        a. What are the benefits & drawbacks associated with that choice?
            - easy cli
                - setup projects, auto probe and do database migrations
                - testing
                    - easy to run specific API + component test to increase dev. speed without help from postman, etc
            - rich lib / features support
                - logging
                - api frameworks
                - database admin page
            - native well designed language
        b. What are the assumptions underlying that choice?
            - python runtime installed in the deployment server
    - [o] docker
        - easy preconfig to deploy by one command
    - [o] postgresql
        - unique feature of bulk create with returned id
        - good lib + frameworks: rest api framework
        - development loggings in web console
    - [-] powerful api frameworks (HOLD ON AS NO TIME)
        - [o] [rest framework] (https://www.django-rest-framework.org/)
            - serializer to serialize back the orm data on multiple subfield relations
            - url view pattern to request mapping
            - [-] data validation (HOLD ON AS NO TIME)
            - support pagination in other projects
        - [-] [django ninja] (https://django-ninja.dev)
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
    - [o] pgcli
        - view sql tables

2. Potential Improvements:
    - much time wasting on debugging the API
        - to improve
            - use some python auto logger to help to debug
    - refactoring a better version of the CRUD model serializers by rest framework
    - provide OpenAPI swagger like doc using django ninja, integrate with rest framework
    - more assertion + testcases on postive and negative test cases
        - [*] opening hours correct infos + duplication validation, etc
    - add internal error + status code handler using rest framework

3. Production consideration:
    - deployment system pre-installations
        - docker: python3.9
    - https
        - installation of signed domain ssl certicate

4. Assumptions
    - Frontend can handle the correct use of Backend API
        - include
            - correct format of payload validated from Frontend as Backend currently not validate them
    - deployment system pre-installations
        - docker

## App featues
- [o] CRUD + bulk_create
- [o] unit + model + API tests (with good naming test cases)
    - [o] bulk_create
    - filters
        - [o] price range
        - [o] district
        - [o] lang
        - [o] category
- [o] well returned serialized data from domain models
- [-] app documentation

## App Architecture
- well designed entity CRUD pattern implementation in django ORM model layer
    - encapsulated entity serialization returns
- seperation of view + model components
- bulk_create with 1 sql query

## Setup Guideline
```sh
## setup steps are in ./scripts/setup.sh
mkdir .pg_files
docker-compose up -d
```

# Test Schemas
```sh
## test steps are in ./scripts/test.sh
. ./scripts/test.sh
```