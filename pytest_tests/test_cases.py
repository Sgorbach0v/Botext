from config.conftest import *
from selenium_tests.selenium_test_cases import *
from pytest_testrail.plugin import pytestrail
from config.config import credentials
from testrail.get_post_test_rail import test_rail
import pytest
import os


# initialize the test rail class and get all test cases
rail = test_rail()
test_cases = rail.get_info_for_testcases()


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
            #arg1.{selenium_class_function}({selenium_class_function}={args}) #sending as kwarg to better readability: just in case
            '''.format(
                step_to_run = test_step,
                selenium_class_function = one_test_case['steps'][test_step][0],
                args = one_test_case['steps'][test_step][1:]
            )
            exec(code, {}, description_step_funcs)


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


def print_assertion_error(test_step, actual_result, expected_result,key):
    string = '''
    ------------------------------------------------------------- FAILED --------------------------------------------------------------------
    Failing step: {test_step_string} 
    Failed verification step: {key_string}
    Failing query: {actual_result_string}
    Expected: {expected_result_string}
    -----------------------------------------------------------------------------------------------------------------------------------------
    '''.format(
        test_step_string=test_step,
        actual_result_string=actual_result,
        expected_result_string=expected_result,
        key_string=key,
        header=test_step[0:6].upper()
    )
    return string

def print_successful_text_verification(number, test_step, key, actual_results, expected_results):
    string = '''
        -------------------------------------------------------------- PASSED -------------------------------------------------------------------
        Step {number}: {test_step_string}
        Verification step: {key_string}
        Actual result: {actual_results_string}
        Expected result: {expected_results_string}
        Result: passed'''.format(
                test_step_string = test_step,
                key_string=key,
                actual_results_string=actual_results,
                expected_results_string=expected_results,
                number = number
                        )
    print(string)


def print_success_no_verification_step(number, test_step, expected_results):
    string = '''
        -------------------------------------------------------------- PASSED -------------------------------------------------------------------
        Step {number}: {test_step_string}
        Expected result: {expected_results_string}'''.format(
        test_step_string=test_step,
        expected_results_string=expected_results,
        number = number,
            )
    print(string)


# Dynamically creating a test case (function) for pytest from test rail test cases
for one_test_case in test_cases:  #TODO: maybe fix the loop
    code = '''
    #Renaming the test case with the title of the test rail case
#@pytestrail.case('C'+str({test_case_id}))
def test_{test_case_title}({assistant}):      
         
        one_test_case = {one_test_case}
        
        #Initialize the bot
        bot = Fb_bots({assistant})

        #get all test case steps for a test case
        test_case_steps = {test_case_steps}
        
        #create dict of description step functions just for this test case
        get_description_step_functions(one_test_case)
        get_expected_results_functions(one_test_case)
        
        for test_step in test_case_steps:

            #select only description steps
            if 'expected' not in test_step:
                description_step_funcs[test_step](bot)
                
                
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
                            assert 0, 'Something went wrong. No actual results have been collected'
                        
                        for actual_result in actual_results:
                            assert actual_result in expected_results, print_assertion_error(test_step[0:6], actual_result, expected_results, key)
                        
                        #printing success if passed
                        print_successful_text_verification(test_step[5:6],test_case_steps[test_step[0:6]], key, actual_results, expected_results)
                        
                #printing success of step without verification
                if type(test_case_steps[test_step]) != dict:
                    print_success_no_verification_step(test_step[5:6],test_case_steps[test_step[0:6]], test_case_steps[test_step])  
        '''.format(
        test_case_id=one_test_case['id'],
        test_case_title=one_test_case['tc title'],
        assistant=one_test_case['assistant'],
        test_case_steps=one_test_case['steps'],
        one_test_case = one_test_case,
    )

    # Executing the string code
    exec(code)
