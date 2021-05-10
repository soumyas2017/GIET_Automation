NATIONALITY = {'name-nationality': ['India']}
CATEGORY_OF_APPLICATION = {'name-category_id': ['GENERAL', 'OBC', 'SC', 'ST', 'GENERAL', 'GENERAL', 'GENERAL', 'GENERAL']}
DATE_OF_BIRTH = {'name-date_of_birth': 'date'}
GENDER = {'name-sex': ['M', 'F', 'O']}
BLOOD_GROUP = {'name-blood_group': ['O-', 'O+', 'A-', 'A+', 'B-', 'B+', 'AB-', 'AB+']}
RELIGION = {'name-religion_id': ['Buddhist', 'Christian', 'Hindu', 'Jain', 'Hindu', 'Hindu', 'Hindu', 'Hindu', 'Hindu']}
FATHERS_NAME = {'name-father_name': 'male_string'}
FATHERS_EMAIL = {'name-father_email': 'dynamic'}
MOTHERS_NAME = {'name-mother_name': 'female_string'}
MOTHERS_EMAIL = {'name-mother_email': 'dynamic'}
FATHERS_OCCUPATION = {'name-guardian_occupation': ['Police Officer', 'Doctor', 'Teacher', 'Lecturer', 'Bank Officer', 'Peon', 'Clerk',
                      'Computer Engineer', 'Athlete', 'Businessman', 'Priest', 'Manager', 'Ex-Army Officer']}
MOTHERS_OCCUPATION = {'name-mother_occupation': ['Police Officer', 'Doctor', 'Teacher', 'Lecturer', 'Bank Officer',
                                                 'Peon', 'Clerk', 'Computer Engineer', 'Homemaker', 'Businesswomen',
                                                 'Manager', 'Homemaker', 'Homemaker', 'Homemaker', 'Homemaker',
                                                 'Homemaker', 'Homemaker', 'Homemaker', 'Homemaker', 'Homemaker']}
FATHERS_PHONE_NUMBER = {'name-correspondence_phone': '10_number'}
MOTHERS_PHONE_NUMBER = {'name-permanent_phone': '10_number'}
EMERGENCY_PHONE = {'name-emergency_phone': '10_number'}
AADHAR_NO = {'name-aadhar_no': '12_number'}
CORRESPONDENCE_ADDRESS = {'name-correspondence_st_address': '40_string'}
TOWN_VILLAGE = {'name-correspondence_town': '6_string'}
RESIDENTIAL_AREA = {'name-correspondence_residential_area': ['U', 'R']}
PO = {'name-correspondence_po': 'dynamic'}
PINCODE = {'name-communication_pincode': '6_number'}
COUNTRY = {'name-correspondence_country_id': ['India']}
DISTRICT = {'name-correspondence_district': 'dynamic'}
CITY = {'name-correspondence_city_id': 'dynamic'}
STATE = {'name-correspondence_state_id': 'dynamic'}
SAME_ADDRESS = {'id-same_address': 'radio'}
CLASS_X_BOARD = {'name-madhyamik_board_name': ['ICSE', 'CBSE', 'STATE BOARD']}
CLASS_X_INSTITUTE = {'name-madhyamik_institute': ['HIGH SCHOOL', 'SCHOOL', 'SISHU VIDYA MANDIR', 'BINA PANI SCHOOL',
                                                  'DON BOSCO SCHOOL']}
CLASS_X_PASSING_YEAR = {'name-madhyamik_yop': '4_number'}
CLASS_X_GRADE_PERCENTAGE = {'name-madhyamik_percentage': '2_number'}
SUBMIT = {'name-submit': 'submit'}
JEE_APPEARED = '/html/body/div[1]/div/div[2]/div[2]/form/div[2]/fieldset/table[9]/tbody/tr[2]/td[2]/input[2]'
STATE_ENTRANCE_APPEARED = '/html/body/div[1]/div/div[2]/div[2]/form/div[2]/fieldset/table[9]/tbody/tr[3]/td[2]/input[2]'
BTECH_APPEARED = '/html/body/div[1]/div/div[2]/div[2]/form/div[2]/fieldset/table[9]/tbody/tr[4]/td[2]/input[2]'

# Other constants
email_issuers = ['gmail', 'yahoomail', 'outlook', 'rediffmail']
login_successful_div_element = 'left-panel'
login_failure_div_element = 'red-left'
login_failure_msg = 'Invalid Email or Password!'
login_page_load_wait_duration = 5
post_login_req_wait = 10
