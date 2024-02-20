Feature: Vet Management

  Background: 
    Given the PetClinic application is running

  Scenario: Show vet list in HTML format
    When I send a GET request to '/vets'
    Then the response status should be 200
    And the response should contain a list of vets in HTML format

  Scenario: Show vet list in JSON format
    When I send a GET request to '/vets.json'
    Then the response status should be 200
    And the response should contain a list of vets in JSON format
    And the response should match the JSON schema for vets

  Scenario: Show vet list in XML format
    When I send a GET request to '/vets.xml'
    Then the response status should be 200
    And the response should contain a list of vets in XML format
    And the response should match the XML schema for vets
