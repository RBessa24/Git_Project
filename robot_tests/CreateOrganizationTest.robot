*** Settings ***
Library        CreateOrganizationTest.py

*** Test Cases ***
Create Organization Test

    ${ret}=    Create Organization Test   %{API_BASE_URL}
    Should Be True    ${ret}    