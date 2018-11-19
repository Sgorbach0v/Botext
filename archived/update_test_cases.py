


### This is not needed anymore I think
#get expected outcomes for a test case based on query
def get_expected_outcomes(project_id, suite_id, case_id, query):
    """Provide your credentials here"""

    client = APIClient('xxxx')
    client.user = 'xxxx'
    client.password = 'xxxx'

    all_test_cases_list = client.send_get('get_cases/' + project_id + '&suite_id=' + suite_id)

    for test_case in all_test_cases_list:
        if test_case['id'] == case_id:
            for expected_outcome in test_case['custom_steps_separated']:
                if query in expected_outcome['content']:
                    return expected_outcome['expected']


# get_expected_outcomes(project_id='1',suite_id='1', case_id=1,query='Get Started')
# get_expected_outcomes(project_id='1',suite_id='1', case_id=2,query='Get Started')


#send new response text to the test case in test rail
def update_test_case_expected_outcomes(project_id, suite_id,case_id,query,new_expected_outcome):
    """Provide your TestRail credentials here"""
    client = APIClient('xxxx')
    client.user = 'xxxx'
    client.password = 'xxxx'

    all_test_cases_list = client.send_get('get_cases/' + project_id + '&suite_id=' + suite_id)

    for test_case in all_test_cases_list:
        if test_case['id'] == case_id:
            for expected_outcome in test_case['custom_steps_separated']:
                if query in expected_outcome['content']:
                    expected_outcome['expected'] = new_expected_outcome
                    client.send_post('update_case/' + str(case_id), test_case)
                    print('posted')



#update_test_case_expected_outcomes(project_id='1', suite_id='2',case_id=5,query='pay a bill',new_expected_outcome='select a payee\nchoose a payee\nwhom to pay')


# Limitations
## can update one expected result at a time
