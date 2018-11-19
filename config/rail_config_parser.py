import configparser
import sys


def parse_rail_config(run_name, project_id, suite_id):
    """Provide your credentials here

    :param run_name:
    :param project_id:
    :param suite_id:
    :return:
    """
    config = configparser.ConfigParser()
    config['API'] = {'url':'xxxx',
                    'email':'xxxx',
                    'password':'xxxx'}

    config['TESTRUN'] = {'name': run_name,
                         'assignedto_id': 1,
                         'project_id': project_id,
                         'suite_id': suite_id}

    with open('config/rail_config.cfg', 'w') as configfile:
        config.write(configfile)


