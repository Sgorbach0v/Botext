from test_rail_data.testrail_api.testrail import APIClient

class test_rail(APIClient):

    #TODO: move usernames, passwords to .env file
    def __init__(self):
        """Provide your credentials here

        """
        self.client = APIClient('xxxx')
        self.client.user = 'xxxx'
        self.client.password = 'xxxx'

    #get all test cases for a specified project and suite from test rail
    def get_all_test_cases(self, project_id, suite_id,):
        all_test_cases_list = self.client.send_get('get_cases/' + project_id + '&suite_id=' + suite_id)
        return all_test_cases_list

    #TODO: do not allow empty action and expected result steps
    #get information about all test cases from test rail
    def get_info_for_testcases(self, project_id, suite_id, assistant='default_name', channel_name='default_name'):
        all_test_cases = self.get_all_test_cases(project_id=project_id, suite_id=suite_id)
        list_of_all_test_cases = []

        #iterate over all test cases
        for one_test_case in all_test_cases:
            description_steps_dict = {}

            counter = 1

            #get steps for each test case
            for step_item in one_test_case['custom_steps_separated']:

                expected_steps_dict = {}


                #take only action steps (not expected steps) and create a list of a query + argument (message, action, ...)
                #list is needed to handle queries with arguments. If no args, then return a list with one list item. All args will be on the next line in test rail
                if '\n' in step_item['content']:
                    step_pytest = step_item['content'].split('\n')

                    #rid of 'and', 'for' for consistency where test rail steps have multiple steps in one
                    for conjunction in ['and', 'for']:
                        if conjunction in step_pytest:
                            conj_index = step_pytest.index(conjunction)
                            step_pytest.pop(conj_index)

                    #adding underscore so the first step can be used as a function name in pytest
                    step_pytest[0] = step_pytest[0].lower().replace(' ','_')

                else:
                    step_pytest = [step_item['content'].lower().replace(' ', '_')]

                #get exepected outcomes
                expected_outcome_pytest = step_item['expected']

                #split expected result step by new line
                list_of_exepcted_outcomes = expected_outcome_pytest.split('\n')

                #get indexes of lines that tell what to verify
                list_of_indexes_of_lines_with_verify = [list_of_exepcted_outcomes.index(x) for x in list_of_exepcted_outcomes if 'verify' in x.lower()]


                #iterate over all of the indexes
                for i in range(len(list_of_indexes_of_lines_with_verify)):

                    #create exepected result steps dictionary:
                    #key -- line that tells what to verify
                    #value -- lines between the lines that tell you what to verify
                    try:
                        #print(list_of_exepcted_outcomes[list_of_indexes_of_lines_with_verify[i]],':',list_of_exepcted_outcomes[list_of_indexes_of_lines_with_verify[i]+1: list_of_indexes_of_lines_with_verify[i+1]])
                        line_with_verify = list_of_exepcted_outcomes[list_of_indexes_of_lines_with_verify[i]].lower().replace(' ', '_')
                        index_of_next_line_with_verify = list_of_indexes_of_lines_with_verify[i]+1
                        index_of_next_verify_line = list_of_indexes_of_lines_with_verify[i+1]

                        list_of_texts_to_verify = list_of_exepcted_outcomes[index_of_next_line_with_verify:index_of_next_verify_line]
                        expected_steps_dict.update({line_with_verify: list_of_texts_to_verify})
                        #print(expected_steps_dict)
                    except:
                        #print(list_of_exepcted_outcomes[list_of_indexes_of_lines_with_verify[i]], ':',
                              #list_of_exepcted_outcomes[list_of_indexes_of_lines_with_verify[i]+1:])

                        line_with_verify = list_of_exepcted_outcomes[list_of_indexes_of_lines_with_verify[i]].lower().replace(' ', '_')
                        index_of_next_line_with_verify = list_of_indexes_of_lines_with_verify[i] + 1
                        list_of_texts_to_verify = list_of_exepcted_outcomes[
                                                  index_of_next_line_with_verify:]

                        expected_steps_dict.update({line_with_verify: list_of_texts_to_verify})

                #if nothing to verify, use the string from expected result step from test rail
                if not bool(expected_steps_dict):
                    expected_steps_dict = step_item['expected'].lower()

                #create a dictionary for description and epected result steps
                description_steps_dict.update({'step_' + str(counter) : step_pytest})
                description_steps_dict.update({'step_' + str(counter) + '_expected' : expected_steps_dict})
                counter = counter + 1

            # create a dictionary with only required information for pytest use
            dictionary_for_pytest = {'id': one_test_case['id'],
                                     'tc title': one_test_case['title'].replace(' ','_').lower(),
                                     'assistant': assistant,
                                     'channel': channel_name,
                                     'steps': description_steps_dict,
                                     #'Platform': one_test_case['custom_platform'], not yet implemented. Maybe add later
                                     }

            list_of_all_test_cases.append(dictionary_for_pytest)

        self.all_test_cases = list_of_all_test_cases
        return list_of_all_test_cases


# #testing
# rail = test_rail()
# # result = rail.get_all_test_cases(str(1),str(1))
# result2 = rail.get_info_for_testcases(str(1),str(1))
# #
# #print(result)
# for i in result2:
#      print('script returns', i)

