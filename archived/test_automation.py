import sys
#adding root folder to sys.path
sys.path.extend(['/Users/sgorbachov/Documents/Selenium_automation'])

from config.conftest import finn_core_messenger, driver
from selenium_drivers.finn_core_driver import Fb_bots
from pytest_testrail.plugin import pytestrail
from config.creds import credentials
from test_rail_data.get_post_test_rail import test_rail
import pytest
import os
import argparse
import time
from config.rail_config_parser import parse_rail_config


parser = argparse.ArgumentParser()
requiredNamed = parser.add_argument_group('required named arguments')
requiredNamed.add_argument("assistant", help="select valid assistant")
requiredNamed.add_argument("channel", help="select valid channel")
requiredNamed.add_argument("test_suite", help="select valid test suite")
parser.add_argument("-b", "--browser", help='Enter browser. Chrome by default')
args = parser.parse_args()


#converting argument input to numbers as assigned in test rail
def choose_project_and_suite(assistant, channel, suite):
    project_and_suite_dict = {}
    if channel == 'messenger' and assistant == 'finn core':
        project_and_suite_dict['project_id'] = '1'
        if suite == 'regression':
            project_and_suite_dict['suite_id'] = '1'
        elif suite == 'smoke':
            project_and_suite_dict['suite_id'] = '3'

    elif channel == 'websdk' and assistant == 'finn core':
        project_and_suite_dict['project_id'] = '1'
        if suite == 'regression':
            project_and_suite_dict['suite_id'] = '12'
        elif suite == 'smoke':
            project_and_suite_dict['suite_id'] = '13'
    else:
        print('PROVIDE VALID ARGUMENT INPUT')

    return project_and_suite_dict


#getting project and suite ids
test_case_info = choose_project_and_suite(args.assistant, args.channel, args.test_suite)


#getting data from test rail
assistant_channel_name = '_'.join([args.assistant.replace(' ', '_'),args.channel])
rail = test_rail()
test_cases = rail.get_info_for_testcases(project_id=test_case_info['project_id'],suite_id=test_case_info['suite_id'], assistant_channel_name=assistant_channel_name)


#Modifying rail_config.cfg to create a test run
run_name = " ".join([args.assistant, args.channel, args.test_suite, 'at '+time.strftime('%H:%M')])
parse_rail_config(run_name=run_name,project_id=test_case_info['project_id'],suite_id=test_case_info['suite_id'])


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


def print_assertion_error(test_case, test_step, actual_result, expected_result,key):
    string = '''
    ------------------------------------------------------------- FAILED --------------------------------------------------------------------
    Failing test case: {test_case_title}
    Failing step: {test_step_string} 
    Failed verification step: {key_string}
    Failing query: {actual_result_string}
    Expected: {expected_result_string}
    -----------------------------------------------------------------------------------------------------------------------------------------
    '''.format(
        test_case_title=test_case,
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



# Dynamically creating a test case (function) for pytest from test rail test cases -- fix so only

for one_test_case in test_cases:  #TODO: maybe fix the loop
    code = '''
    #Renaming the test case with the title of the test rail case
#@pytestrail.case('C'+str({test_case_id}))
def test_{test_case_title}({assistant}):
        
        print('        Test case: {test_case_title}')

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



            #********VERIFICATION STEP HERE*********
            #test_case_steps = Steps: Step_1:[Login to messenger] , Step_1 expected: [Verify text:[Hello],...
            #test_step = Step_1 expected, Step_2 expected, ...
            #test_case_steps[test_step] = dict -- 'Verify text':[a,b,c], 'Verify QRs': [e,f,g]



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
                            assert actual_result in expected_results, print_assertion_error('{test_case_title}', test_step[0:6], actual_result, expected_results, key)

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

def get_html_path_and_title():
    cwd = os.getcwd()
    report = {}
    if cwd.endswith('pytest_cases'):
        path_for_report = cwd[:-12] + 'reports/'
    else:
        path_for_report = cwd + '/reports/'

    report['path'] = path_for_report
    report['title'] = time.strftime('test_report_%Y%m%d_%H%M%S.html')

    return report



if __name__ == "__main__":

    start_string = '''
    Testing started
    Channel: {channel}
    Assistant: {assistant}
    Test suite: {test_suite}
    '''.format(
        channel=args.channel,
        assistant=args.assistant,
        test_suite=args.test_suite
    )
    print(start_string)

    #getting path and title for html report
    report = get_html_path_and_title()

    #defining arguments for pytest
    # " --testrail --tr-config=/Users/sgorbachov/Documents/Selenium_automation/config/rail_config.cfg" \

    args_string = "--html=" + report['path'] + report['title'] + " --self-contained-html " \
                  "--metadata Channel {channel_name} --metadata Assistant {assistant} --metadata Suite {suite}" \
                  " --disable-warnings".format(
        channel_name=args.channel,
        assistant=args.assistant.replace(" ", "_"),
        suite=args.test_suite
    )
    #print(args_string)

    #"--html=../reports/report.html --self-contained-html" #--testrail --tr-config='../config/rail_config.cfg'"

    #running pytest
    pytest.cmdline.main(args_string.split(" "))

    print()
    print('Pytest report: '+ report['path'] + report['title'])
    print('Test rail run results: http://testing.testrail.run_example')
    print()








