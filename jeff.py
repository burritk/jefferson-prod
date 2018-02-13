import json
import requests
from lxml import etree
from selenium.webdriver.common.keys import Keys

from pyscraper import iterator
from pyscraper.selenium_utils import get_headless_driver, get_selenium_xpath_if_exists
from excel_writer import write_to_excel


# Pulling parcel numbers
def get_parcel_numbers(filename):
    session = requests.Session()
    for i in range(1,20):
        file = open(filename + str(i) + '.txt', 'a+')
        form_data = {'owner': '', 'pageNumber': str(i), 'pageSize': '10000'}
        response = session.post('http://www.jpassessor.com/property-search?option=com_ajax&module=propertysearch&format=json&method=getByOwner', data=form_data)
        content = json.loads(response.content)
        data = json.loads(content['data'])
        file.seek(0)
        print len(data['pageData'])
        for datum in data['pageData']:
            print(datum['parcel_number'])
            file.write(datum['parcel_number'] + "\n")
        file.truncate()
        file.close()

def get_parcel_data(input_file, output_file):
    # session = requests.Session()
    # with open(input_file + '.txt', 'r') as input:
    #     parcel_numbers = input.readlines()
    xpath = {}
    xpath['current_date'] = '/html/body/div[2]/div/div/div/table/tbody/tr[2]/td/table/tbody/tr[1]/td[4]/span'
    xpath['ward'] = '/html/body/div[2]/div/div/div/table/tbody/tr[2]/td/table/tbody/tr[2]/td[2]/span'
    xpath['owner_name'] = '/html/body/div[2]/div/div/div/table/tbody/tr[2]/td/table/tbody/tr[3]/td[2]/span'
    xpath['homestead_exemption'] = '/html/body/div[2]/div/div/div/table/tbody/tr[2]/td/table/tbody/tr[3]/td[4]/span'
    xpath['mailing_street'] = '/html/body/div[2]/div/div/div/table/tbody/tr[2]/td/table/tbody/tr[4]/td[2]/span/text()[1]'
    xpath['mailing_city_state_zip'] = '/html/body/div[2]/div/div/div/table/tbody/tr[2]/td/table/tbody/tr[4]/td[2]/span/text()[2]'
    xpath['subdivision'] = '/html/body/div[2]/div/div/div/table/tbody/tr[2]/td/table/tbody/tr[4]/td[4]/span'
    xpath['improvement_address'] = '/html/body/div[2]/div/div/div/table/tbody/tr[2]/td/table/tbody/tr[5]/td[2]/span'
    xpath['legal_description'] = '/html/body/div[2]/div/div/div/table/tbody/tr[2]/td/table/tbody/tr[5]/td[4]/span'
    xpath['land_assessment'] = '/html/body/div[2]/div/div/div/table/tbody/tr[3]/td/table/tbody/tr[2]/td[1]/span'
    xpath['improvement_assessment'] = '/html/body/div[2]/div/div/div/table/tbody/tr[3]/td/table/tbody/tr[2]/td[2]/span'
    xpath['total_assessment'] = '/html/body/div[2]/div/div/div/table/tbody/tr[3]/td/table/tbody/tr[2]/td[3]/span'


    with open(output_file + '.txt', 'a') as output:
        url = 'http://www.jpassessor.com/property-search?tmpl=component&detail=true&parcel='
        counter = 0
        print(counter)
        for id, text in iterator.url_xpath_file(url, input_file, **xpath):
            print(id)
            selection = 'id '
            line = id
            for key, value in text.iteritems():
                selection += key + " "
                line += '"' + value
            output.write(line + '\n')
            counter += 1
            print selection + " " + str(counter)

            # print line
