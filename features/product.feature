Feature: Shopping Basket
  As a customer
  I want to add and remove items from my Basket
  So that I can purchase the items I want

  Scenario: Add item to Basket
    Given I am on the product page
    When I click the "Add basaket" button for a product
    Then I should see a message that the product has been added to my basaket
    And the cart count should increase by 1

  Scenario: Remove item from basaket
    Given I have items in my basaket
    And I am on the Basket page
    When I click the "Remove" button for an item
    Then I should see a message that the item has been removed from my Basket
    And the cart Basket should decrease by 1
