# Ritain - TM632 - Party Management API - Resources Manager


# API Overview

This repository holds an implementation of the TMF 632 Party Management API. Through this API it is possible to create/read/update/delete organizations and their details.


## REST API Standardization

This Service's API is standardized with the TM632 - Party Management REST API specification. More information on this TMF standard can be found [here](https://www.tmforum.org/resources/standard/tmf632-party-management-api-rest-specification-r19-0-0/), and its OpenAPI 3 specification is available [here](https://tmf-open-api-table-documents.s3.eu-west-1.amazonaws.com/OpenApiTable/4.0.0/swagger/TMF632-Party-v4.0.0.swagger.json). Only the Organization-related endpoints were implemented and, for now, only (i) the Organization's base information, (ii) its Party Characteristics, and (iii) its validity Time Period are persisted. More endpoints and features will be added on demand.

## Run the API

To run the API you need to define some environment variables:

```
APP_ENV
DB_LOCATION
DB_NAME
DB_USER
DB_PASSWORD
```

If you with to only do some minor testing on the API, you must set the `APP_ENV` variable to `test` (`export APP_ENV=test`).
In this scenario, you don't need to defined the remaining environment variables. The API will rely on a local SQLite database.

When running the API in a production environment, you must rely on a PostgreSQL database. Thus, you must set all the previously listed environment variables.
In this case, the `APP_ENV` variable should be set to `Production`.
Thus, you must do the following:

``` bash
export APP_ENV=Production
export DB_LOCATION=<db_location>
export DB_NAME=<db_name>
export DB_USER=<db_user>
export DB_PASSWORD=<db_password>
```

### Manually

After defining the environment vairables...

```bash
cd api
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
#export APP_ENV=test
uvicorn main:app
```


### Docker

When running the API in a production environment, please refer to this section.

The first step you'll have to take is to build the API's Docker Image.
To do so, from the root directory, execute the following command: `docker build --no-cache -f docker/Dockerfile  -t ritain:tmf632-party-mgmt-api  ./`

Then, you may rely on the `docker-compose.yaml` file, under `/docker` to deploy the API alongside with a PostgreSQL Database.

``` bash
cd docker
docker-compose up -d # or... docker compose up -d
```

## Documentation

After running the API, you can access its OpenAPI Specification (documentation) via the following URL: `http://<api_ip>:<api_port>/docs`.


## How to Test

### Unitary Tests

```bash
cd api
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
# Set APP_ENV to test, before running the tests
export APP_ENV=test
pytest # or python3 -m pytest
```

### E2E Tests

First of all, you need to deploy the App (for instance, through docker-compose)
Only then, you may run the E2E tests.

First of all, install all required dependencies...

```bash
cd robot_tests
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Then, you should create an environment variable that maps the API's base URL (e.g: http://<api_ip>:<api_port>):

```bash
export API_BASE_URL="http://127.0.0.1:80"
```

Finally, execute the robot tests:

```bash
robot . 
# or python3 -m robot .
```

## Usage Examples

1. Create New Organization
``` bash
curl --location 'http://127.0.0.1:80/organization' \
--header 'Content-Type: application/json' \
--data '{
 "tradingName": "Ritain",
 "isHeadOffice": true,
 "isLegalEntity": true,
 "name": "Ritain - Fundao Headquarters",
 "organizationType": "Testbed",
 "existsDuring": {
    "startDateTime": "2015-10-22T08:31:52.026Z"
 },
 "status": "validated"
}'
````

2. Get All Organizations
``` bash
curl --location 'http://127.0.0.1:80/organization'
```

3. Get A Specific Organization
``` bash
curl --location 'http://127.0.0.1:80/organization?tradingName=Ritain&fields=name%2CtradingName'
```

4. Update a Specific Organization
```bash
curl --location --request PATCH 'http://127.0.0.1:80/organization/1' \
--header 'Content-Type: application/json' \
--data '{
 "tradingName": "Ritain",
 "isHeadOffice": true,
 "isLegalEntity": true,
 "name": "Ritain - Porto Headquarters",
 "organizationType": "Testbed",
 "existsDuring": {
    "startDateTime": "2015-10-22T08:31:52.026Z"
 },
 "status": "validated"
}'
```

5. Delete an Organization

```bash
curl --location --request DELETE 'http://127.0.0.1:80/organization/1'
```
