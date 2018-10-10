import time
from config.config import credentials
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class Fb_bots:

        def __init__(self,driver):
            self.driver = driver


        def login_to_finn_core_messenger(self, args):
            #get login and password elements
            username_field = WebDriverWait(self.driver,10).until(EC.visibility_of_element_located((By.ID,"email")))
            password_field = WebDriverWait(self.driver,10).until(EC.visibility_of_element_located((By.ID,"pass")))

            #TODO: provide username and password #get variables from the .env
            username_field.send_keys(credentials['finn core']['username'])
            password_field.send_keys(credentials['finn core']['password'])

            #get login button and click
            login_button = self.driver.find_element_by_id("loginbutton")
            login_button.click()

            self.get_started(args)


        def get_started(self, query):
            #get 'Get Started' element and click on it
            get_started = WebDriverWait(self.driver,10).until(EC.element_to_be_clickable((By.LINK_TEXT, query[0])))
            get_started.click()
            time.sleep(5)


        def verify_text_response(self, query):
            #TODO: check waiting time
            time.sleep(5)

            #get all text responses in a list
            all_selenium_elements = self.driver.find_elements_by_xpath('//div[@attachments="List []"]')
            list_of_all_selenium_elements_text = [x.text for x in all_selenium_elements]

            #get index of last text response on the right == last user query
            all_elements_on_the_right = self.driver.find_elements_by_xpath('//div[@attachments="List []"][@data-tooltip-position="right"]')
            all_elements_on_the_right_text = [x.text for x in all_elements_on_the_right]
            last_element_on_the_right = all_elements_on_the_right_text[-1]

            #get all bot responses after the user query
            list_of_bot_responses = [x for x in list_of_all_selenium_elements_text if
                                     list_of_all_selenium_elements_text.index(x) > list_of_all_selenium_elements_text.index(last_element_on_the_right)]

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

            time.sleep(3)

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
        def verify_all_account_names_and_balances(self, args):
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

                            #check is one element has multiline response, e.g. balance and available credit
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


    ### CAROUSELS
    #make it methods
        #click on the action (view transactions or view categories)
        def action_click_1_argument_carousel(self, account_or_transaction_name):
            while True:
                parent_element = account_or_transaction_name.find_element_by_xpath('..')
                account_or_transaction_name = parent_element
                if parent_element.get_attribute('class') == '_3cne':
                    parent_element_sibling = parent_element.find_element_by_xpath('following-sibling::div')
                    parent_element_sibling.click()
                    break


        def action_click_2_arguments_carousel(self, category_or_date, action):
            while True:
                parent_element = category_or_date.find_element_by_xpath('..')
                category_or_date = parent_element
                if parent_element.get_attribute('class') == '_3cne':
                    parent_element_sibling = parent_element.find_element_by_xpath('following-sibling::div and text()="'+ action +'"')
                    parent_element_sibling.click()
                    break


        # check spending - time period - view categories or show weekly/monthly
        def view_categories(self, action):

            WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.CLASS_NAME, "_3cnp")))

            action = self.driver.find_element_by_xpath('//a[@class="_3cnp" and text()="' + action[0] + '"]')
            action.click()
            time.sleep(10)


        # get balance - view transactions for an account name - flag as fraud transactions
        def flag_as_fraud(self, transaction_name):
            transaction_name = self.driver.find_element_by_xpath('//div[@class="_3cni" and text()="' + transaction_name[0] + '"]')
            self.action_click_1_argument_carousel(transaction_name)
            time.sleep(5)


        #check spending - time period - view categories - view transactions for a category
        def view_transactions_for_categories(self, category_name):
            category_name = self.driver.find_element_by_xpath('//div[@class="_3cni" and text()="' + category_name[0] + '"]')
            self.action_click_1_argument_carousel(category_name)
            time.sleep(5)


        # check spending - time period (last month) - view categories - show weekly
        def show_weekly(self, args): #date, action arguments
            date = self.driver.find_element_by_xpath('//div[@class="_3cni" and text()="' + args[0] + '"]')
            self.action_click_2_arguments_carousel(date, args[1])
            time.sleep(5)


        # check spending - time period (last year) - view categories - show monthly
        def show_monthly(self, args):
            date = self.driver.find_element_by_xpath('//div[@class="_3cni" and text()="' + args[0] + '"]')
            self.action_click_2_arguments_carousel(date, args[1])
            time.sleep(5)
