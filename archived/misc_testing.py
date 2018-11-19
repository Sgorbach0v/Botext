import os



def report_path():
    cwd = os.getcwd()
    print('Aboslute path',cwd)
    print(cwd.find('Selenium_automation'))
    print(cwd[:28])


report_path()