def get_tax_data(input_file, output_file):
    counter = 0
    driver = get_headless_driver()
    driver.get("https://propertytax.jpso.com/PropertyTax/propsrch.aspx#result")
    # with open('super_output' + str(sys.argv[1]) + '.txt', 'a+') as real_output:
    with open(output_file + '.txt', 'a') as real_output:
        counter = sum(1 for line in real_output)
        # with open('output' + str(sys.argv[1]) + '.txt', 'r') as parcels:
        with open(input_file + '.txt', 'r') as parcels:
            skipped = 0
            for index, parcel in enumerate(parcels):
                if index < counter:
                    continue
                try:

                    print counter, skipped
                    select = driver.find_element_by_xpath('//*[@id="ContentPlaceHolder1_body_cboSearchBy"]')
                    select.send_keys('pp')
                    bar = driver.find_element_by_xpath('//*[@id="ContentPlaceHolder1_body_txtParcel_In"]')
                    bar.send_keys(parcel.split('"')[0].strip())
                    bar.send_keys(Keys.ENTER)
                    hex = driver.find_element_by_xpath('//*[@id="ContentPlaceHolder1_body_lblHEX"]')
                    tax = driver.find_element_by_xpath('//*[@id="ContentPlaceHolder1_body_lblTaxAmt"]')
                    hextax = hex.text + '"' + tax.text
                    string_to_concat = parcel.strip() + '"' + hextax
                    history_button = driver.find_element_by_xpath('//*[@id="ContentPlaceHolder1_body_btViewHistory"]')
                    history_button.click()
                    rows = driver.find_elements_by_class_name('text_smaller')

                    tax = {}
                    for i in range(1, 4):
                        year = ''
                        tax_notice = ''
                        assessment = ''
                        original_tax_due = ''
                        paid_amount = ''
                        date_paid = ''
                        balance_due = ''
                        year = get_selenium_xpath_if_exists(driver, '//*[@id="ContentPlaceHolder1_body_dgHistory"]/tbody/tr[' + str(i + 1) + ']/td[1]')
                        tax_notice = get_selenium_xpath_if_exists(driver, '//*[@id="ContentPlaceHolder1_body_dgHistory"]/tbody/tr[' + str(i + 1) + ']/td[2]')
                        assessment = get_selenium_xpath_if_exists(driver, '//*[@id="ContentPlaceHolder1_body_dgHistory"]/tbody/tr[' + str(i + 1) + ']/td[3]')
                        original_tax_due = get_selenium_xpath_if_exists(driver, '//*[@id="ContentPlaceHolder1_body_dgHistory"]/tbody/tr[' + str(i + 1) + ']/td[4]')
                        paid_amount = get_selenium_xpath_if_exists(driver, '//*[@id="ContentPlaceHolder1_body_dgHistory"]/tbody/tr[' + str(i + 1) + ']/td[5]')
                        date_paid = get_selenium_xpath_if_exists(driver, '//*[@id="ContentPlaceHolder1_body_dgHistory"]/tbody/tr[' + str(i + 1) + ']/td[6]')
                        balance_due = get_selenium_xpath_if_exists(driver, '//*[@id="ContentPlaceHolder1_body_dgHistory"]/tbody/tr[' + str(i + 1) + ']/td[7]')

                        tax_concat = '"' + year + '"' + tax_notice + '"' + assessment + '"' + original_tax_due + '"' + paid_amount + '"' + date_paid + '"' + balance_due
                        string_to_concat += tax_concat

                    real_output.write(string_to_concat + '\n')
                    print(string_to_concat)
                    back_button = driver.find_element_by_xpath('//*[@id="MAIN_OUTLINE_TABLE"]/div[1]/div/div[2]/a/img')
                    back_button.click()
                    counter += 1
                except:
                    driver.close()
                    driver = get_headless_driver()
                    driver.get("https://propertytax.jpso.com/PropertyTax/propsrch.aspx#result")
                    skipped += 1
                    continue

get_parcel_numbers('parcels')
get_parcel_data('parcels', 'parcel_data')
get_tax_data('parcel_data', 'tax_data')

write_to_excel('tax_data', 'output')

