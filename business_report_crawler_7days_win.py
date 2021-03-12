import selenium
from selenium import webdriver
import datetime
import random
import time
import pytz
from pytz import timezone
import logging
import pandas as pd
import sys


USEREMAIL = ''
PASSWORD = ''
END_DATE_STR = ""   # ('%m/%d/%Y')
ROUND = 1

SHORT_TIME = random.uniform(2, 3)
MIDDLE_TIME = random.uniform(35, 50)
LONG_TIME = random.uniform(100, 150)
LOG_NAME = datetime.datetime.now().strftime('%y%m%d') + '.log'
FILE_PATH = ''


# logging set
logging.basicConfig(filename=LOG_NAME, level=logging.INFO, filemode='w',
                    format='%(asctime)s [%(levelname)s] %(message)s')
logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))

# The web browser of the bot is Google Chorme
driver = webdriver.Chrome()

# ------------ function start ------------


# The function that will launch the bot and automaticaly login to amazon account, the first page after login will be Amazon home page
def amazon_login():
    logging.info('----------login start----------')

    try:
        driver.get('https://sellercentral.amazon.com/home?')
        email_field = driver.find_element_by_id('ap_email')
        email_field.clear()
        email_field.send_keys(USEREMAIL)

        email_next_buttom = driver.find_element_by_id('continue')
        email_next_buttom.click()
        time.sleep(SHORT_TIME)
    except:
        logging.exception('!!!!!!!!!!Fail to enter user email!!!!!!!!!!')

    try:
        password_field = driver.find_element_by_id('ap_password')
        password_field.clear()
        password_field.send_keys(PASSWORD)

        password_signin_bittom = driver.find_element_by_id('signInSubmit')
        password_signin_bittom.click()
    except:
        logging.exception('!!!!!!!!!!Fail to enter user password!!!!!!!!!!')

    logging.warning('Please enter opt password')
    time.sleep(MIDDLE_TIME)  # Enter opt password
    # Check successfully login or not
    try:
        login_sucess = driver.find_element_by_class_name('nav-shortened-name')
    except:
        logging.exception(
            '!!!!!!!!!!Fail to login, please rerun this program again!!!!!!!!!!')
    logging.info('----------login end----------')


# The funciton that will navigate to business report webpage.
def to_business_report_page(start_date, end_date):
    logging.info('          download ' + date +
                 ' business reports start')

    business_report_url = 'https://sellercentral.amazon.com/gp/site-metrics/report.html?#&cols=/c0/c1/c2/c3/c4/c5/c6/c7/c8/c9/c10/c11/c12/c13/c14/c15&sortColumn=16&filterFromDate=' + start_date + \
        '&filterToDate=' + end_date + '&fromDate=' + start_date + '&toDate=' + end_date + \
        '&reportID=102:DetailSalesTrafficByChildItem&sortIsAscending=0&currentPage=0&dateUnit=1&viewDateUnits=ALL&runDate='
    driver.get(business_report_url)
    time.sleep(MIDDLE_TIME)

    download_buttom = driver.find_element_by_id('export')
    download_buttom.click()
    time.sleep(1)
    try:
        csv_buttom = driver.find_element_by_id('downloadCSV')
        csv_buttom.click()
    except:
        logging.exception('!!!!!!!!!!Fail to download ' +
                          date + ' business report!!!!!!!!!!')

    time.sleep(SHORT_TIME)
    driver.get('https://www.amazon.com')
    time.sleep(SHORT_TIME)
    logging.info('          download ' + date +
                 ' business reports end----------')


def to_all_listings_report():
    logging.info('----------Download all listing report start----------')
    all_listings_report_url = 'https://sellercentral.amazon.com/listing/reports/ref=xx_invreport_dnav_xx'
    driver.get(all_listings_report_url)
    time.sleep(MIDDLE_TIME)

    select_report_type_buttom = driver.find_element_by_id(
        'a-autoid-0-announce')
    select_report_type_buttom.click()
    time.sleep(SHORT_TIME)
    try:
        all_listings_report_buttom = driver.find_element_by_id('dropdown1_7')
        all_listings_report_buttom.click()
        logging.info('          clicked all listing report buttom')
        time.sleep(1)
        request_buttom = driver.find_element_by_id('a-autoid-5')
        request_buttom.click()
        logging.info('          clicked download buttom')
    except:
        logging.exception(
            '!!!!!!!!!!Fail to choose all listing report buttom, please download it by yourself!!!!!!!!!!')
    time.sleep(LONG_TIME)

    try:
        # find_element_by_class_name will find the first element
        download_buttom = driver.find_element_by_class_name('mt-link-content')
        download_buttom.click()
    except:
        logging.exception(
            '!!!!!!!!!!Fail to download all listing report, please download it by yourself!!!!!!!!!!')

    logging.info('----------Download all listing report end----------')


def add_download_date_column(business_report, pst_time):
    """
    Input: business reoprt (the report we want to edit), pst_time (Current pst time object)
    Output: business report with Download date column
    """
    download_date = []
    business_report_row_number = business_report.shape[0]
    pst_time_str = pst_time.strftime('%Y/%m/%d')
    for i in range(business_report_row_number):
        download_date.append(pst_time_str)
    business_report['Download date'] = download_date
    return business_report


def add_data_date_column(business_report, date):
    """
    Input: business reoprt (the report we want to edit), data_date_str (File's date string)
    Output: business report with Data date column
    """
    data_date = []
    business_report_row_number = business_report.shape[0]
    data_date_str = date.strftime('%Y/%m/%d')
    for i in range(business_report_row_number):
        data_date.append(data_date_str)
    # move data date to the front column
    business_report.insert(0, 'Data date', data_date)
    return business_report


def select_lang():
    lang_swither = webdriver.support.ui.Select(
        driver.find_element_by_id('sc-lang-switcher-header-select'))
    print(lang_swither.all_selected_options)
    if lang_swither.all_selected_options[0].text.find("English") == '-1':
        lang_swither.select_by_value('en_ES')
        time.sleep(5)

# ------------ function end ------------


amazon_login()
select_lang()

current_time = datetime.datetime.now()
pst_time = current_time.astimezone(timezone('US/Pacific'))
pst_time_str = pst_time.strftime('%m-%d-%y')
original_file_month = str(int(pst_time.strftime('%m')))
original_file_day = str(int(pst_time.strftime('%e')))
original_file_year = pst_time.strftime('%y')
original_file_time_str = original_file_month + '-' + \
    original_file_day + '-' + original_file_year
pst_time_str_reset_report_name = pst_time.strftime('%y%m%d')


end_date = datetime.strptime(END_DATE_STR, "%m/%d/%Y")
for i in range(ROUND):
    start_date = end_date - datetime.timedelta(days=7)
    start_date_str = start_date.strftime('%m/%d/%Y')

    logging.info('----------Process ' + data_date_str +
                 ' business reports start----------')
    to_business_report_page(start_date_str, END_DATE_STR)
    time.sleep(10)


logging.info(
    "If there is no error, congradulate you finish today's downloading!")
