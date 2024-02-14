Feature: Visit Management

  Background: 
    Given the PetClinic application is running
    And an owner with id 1 exists in the system
    And a pet with id 101 belonging to owner with id 1 exists in the system

  Scenario: Initiate a new visit form for a pet
    When I submit a request to initiate a new visit form for pet with id 101
    Then the response should show the new visit form

  Scenario Outline: Create a new visit for a pet with valid data
    Given I have the following visit details
      | date       | description          |
      | <date>     | <description>        |
    When I submit a request to create a new visit for pet with id 101
    Then the response should indicate a redirect to the owner's details page
    And the response should include the new visit details with a non-null ID

  Examples:
    | date       | description          |
    | 2023-05-01 | Annual vaccination   |
    | 2023-06-15 | General checkup      |

  Scenario: Create a new visit for a pet with invalid data
    Given I have the following incomplete visit details
      | date       | description |
      |            | Checkup     |
    When I submit a request to create a new visit for pet with id 101
    Then the response should indicate a validation error

  Scenario: Show all visits for a pet
    When I submit a request to show all visits for pet with id 101
    Then the response should show a list of all visits for the pet
