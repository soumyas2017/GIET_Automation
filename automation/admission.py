# Login  - D
# look for branch D
# Click to apply D
# generate fakes WIP
# Fill up the details
# Submit
# Get the application ID
# Close the browser
import json
import ast
import os
import logging
import random
import time
from utilties.constants import *
from utilties.helpers import *
from services.seleniumfactory import SeleniumFactory
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from getindianname import male, female
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s:%(message)s')
logger = logging.getLogger(__name__)


class Admission:
    def __init__(self):
        self.ob = SeleniumFactory()
        self.name = ''
        self.paname = ''
        self.email = ''
        self.password = ''
        self.all_branch_links = list()
        self.apply_link = ''
        self.town = list()
        self.state = list()
        self.city = list()
        self.po = list()
        self.district = list()
        self.datadictionary = dict()
        self.actionables = {'C': 'clickable', 'T': 'typeable', 'S': 'selectable', 'D': 'directable'}

    def get_all_streams(self):
        status, elems = self.ob.search_element_by_css('a.head.item')
        if status:
            for item in elems:
                self.all_branch_links.append(item.get_attribute('href'))
        return self.all_branch_links

    def click_apply(self):
        self.ob.search_and_click_by_xpath(main_tag='a', tag_name='href', tag_value=self.apply_link)

    def login(self):
        gen = get_creds()
        try:
            self.name, self.email, self.password = list(next(gen))
            if self.ob.connect():
                if self.ob.search_and_send_keys_by_name(tag_value='email', tag_search_text=self.email):
                    if self.ob.search_and_send_keys_by_name(tag_value='password', tag_search_text=self.password):
                        if self.ob.click_by_class_name(tag_value='submit'):
                            logger.info('Success Login')
                            self.datadictionary['email'] = self.email
                            self.datadictionary['name'] = self.name
                            self.datadictionary['pass'] = self.password
                            self.apply_link = apply_link(self.get_all_streams())
                            self.datadictionary['apply_url'] = self.apply_link
                        else:
                            logger.error('Unable to locate the submit button')
                    else:
                        logger.error('Can\'t fill the password')
                else:
                    logger.error('Can\'t fill the user email')
        except Exception as e:
            logger.exception(f"Exception as {e}")

    def do_mockup(self, item, action_type="clickable"):
        status = False
        time.sleep(2)
        if action_type == 'selectable':
            tag_name, tag_value, tag_search = get_attribute_and_value(item=item,)
            if tag_value in ['correspondence_state_id', 'correspondence_city_id',]:
                status, items = self.ob.search_and_return_items_by_xpath(tag_name=tag_name, tag_value=tag_value,
                                                                  tag_search_text=tag_search)
                if status:
                    item = random.choice(items)
                    if self.ob.search_and_click_by_xpath(tag_name=tag_name, tag_value=tag_value,
                                                      tag_search_text=item):
                        self.city = item if tag_value == 'correspondence_city_id' else ''
                        return True
                    else:
                        logger.error(f"Unable to select {item}")
                else:
                    logger.error(f"Unable to find the {items}")

                status = self.ob.search_and_click_by_xpath(tag_name=tag_name, tag_value=tag_value, tag_search_text=tag_search)

            elif tag_value in ['blood_group', 'religion_id', 'nationality', 'correspondence_country_id']:
                status = self.ob.search_and_click_by_xpath(tag_name=tag_name, tag_value=tag_value, tag_search_text=tag_search)
        elif action_type == 'clickable':
            tag, tag_value, tag_text = get_attribute_and_value(item=item,  name=self.name)
            if tag_value == 'date_of_birth':
                time.sleep(2)
                if self.ob.click_by_id(tag_value):
                    yob = random.choice([year for year in range(1995, 2005)])
                    month = random.choice(['Jan', 'Feb', 'Mar', 'Apr', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
                    time.sleep(2)
                    if self.ob.search_and_click_by_xpath(tag_name='class', tag_value='ui-datepicker-year', tag_search_text=yob):
                        time.sleep(2)
                        if self.ob.search_and_click_by_xpath(tag_name='class', tag_value='ui-datepicker-month', tag_search_text=month):
                            time.sleep(2)
                            if self.ob.search_and_click_by_xpath(static_tag=date_item()):
                                time.sleep(2)
                                status = True
                            else:
                                logger.error('Unable to click on day picker')
                        else:
                            logger.error('Unable to click on month picker')
                    else:
                        logger.error('Unable to click on year picker')
                else:
                    logger.error('Unable to find DOB object')
            elif tag_value == 'sex':
                status = self.ob.search_and_click_by_xpath(main_tag='input', tag_name='value', tag_value=tag_text)
            elif tag_value == 'same_address':
                status = self.ob.click_by_id(tag_value=tag_value)
            return status
        elif action_type == 'typeable':
            tag, tag_value, tag_text = get_attribute_and_value(item=item)
            if tag_value in ['father_name', 'mother_name']:
                tag_text = tag_text.split(' ')[0] + " " + self.name.split(' ')[1]
                self.paname = tag_text
            elif tag_value in ['father_email', 'mother_email']:
                tag_text = '{}{}@{}.{}'.format(self.paname.replace(' ', '').lower(), generate_email_identifier(),
                                               random.choice(email_issuers), 'com')
            elif tag_value in ['correspondence_town', 'correspondence_po', 'correspondence_district']:
                tag_text = self.city
            status = self.ob.search_and_send_keys_by_name(tag_value=tag_value, tag_search_text=tag_text)
        elif action_type == 'directable':
            status = self.ob.search_and_click_by_xpath(static_tag=item)
        return status

    def get_mock_data(self):
        # logger.info(self.do_mockup(item=GENDER, action_type=self.actionables['C']))
        # logger.info(self.do_mockup(item=BLOOD_GROUP, action_type=self.actionables['S']))
        # logger.info(self.do_mockup(item=RELIGION, action_type=self.actionables['S']))
        # logger.info(self.do_mockup(item=NATIONALITY, action_type=self.actionables['S']))
        # logger.info(self.do_mockup(item=FATHERS_NAME, action_type=self.actionables['T']))
        # logger.info(self.do_mockup(item=FATHERS_EMAIL, action_type=self.actionables['T']))
        # logger.info(self.do_mockup(item=FATHERS_EMAIL, action_type=self.actionables['T']))
        # logger.info(self.do_mockup(item=FATHERS_PHONE_NUMBER, action_type=self.actionables['T']))
        # logger.info(self.do_mockup(item=FATHERS_OCCUPATION, action_type=self.actionables['T']))
        # logger.info(self.do_mockup(item=MOTHERS_NAME, action_type=self.actionables['T']))
        # logger.info(self.do_mockup(item=MOTHERS_EMAIL, action_type=self.actionables['T']))
        # logger.info(self.do_mockup(item=MOTHERS_PHONE_NUMBER, action_type=self.actionables['T']))
        # logger.info(self.do_mockup(item=MOTHERS_OCCUPATION, action_type=self.actionables['T']))
        # logger.info(self.do_mockup(item=EMERGENCY_PHONE, action_type=self.actionables['T']))
        # logger.info(self.do_mockup(item=AADHAR_NO, action_type=self.actionables['T']))
        # logger.info(self.do_mockup(item=DATE_OF_BIRTH, action_type=self.actionables['C']))
        # logger.info(self.do_mockup(item=COUNTRY, action_type=self.actionables['S']))
        # time.sleep(2)
        # logger.info(self.do_mockup(item=STATE, action_type=self.actionables['S']))
        # time.sleep(2)
        # logger.info(self.do_mockup(item=CITY, action_type=self.actionables['S']))
        # logger.info(self.do_mockup(item=DISTRICT, action_type=self.actionables['T']))
        # logger.info(self.do_mockup(item=PO, action_type=self.actionables['T']))
        # logger.info(self.do_mockup(item=TOWN_VILLAGE, action_type=self.actionables['T']))
        # logger.info(self.do_mockup(item=CORRESPONDENCE_ADDRESS, action_type=self.actionables['T']))
        # logger.info(self.do_mockup(item=SAME_ADDRESS, action_type=self.actionables['C']))
        # logger.info(self.do_mockup(item=CLASS_X_BOARD, action_type=self.actionables['T']))
        # logger.info(self.do_mockup(item=CLASS_X_INSTITUTE, action_type=self.actionables['T']))
        # logger.info(self.do_mockup(item=CLASS_X_PASSING_YEAR, action_type=self.actionables['T']))
        # logger.info(self.do_mockup(item=CLASS_X_GRADE_PERCENTAGE, action_type=self.actionables['T']))
        if '&id=3&' in self.apply_link:
            logger.info(self.do_mockup(item=JEE_APPEARED, action_type=self.actionables['D']))
            logger.info(self.do_mockup(item=STATE_ENTRANCE_APPEARED, action_type=self.actionables['D']))
            logger.info(self.do_mockup(item=BTECH_APPEARED, action_type=self.actionables['D']))

    def do_activity(self):
        self.login()
        self.click_apply()
        self.get_mock_data()

    # def do_activity(self):
    #
    #     else:
    #         if (self.email or self.password) is not None:
    #             try:
    #                 element = driver.find_element_by_name('email')
    #                 element.send_keys(self.email)
    #                 element = driver.find_element_by_name('password')
    #                 element.send_keys(self.password)
    #                 element = driver.find_element_by_class_name('submit').click()
    #                 try:
    #                     WebDriverWait(driver, self.wait_duration_login_class_text).until(
    #                         EC.presence_of_element_located((By.CLASS_NAME, self.login_successful_div_class)))
    #                     if self.all_branch_links.__len__() == 0:
    #                         logger.info("First Pull")
    #                         a = driver.find_elements_by_css_selector('a.head.item')
    #                         for i in a:
    #                             self.all_branch_links.append(i.get_attribute('href'))
    #                     else:
    #                         logger.info("Pull skipped")
    #                         # logger.info(self.all_branch_links)
    #
    #                     # Click on apply link
    #                     self.apply_link = str(self.randomize_stream())
    #                     driver.find_element_by_xpath(f"//a[@href='{self.apply_link}']").click()
    #
    #                     # Select Nationality
    #                     time.sleep(2)
    #                     nationality_tag, nationality_tag_text, nationality_tag_value = self.get_attribute_and_value(item=NATIONALITY)
    #                     driver.find_element_by_xpath(f"//select[@{nationality_tag}='{nationality_tag_text}']"
    #                                                  f"/option[text()='{nationality_tag_value}']").click()
    #
    #                     # Select Category
    #                     time.sleep(2)
    #                     category_tag, category_tag_text, category_tag_value = self.get_attribute_and_value(
    #                         item=CATEGORY_OF_APPLICATION)
    #                     driver.find_element_by_xpath(f"//select[@{category_tag}='{category_tag_text}']"
    #                                                  f"/option[text()='{category_tag_value}']").click()
    #
    #                     # Type in Fathers name
    #                     time.sleep(2)
    #                     fathersname_tag, fathersname_tag_text, fathersname_tag_value = self.get_attribute_and_value(
    #                         item=FATHERS_NAME)
    #                     fathersname_tag_value = fathersname_tag_value.split(' ')[0] + " " + self.name.split(' ')[1]
    #                     driver.find_element_by_name(fathersname_tag_text).send_keys(fathersname_tag_value)
    #
    #                     # Type in Fathers email
    #                     time.sleep(2)
    #                     fathersemail_tag, fathersemail_tag_text, fathersemail_tag_value = self.get_attribute_and_value(
    #                         item=FATHERS_EMAIL)
    #                     fathersemail_tag_value = '{}{}@{}.{}'.format(fathersname_tag_value.replace(' ', '').lower(),
    #                                                 self.generate_email_identifier(), random.choice(email_issuers), 'com')
    #                     driver.find_element_by_name(fathersemail_tag_text).send_keys(fathersemail_tag_value)
    #
    #                     # Type in Mothers name
    #                     time.sleep(2)
    #                     mothersname_tag, mothersname_tag_text, mothersname_tag_value = self.get_attribute_and_value(
    #                         item=MOTHERS_NAME)
    #                     mothersname_tag_value = mothersname_tag_value.split(' ')[0] + " " + self.name.split(' ')[1]
    #                     driver.find_element_by_name(mothersname_tag_text).send_keys(mothersname_tag_value)
    #
    #                     # Type in Mothers email
    #                     time.sleep(2)
    #                     mothersemail_tag, mothersemail_tag_text, mothersemail_tag_value = self.get_attribute_and_value(
    #                         item=MOTHERS_EMAIL)
    #                     mothersemail_tag_value = '{}{}@{}.{}'.format(mothersname_tag_value.replace(' ', '').lower(),
    #                                                                  self.generate_email_identifier(),
    #                                                                  random.choice(email_issuers), 'com')
    #                     driver.find_element_by_name(mothersemail_tag_text).send_keys(mothersemail_tag_value)
    #
    #                     # Type in Aadhar no
    #                     time.sleep(2)
    #                     aadharno_tag, aadharno_tag_text, aadharno_tag_value = self.get_attribute_and_value(
    #                         item=AADHAR_NO)
    #                     driver.find_element_by_name(aadharno_tag_text).send_keys(aadharno_tag_value)
    #
    #                     # Type in DOB
    #                     dob_tag, dob_tag_text, dob_tag_value = self.get_attribute_and_value(
    #                         item=DATE_OF_BIRTH)
    #                     driver.find_element_by_id(dob_tag_text).click()
    #                     time.sleep(2)
    #                     yob = random.choice([year for year in range(1995, 2005)])
    #                     driver.find_element_by_xpath(f"//select[@class='ui-datepicker-year']/option[text()='{yob}']").click()
    #                     driver.find_element_by_xpath(f"//select[@class='ui-datepicker-month']"
    #                                                  f"/option[text()='{random.choice(['Jan','Feb','Mar','Apr','May','Jun'])}']").click()
    #                     driver.find_element_by_xpath(f"/html/body/div[3]/table/tbody/tr[{random.randint(1,4)}]/td[{random.randint(1,6)}]").click()
    #
    #
    #                     # Select Gender
    #                     time.sleep(2)
    #                     gender_tag, gender_tag_text, gender_tag_value = self.get_attribute_and_value(
    #                         item=GENDER)
    #                     logger.info(gender_tag_value)
    #                     driver.find_element_by_xpath(f"//input[@value='{gender_tag_value}']").click()
    #
    #                     # Select Blood Group
    #                     time.sleep(2)
    #                     blood_group_tag, blood_group_tag_text, blood_group_tag_value = self.get_attribute_and_value(
    #                         item=BLOOD_GROUP)
    #                     driver.find_element_by_xpath(f"//select[@{blood_group_tag}='{blood_group_tag_text}']"
    #                                                  f"/option[text()='{blood_group_tag_value}']").click()
    #
    #                     # Select Religion
    #                     time.sleep(2)
    #                     religion_tag, religion_tag_text, religion_tag_value = self.get_attribute_and_value(
    #                         item=RELIGION)
    #                     driver.find_element_by_xpath(f"//select[@{religion_tag}='{religion_tag_text}']"
    #                                                  f"/option[text()='{religion_tag_value}']").click()
    #
    #                     # Occupation of Father
    #                     time.sleep(2)
    #                     fathers_occ_tag, fathers_occ_tag_text, fathers_occ_tag_value = self.get_attribute_and_value(
    #                         item=FATHERS_OCCUPATION)
    #                     driver.find_element_by_name(fathers_occ_tag_text).send_keys(fathers_occ_tag_value)
    #
    #                     # Fathers phone number
    #                     time.sleep(2)
    #                     fathersno_tag, fathersno_tag_text, fathersno_tag_value = self.get_attribute_and_value(
    #                         item=FATHERS_PHONE_NUMBER)
    #                     driver.find_element_by_name(fathersno_tag_text).send_keys(fathersno_tag_value)
    #
    #                     # Occupation of Mother
    #                     time.sleep(2)
    #                     mothers_occ_tag, mothers_occ_tag_text, mothers_occ_tag_value = self.get_attribute_and_value(
    #                         item=MOTHERS_OCCUPATION)
    #                     driver.find_element_by_name(mothers_occ_tag_text).send_keys(mothers_occ_tag_value)
    #
    #                     # Mothers phone number
    #                     time.sleep(2)
    #                     mothersno_tag, mothersno_tag_text, mothersno_tag_value = self.get_attribute_and_value(
    #                         item=MOTHERS_PHONE_NUMBER)
    #                     driver.find_element_by_name(mothersno_tag_text).send_keys(mothersno_tag_value)
    #
    #                     # Emergency contact no
    #                     time.sleep(2)
    #                     emergencyno_tag, emergencyno_tag_text, emergencyno_tag_value = self.get_attribute_and_value(
    #                         item=EMERGENCY_PHONE)
    #                     driver.find_element_by_name(emergencyno_tag_text).send_keys(emergencyno_tag_value)
    #
    #
    #                     # Select a country
    #                     time.sleep(2)
    #                     tag, tag_text, tag_value = self.get_attribute_and_value(item=COUNTRY)
    #                     driver.find_element_by_xpath(f"//select[@{tag}='{tag_text}']/option[text()='{tag_value}']") \
    #                         .click()
    #
    #                     # Get all states from dropdown
    #                     time.sleep(2)
    #                     state_tag, state_tag_text, state_tag_value = self.get_attribute_and_value(item=STATE)
    #                     states = ''.join(driver.find_element_by_xpath(f"//select[@{state_tag}='{state_tag_text}']")
    #                                      .text).split("\n")
    #                     states = self.remove_junks(states)
    #                     self.state = random.choice(states)
    #
    #                     # Select a state from dropdown
    #                     driver.find_element_by_xpath(f"//select[@{state_tag}='{state_tag_text}']/option[text()='{self.state}']") \
    #                         .click()
    #
    #                     # Get all cities from dropdown
    #                     time.sleep(2)
    #                     city_tag, city_tag_text, city_tag_value = self.get_attribute_and_value(item=CITY)
    #                     cities = ''.join(driver.find_element_by_xpath(f"//select[@{city_tag}='{city_tag_text}']")
    #                                      .text).split("\n")
    #                     cities = self.remove_junks(cities)
    #                     self.city = random.choice(cities)
    #                     self.town = self.city
    #                     self.po = self.city
    #
    #                     # Select City
    #                     time.sleep(2)
    #                     city_tag, city_tag_text, city_tag_value = self.get_attribute_and_value(
    #                         item=CITY)
    #                     driver.find_element_by_xpath(
    #                         f"//select[@{city_tag}='{city_tag_text}']/option[text()='{self.city}']") \
    #                         .click()
    #
    #                     # Type In Dist.
    #                     time.sleep(2)
    #                     dist_tag, dist_tag_text, dist_tag_value = self.get_attribute_and_value(
    #                         item=DISTRICT)
    #                     driver.find_element_by_name(dist_tag_text).send_keys(self.city)
    #
    #                     # Type in PO
    #                     time.sleep(2)
    #                     po_tag, po_tag_text, po_tag_value = self.get_attribute_and_value(
    #                         item=PO)
    #                     driver.find_element_by_name(po_tag_text).send_keys(self.city)
    #
    #                     # Type in Pincode
    #                     time.sleep(2)
    #                     pin_tag, pin_tag_text, pin_tag_value = self.get_attribute_and_value(
    #                         item=PINCODE)
    #                     driver.find_element_by_name(pin_tag_text).send_keys(pin_tag_value)
    #
    #                     # Type in Houseno
    #                     time.sleep(2)
    #                     house_add_tag, house_add_tag_text, house_add_tag_value = self.get_attribute_and_value(
    #                         item=CORRESPONDENCE_ADDRESS)
    #                     driver.find_element_by_name(house_add_tag_text).send_keys(house_add_tag_value)
    #
    #                     # Type in Town/Vill
    #                     time.sleep(2)
    #                     town_tag, town_tag_text, town_tag_value = self.get_attribute_and_value(
    #                         item=TOWN_VILLAGE)
    #                     driver.find_element_by_name(town_tag_text).send_keys(town_tag_value)
    #
    #                     # Same address @input
    #                     driver.find_element_by_id('same_address').click()
    #
    #                     # Aplicant Info #
    #
    #                     # Type in Board
    #                     time.sleep(2)
    #                     x_tag, x_tag_text, x_tag_value = self.get_attribute_and_value(
    #                         item=CLASS_X_BOARD)
    #                     driver.find_element_by_name(x_tag_text).send_keys(x_tag_value)
    #
    #                     # Type institution
    #                     time.sleep(2)
    #                     x_inst_tag, x_inst_tag_text, x_inst_tag_value = self.get_attribute_and_value(
    #                         item=CLASS_X_INSTITUTE)
    #                     driver.find_element_by_name(x_inst_tag_text).send_keys(x_inst_tag_value)
    #
    #                     # Type year of passing
    #                     time.sleep(2)
    #                     x_yop_tag, x_yop_tag_text, x_inst_tag_value = self.get_attribute_and_value(
    #                         item=CLASS_X_PASSING_YEAR)
    #                     driver.find_element_by_name(x_yop_tag_text).send_keys((str(int(yob) + 15)))
    #
    #                     # Percentage
    #                     time.sleep(2)
    #                     x_gpa_tag, x_gpa_tag_text, x_gpa_tag_value = self.get_attribute_and_value(
    #                         item=CLASS_X_GRADE_PERCENTAGE)
    #                     gpa = float(int(x_gpa_tag_value)/10) if CLASS_X_BOARD == 'CBSE' else x_gpa_tag_value
    #                     logger.info(gpa)
    #                     driver.find_element_by_name(x_gpa_tag_text).send_keys(str(gpa))
    #
    #                     try:
    #                         # Only BTECH applicants will have the below fields
    #                         if '&id=3&' in self.apply_link:
    #                             #jee_appeared,
    #                             time.sleep(2)
    #                             driver.find_element_by_xpath("/html/body/div[1]/div/div[2]/div[2]/form/div[2]/fieldset/table[9]/tbody/tr[2]/td[2]/input[2]").click()
    #
    #                             # state_entrance_appeared,
    #                             time.sleep(2)
    #                             driver.find_element_by_xpath(
    #                                 "/html/body/div[1]/div/div[2]/div[2]/form/div[2]/fieldset/table[9]/tbody/tr[3]/td[2]/input[2]").click()
    #
    #                             # dbu_get_for_btech_appeared
    #                             time.sleep(2)
    #                             driver.find_element_by_css_selector("input#dbu_get_for_btech_appeared_2").click()
    #                         else:
    #                             logger.info(self.apply_link)
    #                     except Exception as e:
    #                         logger.exception("Not available")
    #                     finally:
    #                         time.sleep(1000)
    #                         return 'Success'
    #                 except TimeoutException:
    #                     print("Loading took too much time!")
    #                     return 'Fail'
    #                 finally:
    #                     driver.close()
    #             except BaseException as e:
    #                 logger.exception(f"Some error {e}")







obj = Admission()
obj.do_activity()
# obj.login()
# ob = SeleniumFactory(url='https://2020admission.giet.edu/admission/index.php?p=login', success_element='left-panel')
# ob.connect()
# print(obj.get_attribute_and_value(item=STATE))



