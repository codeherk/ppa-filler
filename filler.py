import sys
import click
import time
from selenium import webdriver
from selenium.webdriver.support.ui import Select
 
CHROMEDRIVER_PATH = "C:/Users/codeherk/Desktop/dev/chromedriver.exe"
checkbox = '//*[@id="termsAgreement"]'
agree_button = '//*[@id="disclaimerSubmitBtn"]'
select_dropdown = '//*[@id="searchBy"]'
plate_number_box = '//*[@id="otherFirstField"]'
state_dropdown = '//*[@id="state"]'
search_button = '//*[@id="ticketSearch"]'
pay_button = '//*[@id="payNowBtn"]'

driver = None

# print('Number of arguments:', len(sys.argv), 'arguments.')
# print('Argument List:', str(sys.argv))

def load():
    global driver
    url = "https://onlineserviceshub.com/ParkingPortal/Philadelphia"
    driver = webdriver.Chrome(executable_path=CHROMEDRIVER_PATH)
    driver.get(url)

    time.sleep(3)
    driver.find_element_by_xpath(checkbox).click()
    driver.find_element_by_xpath(agree_button).click()

def find_tickets(license_plate_number):
    global driver
    select = Select(driver.find_element_by_xpath(select_dropdown))
    # for option in select.options:
    #     print(option.text)

    # Ticket Number
    # License Plate
    # Notice Number
    # Payment Plan Number

    select.select_by_visible_text("License Plate")
    driver.find_element_by_xpath(plate_number_box).send_keys(license_plate_number)


    state_select = Select(driver.find_element_by_xpath(state_dropdown))
    state_select.select_by_visible_text("Pennsylvania")

    driver.find_element_by_xpath(search_button).click()
    time.sleep(2)
    table = driver.find_element_by_xpath("//*[@id=\"form0\"]/div[1]/table")
    rows = table.find_elements_by_xpath(".//tr")
    if (len(rows) > 1):
        table_headers = [td.text.replace('\n', '') for td in rows[0].find_elements_by_xpath(".//th")[1:]]
        table_headers.pop(2)
        print('\t'.join(table_headers))
        rows = rows[1:]
        for row in rows:
            ticket_row = [td.text.replace('\n', ' ') for td in row.find_elements_by_xpath(".//td")[1:]]
            ticket_row[0] = ticket_row[0].split(' ')[0]
            ticket_row.pop(2)
            print('\t'.join(ticket_row))
def pay():
    driver.find_element_by_xpath(pay_button).click()
if(len(sys.argv) != 2):
    print("python ppa.py <license-plate-number>")
    exit()
else:
    load()
    license_plate_number = sys.argv[1]
    # print(f"License Plate Number: {license_plate_number}")
    find_tickets(license_plate_number)
    pay()
