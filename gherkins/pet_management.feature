Feature: Pet Management

  Background: 
    Given the PetClinic application is running
    And an owner with id 1 exists in the system

  Scenario Outline: Create a new pet with valid data
    Given I have the following pet details
      | name     | birthDate  | type      |
      | <name>   | <birthDate>| <type>    |
    When I submit a GET request to initiate pet creation for owner with id 1
    Then the response should show the pet creation form
    When I submit a POST request to create a new pet for owner with id 1 with the following details
      | name     | birthDate  | type      |
      | <name>   | <birthDate>| <type>    |
    Then the response should indicate a redirect to the owner's details page
    And the response should include pet details "<name>" with a non-null ID

  Examples:
    | name   | birthDate  | type |
    | Fluffy | 2020-04-12 | Dog  |
    | Whiskers | 2019-08-09 | Cat  |

  Scenario: Create a new pet with invalid data
    Given I have the following pet details
      | name | birthDate | type |
      |      | 2020-04-12| Dog  |
    When I submit a POST request to create a new pet for owner with id 1 with the following details
      | name | birthDate | type |
      |      | 2020-04-12| Dog  |
    Then the response should indicate a validation error

  Scenario Outline: Update an existing pet with valid data
    Given an existing pet with id 10 belonging to owner with id 1
    And I have the updated pet details
      | name     | birthDate  | type      |
      | <name>   | <birthDate>| <type>    |
    When I submit a GET request to initiate pet update for pet with id 10
    Then the response should show the pet update form
    When I submit a POST request to update the pet with id 10 for owner with id 1 with the following details
      | name     | birthDate  | type      |
      | <name>   | <birthDate>| <type>    |
    Then the response should indicate a redirect to the owner's details page
    And the response should include updated pet details "<name>"

  Examples:
    | name   | birthDate  | type |
    | Fido   | 2018-03-15 | Dog  |
    | Mittens | 2017-07-21 | Cat  |

  Scenario: Update an existing pet with invalid data
    Given an existing pet with id 10 belonging to owner with id 1
    When I submit a POST request to update the pet with id 10 for owner with id 1 with the following details
      | name | birthDate | type |
      | Fido |           | Dog  |
    Then the response should indicate a validation error

  # Add teardown steps to clean up created entities