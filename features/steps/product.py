from behave import given, when, then
from behave import given, when, then
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@given(u'I am on the product page')
def step_impl(context):
    # implementation to navigate to the product page
    pass

@when(u'I click the "Add basaket" button for a product')
def step_impl(context):
    # implementation to click the "Add basket" button for a product
    pass

@then(u'I should see a message that the product has been added to my basaket')
def step_impl(context):
    # implementation to verify that a message confirming the addition of the product to the basket is displayed
    pass

@then(u'the cart count should increase by 1')
def step_impl(context):
    # implementation to verify that the cart count has increased by 1 after adding the product to the basket
    pass

@given(u'I have items in my basaket')
def step_impl(context):
    # implementation to add items to the basket before running the scenario
    pass

@given(u'I am on the Basket page')
def step_impl(context):
    # implementation to navigate to the Basket page
    pass

@when(u'I click the "Remove" button for an item')
def step_impl(context):
    # implementation to click the "Remove" button for an item in the basket
    pass

@then(u'I should see a message that the item has been removed from my Basket')
def step_impl(context):
    # implementation to verify that a message confirming the removal of the item from the basket is displayed
    pass

@then(u'the cart Basket should decrease by 1')
def step_impl(context):
    # implementation to verify that the basket count has decreased by 1 after removing an item from the basket
    pass
