import random
import shelve
import shutil
import sys
import logging
import logging.config
import os
import json
import tempfile
from contextlib import contextmanager
from utilties.constants import *
from getindianname import male, female
from ast import literal_eval

from utilties.config import get_env

logging.config.fileConfig('logging.conf')
logger = logging.getLogger('helpers')

DATA_DD = dict()


def date_item():
    return f"/html/body/div[3]/table/tbody/tr[{random.randint(1,4)}]/td[{random.randint(1,6)}]"


def get_power(a, b):
    return a ** b


def generate_random_numbers(length):
    number = 0
    if length == '10':  # phone number
        number = str(random.randint(6, 9)) + str(random.randint(100000000, 999999999))
    elif length == '12':  # Aadhar card
        number = str(random.randint(1, 9)) + str(random.randint(10000000000, 99999999999))
    elif length == '4':  # Year of passing
        number = str(random.randint(1990, 2003))
    elif length == '2':  # percentage
        number = str(random.randint(50, 99))
    elif length == '6':  # pincode
        number = str(random.randint(1, 9)) + str(random.randint(10000, 99999))
    return number


def generate_random_strings(length):
    text = 0
    if length == '6':  # Town/Village
        text = ''
    elif length == '40':  # Address
        plotno = str(random.randint(1, 100))
        areano = str(random.randint(1, 100))
        fno = str(random.randint(1, 20))
        text = random.choice([f"PLOT NO, {plotno}, Street no {areano}",
                              f" Floor No: {fno}, House no, {plotno}, Area no {areano}",
                              f" Floor No: {fno}, Building no, {plotno}, Street No {areano}"])
    return text


def get_attribute_and_value(item=None, items=None, name=None, actiontype='default'):
    if actiontype == 'default':
        key = ''.join(list(item.keys()))
        # key = item.keys()
        if isinstance(item[key], list) and len(item[key]) > 0:
            attribute_tag, attribute_name = list(''.join(key).split('-'))
            if attribute_name == 'sex':
                if str(name.split(" ")[0]).endswith(('a', 'i')):
                    attribute_value = item[key][1]
                else:
                    attribute_value = item[key][0]
            else:
                attribute_value = random.choice(item[key])
            return attribute_tag, attribute_name, str(attribute_value)
        else:
            attribute_tag, attribute_name = list(''.join(key).split('-'))
            if item[key] not in ['dynamic', 'radio', 'date', 'male_string', 'female_string', 'submit']:
                length, typeofval = str(item[key]).split('_')
                atrribute_value = generate_random_strings(length) if typeofval == 'string' else \
                    generate_random_numbers(length)
            elif item[key] in ['male_string']:
                atrribute_value = male()
            elif item[key] in ['female_string']:
                atrribute_value = female()
            else:
                atrribute_value = ''
            return attribute_tag, attribute_name, str(atrribute_value)
    else:
        test_dd = list()
        for item in items:
            key = ''.join(list(item.keys()))
            attribute_tag, attribute_name = list(''.join(key).split('-'))
            test_dd.append(attribute_name)
        return test_dd


def get_creds(filedata=None):
    try:
        # datafile = win_cred_file if sys.platform == 'win32' else linux_cred_file
        # for line in open(datafile, 'r'):
        #     if line != '\n':
        #         data_dict = literal_eval(line)
        #         name = data_dict['name']
        #         email = data_dict['email']
        #         password = data_dict['password']
        #         yield name, email, password
        datafile = filedata
        for line in datafile:
            name = line['name']
            email = line['email']
            password = line['password']
            logger.info(f"{name} = {email}")
            yield name, email, password
    except OSError as e:
        logger.critical(f"No file exits error desc - {e}")


def generate_email_identifier():
    email_identifier = random.randint(1, 9999)
    return str(email_identifier)


def generate_email_issuer():
    email_issuer_identifier = random.choice(email_issuers)
    return str(email_issuer_identifier)


def generate_phone_number():
    num = str(random.randint(6, 9)) + str(random.randint(100000000, 999999999))
    return str(num)


def remove_junks(item):
    item.pop(0)
    item.pop(-1)
    if 'test State' in item:
        item.remove('test State')
    return item


def apply_link(streams):
    item = random.choice(streams)
    only_apply_url = item.split('admission/')[1]
    return only_apply_url


def update_dd(dd=None, key=None, value=None):
    dd.update({key: value})
    return dd


def write_mock_data(data_dictionary=None, cached=None):
    try:
        mock_data_file = cached['mock_data_file'] if cached is not None else get_env('mock_data_file')
        if not os.path.exists(mock_data_file):
            with open(mock_data_file, 'w') as writer:
                writer.writelines(json.dumps(data_dictionary, indent=4))
        else:
            with open(mock_data_file, 'a') as writer:
                writer.writelines(json.dumps(data_dictionary, indent=4))
        return "Successfully wrote the data dictionary file"
    except OSError as e:
        logger.exception(f"Error while writing data dictionary {e}")


CACHE_STATE = {}
@contextmanager
def get_temporary_cache(writeback=True):
    cache_dir = tempfile.mkdtemp(prefix='ga')
    shelf_file_path = os.path.join(cache_dir, "cache.shelve")
    shelf = shelve.open(shelf_file_path, writeback=writeback)
    CACHE_STATE["cache"] = shelf
    yield CACHE_STATE["cache"]
    del CACHE_STATE["cache"]
    shelf.close()
    shutil.rmtree(cache_dir)


def get_temp_repo_root_dir():
    temp_root_path = os.path.expanduser(os.path.join("~", "tmp", "temp_data"))
    if not os.path.exists(temp_root_path):
        os.makedirs(temp_root_path)
    return temp_root_path
