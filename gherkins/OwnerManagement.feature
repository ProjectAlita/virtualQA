Feature: Owner Management

  Background: 
    Given the PetClinic application is running

  Scenario: Initiate creation of a new owner
    When I send a GET request to '/owners/new'
    Then the response status should be 200
    And the response should contain an owner creation form

  Scenario Outline: Process creation of a new owner
    Given I have the following owner details
      | firstName | lastName | address       | city    | telephone |
      | <firstName> | <lastName> | <address> | <city> | <telephone> |
    When I submit a POST request to '/owners/new' with the owner details
    Then the response status should be 302
    And the response should redirect to the created owner's page

  Examples:
    | firstName | lastName | address       | city    | telephone |
    | John      | Doe      | 123 Main St.  | Anytown | 1234567890 |

  Scenario: Initiate owner search
    When I send a GET request to '/owners/find'
    Then the response status should be 200
    And the response should contain an owner search form

  Scenario Outline: Process find owner form
    When I submit a GET request to '/owners' with the query parameter lastName '<lastName>'
    Then the response status should be 200
    And the response should contain a list of owners or redirect to single owner page

  Examples:
    | lastName |
    | Doe      |
    | Smith    |

  Scenario: Initiate update of an owner
    Given an existing owner with id '12345'
    When I send a GET request to '/owners/12345/edit'
    Then the response status should be 200
    And the response should contain an owner update form

  Scenario Outline: Process update of an owner
    Given an existing owner with id '<ownerId>'
    And I have the updated owner details
      | firstName | lastName | address       | city    | telephone |
      | <firstName> | <lastName> | <address> | <city> | <telephone> |
    When I submit a POST request to '/owners/<ownerId>/edit' with the updated owner details
    Then the response status should be 302
    And the response should redirect to the updated owner's page

  Examples:
    | ownerId | firstName | lastName | address       | city    | telephone |
    | 12345   | Jane      | Roe      | 456 Elm St.   | Newtown | 0987654321 |

  Scenario: Show an owner
    Given an existing owner with id '12345'
    When I send a GET request to '/owners/12345'
    Then the response status should be 200
    And the response should contain the details of the owner
