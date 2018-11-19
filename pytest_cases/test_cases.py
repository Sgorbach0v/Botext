from pytest_cases import printers
from pytest_testrail.plugin import pytestrail
from selenium_drivers import finn_core_driver, finn_demo_driver, atb_driver
from config.conftest import finn_core_messenger, driver, atb_messenger, finn_demo_messenger


#Dynamically creating a dictionary of functions for each step with names as test case steps
description_step_funcs = {}
#create dictionaries with functions for description test steps
def get_description_step_functions(one_test_case):

    #iterate over each step in each test case
    for test_step in one_test_case['steps']:

        #select only description steps
        if 'expected' not in test_step:
            #create function with names of steps
            #arg1 == bot == selenium class object
            #class_function == class function from selenium class == description step name, e.g. Login_to_finn_core_messenger
            #args == arguments for queries == message to send, action on a carousel, etc == each arg is on next line in test rail description step
            code = '''def {step_to_run}(arg1):
            #Step {selenium_class_function}
            arg1.{selenium_class_function}({args})
            '''.format(
                step_to_run=test_step,
                selenium_class_function=one_test_case['steps'][test_step][0],
                args=one_test_case['steps'][test_step][1:]
            )
            exec(code, {}, description_step_funcs)

# get_description_step_functions(one_test_case)
# print(description_step_funcs)


expected_result_funcs = {}
#create dictionaries with functions for expected results test steps
def get_expected_results_functions(one_test_case):

    #iterate over each step in each test case
    for test_step in one_test_case['steps']:

        #select only expected result steps
        if 'expected' in test_step:

            for key in one_test_case['steps'][test_step]:
                if 'verify' in key:
                    code ='''def {function_name}_{step}(arg1):
                    actual_result = arg1.{selenium_class_function}({args})
                    return actual_result
                    '''.format(
                        function_name = key,
                        selenium_class_function = key,
                        args=one_test_case['steps'][test_step[0:6]][1:],
                        step=test_step
                    )
                    exec(code, {}, expected_result_funcs)

# testing
# one_test_to_test_function = test_cases[1]
# get_expected_results_functions(one_test_to_test_function)
# print(expected_result_funcs)


#******* test case functions *********
#adding test case to test rail run
@pytestrail.case('C'+str(42))
#Renaming the test case with the title of the test rail case
def test_view_transactions_for_an_account(finn_core_messenger):
    
    printers.print_test_case_title('view_transactions_for_an_account')
    
    #Initialize the bot
    bot = finn_core_driver.finn_core_messenger_bot(finn_core_messenger)

    #get all test case steps for a test case
    test_case_steps = {'step_1': ['login_to_messenger', 'Get Started'], 'step_1_expected': 'logged in and opened', 'step_2': ['send_query', 'get balance'], 'step_2_expected': 'sent query', 'step_3': ['click_on_view_transactions', 'Investment'], 'step_3_expected': 'clicked'}

    #create dict of description step functions for the current test case
    one_test_case = {'id': 42, 'tc title': 'view_transactions_for_an_account', 'assistant': 'finn_core', 'channel': 'messenger', 'steps': {'step_1': ['login_to_messenger', 'Get Started'], 'step_1_expected': 'logged in and opened', 'step_2': ['send_query', 'get balance'], 'step_2_expected': 'sent query', 'step_3': ['click_on_view_transactions', 'Investment'], 'step_3_expected': 'clicked'}}
    get_description_step_functions(one_test_case)
    get_expected_results_functions(one_test_case)

    for test_step in test_case_steps:

        #select only description steps
        if 'expected' not in test_step:
            description_step_funcs[test_step](bot)
        
        #Verification
        #all other test_steps are expected outcomes steps
        else:
            #iterate over keys (text verifications)
            for key in test_case_steps[test_step]:

                #check if getting actual results are necessary
                if 'verify' in key:

                    #get actual results from messenger
                    actual_results = expected_result_funcs[key+'_'+test_step](bot)
                    
                    #get expected results from test rail
                    expected_results = test_case_steps[test_step][key]

                    if not actual_results:
                        assert 0, printers.print_assertion_error('view_transactions_for_an_account', test_step[0:6], 'No results collected', expected_results, key)

                    for actual_result in actual_results:
                        assert actual_result in expected_results, printers.print_assertion_error('view_transactions_for_an_account', test_step[0:6], actual_result, expected_results, key)

                    #printing success if passed
                    printers.print_successful_text_verification(test_step[5:6],test_case_steps[test_step[0:6]], key, actual_results, expected_results)

            #printing success of step if there is no verify in expected outcomes step
            if type(test_case_steps[test_step]) != dict:
                printers.print_success_no_verification_step(test_step[5:6],test_case_steps[test_step[0:6]], test_case_steps[test_step])
            