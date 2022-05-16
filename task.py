import logging
import os
import sys
from RPA.Browser.Selenium import Selenium
from RPA.Windows import Windows
from RPA.HTTP import HTTP


browser_lib = Selenium()
http_lib = HTTP()
win_lib = Windows()

EMPLOYEE_LIST_APP_PATH = f"{os.getcwd()}\\EmployeeList.exe"
EMPLOYEE_LIST_APP_TITLE = "Employee Database"
AMOUNT_OF_EMPLOYEES_TO_PROCESS = 10
HR_API_URL = "https://botgames-employee-data-migration-vwsrh7tyda-uc.a.run.app/employees"
HR_WEB_APP_URL = "https://developer.automationanywhere.com/challenges/automationanywherelabs-employeedatamigration.html"


def complete_human_resources_challenge():
    open_employee_list_app(EMPLOYEE_LIST_APP_PATH)
    open_hr_web_app(HR_WEB_APP_URL)
    complete_all_employee_details(AMOUNT_OF_EMPLOYEES_TO_PROCESS)
    take_screenshot_of_results()
    win_lib.close_window(EMPLOYEE_LIST_APP_TITLE)


def open_employee_list_app(path):
    win_lib.windows_run(path, wait_time=1)


def open_hr_web_app(url):
    browser_lib.open_available_browser(url)


def complete_all_employee_details(amount_of_employees_to_process):
    for i in range(amount_of_employees_to_process):
        complete_employee_details()


def complete_employee_details():
    id = get_employee_id()
    employee_data = get_employee_data(id)
    fill_in_employee_data(employee_data)


def get_employee_id():
    return browser_lib.get_value("css:#employeeID")


def get_employee_data(id):
    hr_api_data = get_hr_api_data(id)
    employee_app_data = get_employee_app_data(id)
    return {**hr_api_data, **employee_app_data}


def get_hr_api_data(id):
    hr_api_response = get_hr_api_response(id)
    json_data = hr_api_response.json()
    return dict(
        phone_number = json_data["phoneNumber"],
        start_date = json_data["startDate"]
    ) 


def get_hr_api_response(id):
    api_url = f"{HR_API_URL}?id={id}"
    return http_lib.http_get(api_url)


def get_employee_app_data(id):
    win_lib.control_window(EMPLOYEE_LIST_APP_TITLE, wait_time=0.2)
    win_lib.click("id:btnClear", wait_time=0.2)
    win_lib.set_value("id:txtEmpId", id)
    win_lib.click("id:btnSearch", wait_time=0.2)
    data = {
        "first_name": "txtFirstName",
        "last_name": "txtLastName",
        "email": "txtEmailId",
        "city": "txtCity",
        "zip_code": "txtZip",
        "job_title": "txtJobTitle",
        "department": "txtDepartment",
        "manager": "txtManager",
        "state": "txtState",
    }
    for name, elem_id in data.items():
        data[name] = win_lib.get_value(f"id:{elem_id}")
    return data


def fill_in_employee_data(employee):
    fill_field("css:#firstName", employee["first_name"])
    fill_field("css:#lastName", employee["last_name"])
    fill_field("css:#phone", employee["phone_number"])
    fill_field("css:#email", employee["email"])
    fill_field("css:#city", employee["city"])
    fill_field("css:#zip", employee["zip_code"])
    fill_field("css:#title", employee["job_title"])
    fill_field("css:#startDate", employee["start_date"])
    fill_field("css:#manager", employee["manager"])
    browser_lib.select_from_list_by_value("css:#state", employee["state"])
    browser_lib.select_from_list_by_value("css:#department", employee["department"])
    browser_lib.click_button("css:#submitButton")


def fill_field(locator, value):
    browser_lib.input_text(locator, value)


def take_screenshot_of_results():
    browser_lib.wait_until_element_is_visible("css:.modal-confirm")
    browser_lib.screenshot(filename="output/result.png")


def initialize_logging():
    stdout = logging.StreamHandler(sys.stdout)

    logging.basicConfig(
        level=logging.INFO,
        format="{%(filename)s:%(lineno)d} %(levelname)s - %(message)s",
        handlers=[stdout]
    )


if __name__ == "__main__":
    initialize_logging()
    complete_human_resources_challenge()
