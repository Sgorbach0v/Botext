import pytest
from selenium import webdriver
import time


#dict of browsers. Add more later
browsers = {
    #'firefox': webdriver.Firefox,
    'chrome': webdriver.Chrome,
}


#fixture to start driver and use in all test sessions
@pytest.yield_fixture(scope='class',params=browsers.keys())
def driver(request):
    driver = browsers[request.param]()
    yield driver
    delete_conversation(driver)
    #TODO: logout from bank before closing the browser
    driver.quit()


#fixture to open fb_messenger page: TODO: create fixture for every bot or parameters
@pytest.fixture
def finn_core_messenger(driver):
    browser = driver
    browser.get('https://www.messenger.com/t/142941776333286') #FAISTGCORE bot

    return browser

#function to delete the conversation before closing the browser
def delete_conversation(driver):
    convo_actions_button = driver.find_element_by_xpath('//div[@aria-label="Conversation actions"]')
    convo_actions_button.click()
    time.sleep(1)

    delete_convo_button = driver.find_element_by_xpath("//span[contains(text(), 'Delete')]")
    delete_convo_button.click()
    time.sleep(1)

    confirm_delete_button = driver.find_element_by_xpath("//button[contains(text(), 'Delete')]")
    confirm_delete_button.click()
    time.sleep(1)



# #fixture to open web sdk
# @pytest.fixture
# def sdk(driver):
#     browser = driver
#     browser.get('sdk url')
#     return browser
#
# #fixture to open cms page
# @pytest.fixture
# def cds(driver):
#     browser = driver
#     browser.get('sdk url')
#     return browser
