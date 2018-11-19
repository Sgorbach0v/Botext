
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
#****** test case functions ******
# THIS
# IS
# WHAT
# I
# GET