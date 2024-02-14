Feature: Owner Management

  Background: 
    Given the PetClinic application is running

  Scenario Outline: Create a new owner with valid data
    Given I have the following owner details
      | firstName | lastName | address       | city    | telephone   |
      | <firstName> | <lastName> | <address> | <city> | <telephone> |
    When I submit a request to create a new owner
    Then the response should indicate the owner was created successfully
    And the response should include owner details "<firstName>" "<lastName>" with a non-null ID

  Examples:
    | firstName | lastName | address       | city    | telephone   |
    | John      | Doe      | 123 Main St.  | Anytown | 1234567890  |
    | Jane      | Roe      | 456 Elm St.   | Newtown | 0987654321  |

  Scenario: Create a new owner with missing required fields
    Given I have the following incomplete owner details
      | firstName | lastName | address | city | telephone |
      | John      |          | 123 Main St. | Anytown | 1234567890 |
    When I submit a request to create a new owner
    Then the response should indicate a validation error

  Scenario: Find owner with existing last name
    Given existing owners with lastName "Doe"
    When I submit a request to find owners by last name "Doe"
    Then the response should show a list of owners with last name "Doe"

  Scenario: Find owner with non-existing last name
    Given no existing owner with lastName "NonExisting"
    When I submit a request to find owners by last name "NonExisting"
    Then the response should indicate no owners found

  Scenario Outline: Update an existing owner with valid data
    Given an existing owner with id <ownerId>
    And I have the updated owner details
      | firstName | lastName | address       | city    | telephone   |
      | <firstName> | <lastName> | <address> | <city> | <telephone> |
    When I submit a request to update the owner with id <ownerId>
    Then the response should indicate the owner was updated successfully
    And the response should include updated owner details "<firstName>" "<lastName>"

  Examples:
    | ownerId | firstName | lastName | address       | city    | telephone   |
    | 1       | John      | Smith    | 123 Main St.  | Anytown | 1234567890  |
    | 2       | Jane      | Doe      | 456 Elm St.   | Newtown | 0987654321  |

  Scenario: Update an existing owner with invalid data
    Given an existing owner with id 1
    When I submit a request to update the owner with id 1 with the following details missing city
      | firstName | lastName | address       | telephone   |
      | John      | Smith    | 123 Main St.  | 1234567890  |
    Then the response should indicate a validation error

  Scenario: Display an existing owner's details
    Given an existing owner with id 1
    When I submit a request to display the owner's details with id 1
    Then the response should show the details for owner with id 1

  # Add teardown steps to clean up created entities