import time
from config.creds import credentials
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class atb_messenger_bot:

    def __init__(self, driver):
        self.driver = driver

    def login_to_messenger(self, args):
        # get login and password elements
        username_field = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.ID, "email")))
        password_field = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.ID, "pass")))

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
        all_elements_on_the_right = self.driver.find_elements_by_xpath(
            '//div[@class="_3058 _ui9 _hh7 _s1- _52mr _43by _3oh-"][@data-tooltip-position="right"]')
        all_elements_on_the_right_text = [x.text for x in all_elements_on_the_right]
        last_element_on_the_right = all_elements_on_the_right_text[-1]

        # get all bot responses after the user query
        list_of_bot_responses = [x for x in list_of_all_selenium_elements_text if
                                 list_of_all_selenium_elements_text.index(
                                     x) > list_of_all_selenium_elements_text.index(last_element_on_the_right)]

        return list_of_bot_responses

    def verify_qr_text(self, args):

        time.sleep(2)
        # get the QR elements
        QRs_selenium = self.driver.find_elements_by_xpath('//div[@class="_10-e"]')

        # List of unique QRs
        QRs_selenium_no_empty_list = list(filter(None, [x.text for x in QRs_selenium]))

        # TODO: ^^ not really neaded ?
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

        # send a query
    def send_query(self, args):
        while True:
            try:
                active_element = self.driver.switch_to.active_element
                active_element.send_keys(args[0])
                send_button = WebDriverWait(self.driver, 5).until(
                    EC.element_to_be_clickable((By.LINK_TEXT, 'Send')))
                send_button.click()
                break
            except:
                message_field = self.driver.find_element_by_class_name('_1mf')
                message_field.click()
                continue

        time.sleep(3)

    def click_on_persistent_menu(self, option):

        # get the hamburger button (three horizontal lines icon) and click on it
        hamburger_button = self.driver.find_element_by_class_name('_3km2')
        hamburger_button.click()

        # get the option to click object and click on it
        option_to_click = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.LINK_TEXT, option[0].replace('select ', '')))) #TODO fix
        option_to_click.click()

            #unique_account_names = []

            # while True:
            #     try:
            #         account_names = self.driver.find_elements_by_class_name('_3cni')
            #
            #         unique_account_names = [x.text for x in account_names]
            #
            #         # # check if a visible QR is not in the initial list and append it
            #         # for i in list_of_account_names:
            #         #     if i not in QRs_selenium_no_empty_list and i.text:
            #         #         QRs_selenium_no_empty_list.append(i.text)
            #
            #         # forward button click
            #         forward_button = self.driver.find_element_by_xpath("//div[@direction='forward']")
            #         forward_button.click()
            #         time.sleep(0.5)
            #     except:
            #
            #         break
            # return QRs_selenium_no_empty_list




            #CAROUSELS NOTES
            # check spending -- DONE
            # check spending: no options, 2 actions
                # _3cnp = view categories -- action #
                # _3cnp = show monthly/weekly -- action #


            # get balance - view transactions for accounts -- DONE
            #view transactions: options. 1 action
                # _3cnh = Credit card -- type N/A
                # _3cni = Credit, chequing -- product name #
                # _3cnp = view transactions -- action #

            # get balance - view transactions for accounts - flag as fraud -- DONE
            # flag_as_fraud: options. 1 action
                # _3cnh = Misc. Payment -- type N/A
                # _3cni = 7-Eleven, etc -- transaction name
                # _3cnp = Flag as fraud -- action #


            #check spending - time period - view categories - view transactions for categories -- DONE
            #view transaction for categories: options. 2 actions
                # _3cnh = Credit card -- type N/A
                # _3cni = Taxi, food -- category name #
                # _3cnp = view transactions -- action #
                # _3cnp = show monthly -- action #


            #check spending - time period (last month) - view categories - show weekly -- DONE
            #show weekly: options. 2 actions
                # _3cnh = Fast Food: From Jun 22, 18 to Jun 29, 18 - those dates but for different months
                # _3cni = Fast Food: From Mar 22, 18 to Mar 29, 18 - date on carousel
                # _3cnp = view Categories - action#
                # _3cnp = view transactions - action #

            #check spending - time period (last year) - view categories - show monthly -- DONE
            #show monthly: options. 3 actions
                # _3cnh = Fast Food: From Aug 1, 18 to Sep 1, 18 - total time period N/A
                # _3cni = Fast Food: From Aug 1, 18 to Sep 1, 18 - date on carousel
                # _3cnp = view categories #
                # _3cnp = view transactions #
                # _3cnp = view weekly - action #



        #TODO:
        #verify carousels
        #enter pin code for confirmation
        #branch locator
        #wait for the response or element to appear after a send_a_query and then continue



