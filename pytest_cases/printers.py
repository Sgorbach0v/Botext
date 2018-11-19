
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
    Status: passed'''.format(
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


def print_start(channel, assistant, test_suite):
    start_string = '''
    Testing started
    Channel: {channel}
    Assistant: {assistant}
    Test suite: {test_suite}'''.format(
        channel=channel,
        assistant=assistant,
        test_suite=test_suite
    )
    print(start_string)


def print_finish(report):
    string = '''
Pytest report: {path}{name}
Test rail run results: http://testing.testrail.run_example
    '''.format(
        path=report['path'],
        name=report['name']
    )
    print(string)


def print_test_case_title(test_case):
    string='''        Test case: {test_case}'''.format(
        test_case=test_case
    )
    print(string)


def print_number_of_test_case(number_of_test_cases):
    string='''    Number of test cases: {number_of_test_cases}
    '''.format(
        number_of_test_cases=len(number_of_test_cases)
    )
    #print(string)
    return string