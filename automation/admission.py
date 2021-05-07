# Login  - D
# look for branch D
# Click to apply D
# generate fakes WIP
# Fill up the details
# Submit
# Get the application ID
# Close the browser
import time
from utilties.constants import *
from utilties.helpers import *
from services.seleniumfactory import SeleniumFactory
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

            elif tag_value in ['blood_group', 'religion_id', 'nationality', 'correspondence_country_id', 'category_id']:
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
        logger.info(self.do_mockup(item=GENDER, action_type=self.actionables['C']))
        logger.info(self.do_mockup(item=BLOOD_GROUP, action_type=self.actionables['S']))
        # logger.info(self.do_mockup(item=RELIGION, action_type=self.actionables['S']))
        # logger.info(self.do_mockup(item=NATIONALITY, action_type=self.actionables['S']))
        # logger.info(self.do_mockup(item=CATEGORY_OF_APPLICATION, action_type=self.actionables['S']))
        # logger.info(self.do_mockup(item=FATHERS_NAME, action_type=self.actionables['T']))
        # logger.info(self.do_mockup(item=FATHERS_EMAIL, action_type=self.actionables['T']))
        # logger.info(self.do_mockup(item=FATHERS_PHONE_NUMBER, action_type=self.actionables['T']))
        # logger.info(self.do_mockup(item=FATHERS_OCCUPATION, action_type=self.actionables['T']))
        # logger.info(self.do_mockup(item=MOTHERS_NAME, action_type=self.actionables['T']))
        # logger.info(self.do_mockup(item=MOTHERS_EMAIL, action_type=self.actionables['T']))
        # logger.info(self.do_mockup(item=MOTHERS_PHONE_NUMBER, action_type=self.actionables['T']))
        # logger.info(self.do_mockup(item=MOTHERS_OCCUPATION, action_type=self.actionables['T']))
        # logger.info(self.do_mockup(item=EMERGENCY_PHONE, action_type=self.actionables['T']))
        # logger.info(self.do_mockup(item=AADHAR_NO, action_type=self.actionables['T']))
        # logger.info(self.do_mockup(item=PINCODE, action_type=self.actionables['T']))
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
        # if '&id=3&' in self.apply_link:
        #     logger.info(self.do_mockup(item=JEE_APPEARED, action_type=self.actionables['D']))
        #     logger.info(self.do_mockup(item=STATE_ENTRANCE_APPEARED, action_type=self.actionables['D']))
        #     logger.info(self.do_mockup(item=BTECH_APPEARED, action_type=self.actionables['D']))

    def verify_and_store_data(self):
        tag, name = get_attribute_and_value(item=BLOOD_GROUP, actiontype='verify', )
        status, value = self.ob.search_element_by_name_or_id(main_tag='xpath' if name == 'sex' else 'name', tag_value=name)
        if status:
            logger.info(f"{name} - {value}")

    def do_activity(self):
        self.login()
        self.click_apply()
        self.get_mock_data()
        self.verify_and_store_data()






obj = Admission()
obj.do_activity()
# obj.login()
# ob = SeleniumFactory(url='https://2020admission.giet.edu/admission/index.php?p=login', success_element='left-panel')
# ob.connect()
# print(obj.get_attribute_and_value(item=STATE))



