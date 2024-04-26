Feature: Checkout process
  As a logged-in user
  I want to be able to checkout the items in my cart
  So that I can purchase my selected products

  Scenario: User checks out items successfully
    Given I am a logged-in user
    And I have items in my cart
    When I navigate to the checkout page
    And I confirm my order details
    Then I should be able to place an order successfully
