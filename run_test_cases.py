import argparse
import time
import os
from config import rail_config_parser
from pytest_cases import printers
import pytest
from test_rail_data.get_post_test_rail import test_rail

#converting argument input to numbers as assigned in test rail TODO: make it a dictionary, rather than ifs
def choose_project_and_suite(assistant, channel, suite):
    project_and_suite_dict = {}
    if channel == 'messenger' and assistant == 'finn core':
        project_and_suite_dict['project_id'] = '1'
        if suite == 'regression':
            project_and_suite_dict['suite_id'] = '9' #TODO change 9 to 1
        elif suite == 'smoke':
            project_and_suite_dict['suite_id'] = '3'

    elif channel == 'messenger' and assistant == 'finn demo':
        project_and_suite_dict['project_id'] = '4'
        if suite == 'demo':
            project_and_suite_dict['suite_id'] = '10'
        elif suite == 'smoke':
            project_and_suite_dict['suite_id'] = '3'

    elif channel == 'websdk' and assistant == 'finn core':
        project_and_suite_dict['project_id'] = '1'
        if suite == 'regression':
            project_and_suite_dict['suite_id'] = '12'
        elif suite == 'smoke':
            project_and_suite_dict['suite_id'] = '13'
    elif channel == 'messenger' and assistant == 'atb':
        project_and_suite_dict['project_id'] = '2'
        if suite == 'regression':
            project_and_suite_dict['suite_id'] = '5'

    else:
        print('PROVIDE VALID ARGUMENT INPUT')
        exit()

    return project_and_suite_dict


#generate test case for pytest with the requested parameters and write them to a separate file
#assistant_channel_name will be sent to assistant name in the dict obtained from test rail
#assistant_channel_name --> fixture name
def generate_test_cases(test_case_info, assistant, channel_name):
    '''
    todo: add docstrings
    :param test_case_info:
    :param assistant_channel_name:
    :return:
    '''

    all_after_asterisks = []

    with open('pytest_cases/test_cases.py', 'r') as myfile:
        reader = myfile.read()
        list_of_lines = reader.split('\n')
        for i in list_of_lines:
            if 'test case functions' in i:
                all_after_asterisks = list_of_lines[:list_of_lines.index(i) + 1]
                break
    all_after_asterisks_add_back = '\n'.join(all_after_asterisks)

    rail = test_rail()
    test_cases = rail.get_info_for_testcases(project_id=test_case_info['project_id'],
                                             suite_id=test_case_info['suite_id'],
                                             assistant=assistant,
                                             channel_name=channel_name)

    test_case_code = []
    for one_test_case in test_cases:
        code = '''
#adding test case to test rail run
@pytestrail.case('C'+str({test_case_id}))
#Renaming the test case with the title of the test rail case
def test_{test_case_title}({assistant}_{channel}):
    
    printers.print_test_case_title('{test_case_title}')
    
    #Initialize the bot
    bot = {assistant}_driver.{assistant}_{channel}_bot({assistant}_{channel})

    #get all test case steps for a test case
    test_case_steps = {test_case_steps}

    #create dict of description step functions for the current test case
    one_test_case = {one_test_case}
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
                        assert 0, printers.print_assertion_error('{test_case_title}', test_step[0:6], 'No results collected', expected_results, key)

                    for actual_result in actual_results:
                        assert actual_result in expected_results, printers.print_assertion_error('{test_case_title}', test_step[0:6], actual_result, expected_results, key)

                    #printing success if passed
                    printers.print_successful_text_verification(test_step[5:6],test_case_steps[test_step[0:6]], key, actual_results, expected_results)

            #printing success of step if there is no verify in expected outcomes step
            if type(test_case_steps[test_step]) != dict:
                printers.print_success_no_verification_step(test_step[5:6],test_case_steps[test_step[0:6]], test_case_steps[test_step])
            '''.format(
            test_case_id=one_test_case['id'],
            test_case_title=one_test_case['tc title'],
            assistant=one_test_case['assistant'],
            channel= one_test_case['channel'],
            test_case_steps=one_test_case['steps'],
            one_test_case=one_test_case,
        )

        test_case_code.append(code) # appends test cases

    print(printers.print_number_of_test_case(test_case_code))

    with open('pytest_cases/test_cases.py', 'w') as myfile:
        for i in all_after_asterisks_add_back:
            myfile.write(i)
        for k in test_case_code:
            myfile.write(k)

#get path and name for html report
def report_path_name():
    cwd = os.getcwd()
    report = {}
    report['path'] = cwd + '/reports/'
    report['name'] = time.strftime('test_report_%Y%m%d_%H%M%S.html')
    return report



if __name__ == '__main__':

    #parsing arguments
    parser = argparse.ArgumentParser()
    requiredNamed = parser.add_argument_group('required named arguments')
    requiredNamed.add_argument('-a', '--assistant', help='Enter assistant: "finn core", atb, etc.', required=True)
    requiredNamed.add_argument('-c', '--channel', help='Enter channel: messenger, websdk', required=True)
    requiredNamed.add_argument('-s', '--suite', help='Enter test suite: regression, smoke', required=True)

    parser.add_argument("-b", '--browser', help='Enter browser. Chrome by default')
    parser.add_argument("-l", '--lang_code', help='Enter language code. en-CA by default')

    args = parser.parse_args()


    #print the beginning
    printers.print_start(args.assistant, args.channel, args.suite)

    # dictionary with project and suite ids TODO: change to a dict
    test_case_info = choose_project_and_suite(args.assistant, args.channel, args.suite)


    # getting data from test rail and creating pytest test cases
    generate_test_cases(test_case_info, args.assistant.replace(' ', '_'), args.channel)


    # Modifying rail_config.cfg to create a test run with correct configuration
    run_name = " ".join([args.assistant, args.channel, args.suite, 'at ' + time.strftime('%H:%M')])
    rail_config_parser.parse_rail_config(run_name=run_name, project_id=test_case_info['project_id'], suite_id=test_case_info['suite_id'])

    #html path and name
    report = report_path_name()

    # defining arguments for pytest
    # " --disable-warnings" -- disable annoying warnings
    # "--count=10 " -- test n times
    #" --testrail --tr-config=config/rail_config.cfg" -- test rail config
    args_string = "pytest_cases/test_cases.py --html=" + report['path'] + report['name'] + \
                                                                " --self-contained-html " \
                                                                "--metadata Channel {channel_name} --metadata Assistant {assistant} --metadata Suite {suite} " \
                                                                "--count=1" \
                                                                " --disable-warnings"\
                                                                " --reruns 0".format(
        channel_name=args.channel,
        assistant=args.assistant.replace(" ", "_"),
        suite=args.suite
    )
    #running pytest
    pytest.cmdline.main(args_string.split(" "))

    printers.print_finish(report)

