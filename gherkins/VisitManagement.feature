Feature: Visit Management

  Background: 
    Given the PetClinic application is running

  Scenario: Initiate creation of a new visit
    Given an existing pet with id '67890'
    When I send a GET request to '/owners/*/pets/67890/visits/new'
    Then the response status should be 200
    And the response should contain a visit creation form

  Scenario Outline: Process creation of a new visit
    Given an existing pet with id '<petId>' belonging to owner with id '<ownerId>'
    And I have the following visit details
      | date       | description       |
      | <date>     | <description>     |
    When I submit a POST request to '/owners/<ownerId>/pets/<petId>/visits/new' with the visit details
    Then the response status should be 302
    And the response should redirect to the owner's page with the new visit

  Examples:
    | ownerId | petId | date       | description         |
    | 12345   | 67890 | 2023-04-12 | Annual vaccination  |

  Scenario: Show visits for a pet
    Given an existing pet with id '67890'
    When I send a GET request to '/owners/*/pets/67890/visits'
    Then the response status should be 200
    And the response should contain a list of visits for the pet
