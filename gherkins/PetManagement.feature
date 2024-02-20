Feature: Pet Management

  Background: 
    Given the PetClinic application is running

  Scenario: Initiate creation of a new pet
    Given an existing owner with id '12345'
    When I send a GET request to '/owners/12345/pets/new'
    Then the response status should be 200
    And the response should contain a pet creation form

  Scenario Outline: Process creation of a new pet
    Given an existing owner with id '<ownerId>'
    And I have the following pet details
      | name      | birthDate  | type        |
      | <name>    | <birthDate> | <type>      |
    When I submit a POST request to '/owners/<ownerId>/pets/new' with the pet details
    Then the response status should be 302
    And the response should redirect to the owner's page with the new pet

  Examples:
    | ownerId | name   | birthDate  | type |
    | 12345   | Bella  | 2020-04-23 | Dog  |

  Scenario: Initiate update of a pet
    Given an existing pet with id '67890' belonging to owner with id '12345'
    When I send a GET request to '/owners/12345/pets/67890/edit'
    Then the response status should be 200
    And the response should contain a pet update form

  Scenario Outline: Process update of a pet
    Given an existing pet with id '<petId>' belonging to owner with id '<ownerId>'
    And I have the updated pet details
      | name      | birthDate  | type        |
      | <name>    | <birthDate> | <type>      |
    When I submit a POST request to '/owners/<ownerId>/pets/<petId>/edit' with the updated pet details
    Then the response status should be 302
    And the response should redirect to the owner's page with the updated pet

  Examples:
    | ownerId | petId | name   | birthDate  | type |
    | 12345   | 67890 | Max    | 2019-05-30 | Cat  |
