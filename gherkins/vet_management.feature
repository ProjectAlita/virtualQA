Feature: Vet Management

  Background:
    Given the PetClinic application is running

  Scenario: List all vets in HTML format
    When I request the list of all vets in HTML format
    Then the response should be an HTML page listing the vets

  Scenario: List all vets in JSON format
    When I request the list of all vets in JSON format
    Then the response should be a JSON list of the vets

  Scenario: List all vets in XML format
    When I request the list of all vets in XML format
    Then the response should be an XML list of the vets
