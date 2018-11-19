import time
from config.creds import credentials
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class finn_demo_messenger_bot:

    def __init__(self,driver):
        self.driver = driver


    def login_to_messenger(self, args):
        # get login and password elements
        username_field = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.ID,"email")))
        password_field = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.ID,"pass")))

        # TODO: provide username and password #get variables from the .env
        username_field.send_keys(credentials['finn core']['username'])
        password_field.send_keys(credentials['finn core']['password'])

        # get login button and click
        login_button = self.driver.find_element_by_id("loginbutton")
        login_button.click()

        self.get_started(args)


    def get_started(self, query):
        # get 'Get Started' element and click on it
        get_started = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.LINK_TEXT, query[0])))
        get_started.click()
        time.sleep(5)


    def verify_text_response(self, query):
        # TODO: check waiting time
        time.sleep(5)

        # get all text responses in a list
        all_selenium_elements = self.driver.find_elements_by_xpath('//span[@class="_3oh- _58nk"]')
        list_of_all_selenium_elements_text = [x.text for x in all_selenium_elements]


        # get index of last text response on the right == last user query
        all_elements_on_the_right = self.driver.find_elements_by_xpath('//div[@class="_3058 _ui9 _hh7 _s1- _52mr _43by _3oh-"][@data-tooltip-position="right"]')
        all_elements_on_the_right_text = [x.text for x in all_elements_on_the_right]
        last_element_on_the_right = all_elements_on_the_right_text[-1]

        #get all bot responses after the user query
        list_of_bot_responses = [x for x in list_of_all_selenium_elements_text if
                                 list_of_all_selenium_elements_text.index(x) > list_of_all_selenium_elements_text.index(last_element_on_the_right)]

        # check if one element has multiline response and split it by '\n'
        for text_response in list_of_bot_responses:
            if '\n' in text_response:
                for z in text_response.split('\n'):
                    list_of_bot_responses.append(z)
                list_of_bot_responses.pop(list_of_bot_responses.index(text_response))

        return list_of_bot_responses


    def verify_qr_text(self, args):

        time.sleep(2)
        #get the QR elements
        QRs_selenium = self.driver.find_elements_by_xpath('//div[@class="_10-e"]')

        #List of unique QRs
        QRs_selenium_no_empty_list = list(filter(None, [x.text for x in QRs_selenium]))

        #TODO: ^^ not really neaded ?
        while True:
            try:
                # get all the visible QRs
                QRs_selenium_forward = self.driver.find_elements_by_xpath('//div[@class="_10-e"]')

                # check if a visible QR is not in the initial list and append it
                for i in QRs_selenium_forward:
                    if i.text not in QRs_selenium_no_empty_list and i.text:
                        QRs_selenium_no_empty_list.append(i.text)

                # forward button click
                forward_button = self.driver.find_element_by_xpath("//div[@direction='forward']")
                forward_button.click()
                time.sleep(0.5)
            except:
                break

        return QRs_selenium_no_empty_list


    def take_screenshot(self,title):
        self.driver.save_screenshot("../reports/screenshots/"+title+".png")


    #send a query
    def send_query(self, args):
        while True:
            try:
                active_element = self.driver.switch_to.active_element
                active_element.send_keys(args[0])
                send_button = WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable((By.LINK_TEXT, 'Send')))
                send_button.click()
                break
            except:
                message_field = self.driver.find_element_by_class_name('_1mf')
                message_field.click()
                continue

        time.sleep(4)

    #go to secure login
    def authenticate(self, args):
        self.send_query(['login'])
        self.click_go_to_secure_login()
        self.enter_username_and_password_for_secure_login()

    def click_go_to_secure_login(self):
        go_to_secure_login = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.LINK_TEXT,'🔒Go to secure login')))
        go_to_secure_login.click()

    #enter username and login for bank
    def enter_username_and_password_for_secure_login(self):
        #switch to iframe
        self.driver.switch_to.frame(self.driver.find_element_by_name("messenger_ref"))

        # get login and password elements
        username_field = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.ID, "username")))
        password_field = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.ID, "password")))

        #provide username and password TODO: get username and password from .env
        username_field.send_keys('123')
        password_field.send_keys('123')
        time.sleep(2)

        #click on login button
        login_button = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.TAG_NAME, 'button')))
        login_button.click()
        time.sleep(2)

        #switch back to default frame
        self.driver.switch_to.default_content()
        time.sleep(2)

    #USE THIS AS THE EXAMPLE FOR THE REST OF THE FUNCTIONS
    #click on a QR based on provided text
    def click_on_qr(self, QR_text):
        #QR_button = self.driver.find_element_by_xpath('//div[@class="_10-e" and text()="'+QR_text+'"]')
        QR_button = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//div[@class="_10-e" and text()="'+QR_text[0]+'"]')))
        QR_button.click()
        time.sleep(10)

    #get account names and their balances from carousels
    def verify_account_names_and_amounts(self, args):
        time.sleep(5)
        account_names_selenium = self.driver.find_elements_by_class_name('_3cni')

        list_of_account_names_no_empties = list(filter(None, [x.text for x in account_names_selenium]))


        while True:
            try:
                # get all the visible carousel items
                account_names = self.driver.find_elements_by_class_name('_3cni')

                # check if a visible carousel item is not in the initial list and append it
                for i in account_names:
                    if i.text not in list_of_account_names_no_empties and i.text:

                        #check if one element has multiline response, e.g. balance and available credit
                        if '\n' in i.text:
                            #split by line and add to the list
                            for z in i.text.split('\n'):
                                list_of_account_names_no_empties.append(z)
                        else:
                            list_of_account_names_no_empties.append(i.text)

                # forward button click
                forward_button = self.driver.find_element_by_xpath("//div[@direction='forward']")
                forward_button.click()
                time.sleep(0.5)
            except:
                break

        return list_of_account_names_no_empties

    # def verify_button_name(self, button_name):
    #
    #     time.sleep(3)
    #     print(button_name)
    #
    #     #button_to_verify = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.LINK_TEXT, button_name)))
    #
    #     go_to_secure_login = WebDriverWait(self.driver, 10).until(
    #         EC.visibility_of_element_located((By.LINK_TEXT, '🔒Go to secure login')))
    #
    #
    #
    #     print(go_to_secure_login.text)
    #
    #     return button_to_verify.text


    #click on persistent menu
    def click_on_persistent_menu(self, option):

        #get the hamburger button (three horizontal lines icon) and click on it
        hamburger_button = self.driver.find_element_by_class_name('_3km2')
        hamburger_button.click()

        #click on the option and if it's not there click 'more' and click on the option
        try:
            # get the option to click object and click on it
            option_to_click = WebDriverWait(self.driver, 1).until(EC.element_to_be_clickable((By.LINK_TEXT, option[0].replace('select ', ''))))
            option_to_click.click()
        except:
            # get 'more' button and click on it
            more_button = WebDriverWait(self.driver, 1).until(EC.element_to_be_clickable((By.LINK_TEXT, 'More')))
            more_button.click()

            # get the option to click object and click on it
            option_to_click = WebDriverWait(self.driver, 1).until(EC.element_to_be_clickable((By.LINK_TEXT, option[0].replace('select ', ''))))
            option_to_click.click()
        #TODO: add a printer function or handle errors in a different place
        finally:
            #print the error
            print('Option is not in the persistent menu')
            assert 0, 'Option is not in the persistent menu'