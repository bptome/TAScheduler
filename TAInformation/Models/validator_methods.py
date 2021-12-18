# Validator Method Module by: Terence Lee (12/17/2021)

from TAInformation.Models.base_user import BaseUser
from curses.ascii import isupper, islower, isdigit
from django.core.exceptions import ValidationError
from django.core.validators import validate_email

# Data validating methods module
# For all methods:
# Pre: Argument passed is derived from BaseUser
# Post: Returns dict object that indicates result of validation and error message, if needed
from TAInformation.models import User, Skill


def id_validator(new_user):
    if (not isinstance(new_user.user_id, int)) or new_user.user_id < 0:
        return {'result': False, 'errorMsg': "Invalid user id entered\n"}

    return {'result': True, 'errorMsg': ""}


def name_validator(new_user):
    if len(new_user.name) < 5:
        return {'result': False, 'errorMsg': "Invalid name given\n"}

    return {'result': True, 'errorMsg': ""}


def password_validator(new_user):
    if len(new_user.password) < 4:
        return {'result': True, 'errorMsg': "Password must be at least 4 characters long\n"}

    uppercase_missing = True
    lowercase_missing = True
    number_missing = True
    special_char_missing = True

    # Loop to check if password format is correct
    for c in new_user.password:
        if isupper(c):
            uppercase_missing = False
        elif islower(c):
            lowercase_missing = False
        elif isdigit(c):
            number_missing = False
        else:
            special_char_missing = False

    error_msg = ""
    if uppercase_missing:
        error_msg += "Password must contain >= 1 uppercase letter\n"

    if lowercase_missing:
        error_msg += "Password must contain >= 1 lowercase letter\n"

    if number_missing:
        error_msg += "Password must contain >= 1 number\n"

    if special_char_missing:
        error_msg += "Password must contain >= 1 non-alphanumeric character\n"

    if error_msg != "":
        return {'result': False, 'errorMsg': error_msg}

    return {'result': True, 'errorMsg': ""}


def email_validator(new_user):
    try:
        validate_email(new_user.email)
    except ValidationError as errorMsg:
        error_msg = errorMsg.message + " "
        return {'result': False, 'errorMsg': error_msg}

    return {'result': True, 'errorMsg': ""}


def address_validator(new_user):
    if new_user.home_address == "":
        return {'result': False, 'errorMsg': "Home address is missing\n"}

    address_no_whitespace: str = new_user.home_address.replace(" ", "")
    if address_no_whitespace == "":
        return {'result': False, 'errorMsg': "Home address must contain some non-space characters\n"}

    return {'result': True, 'errorMsg': ""}


def phone_validator(new_user):
    if new_user.phone == "":
        return {'result': False, 'errorMsg': "No phone number given\n"}
    if len(new_user.phone) != 13:
        return {'result': False, 'errorMsg': "Phone number should have exactly 13 characters\n"}

    char_set = {0, 4, 8}
    digit_set = set(range(13)) - char_set

    for index in range(13):
        if index in digit_set and not isdigit(new_user.phone[index]):
            return {'result': False, 'errorMsg': "Misplaced character in phone number entry\n"}

        if index == 0 and new_user.phone[0] != '(':
            return {'result': False, 'errorMsg': "Missing lead parentheses in phone number entry\n"}

        if index == 4 and new_user.phone[4] != ')':
            return {'result': False, 'errorMsg': "Missing trailing parentheses in phone number entry\n"}

        if index == 8 and new_user.phone[8] != '-':
            return {'result': False, 'errorMsg': "Missing dash between prefix and suffix in phone number entry\n"}

    return {'result': True, 'errorMsg': ""}


def save_new_user(new_user: BaseUser):
    user_to_save = User(user_id=new_user.user_id, name=new_user.name, password=new_user.password,
                        email=new_user.email, home_address=new_user.home_address, phone=new_user.phone,
                        role=new_user.role.value)
    user_to_save.save()


def build_error_message(new_user: BaseUser) -> str:
    return_dict = {}

    return_dict = id_validator(new_user)
    error_msg = return_dict['errorMsg']

    return_dict = name_validator(new_user)
    error_msg += return_dict['errorMsg']

    return_dict = password_validator(new_user)
    error_msg += return_dict['errorMsg']

    return_dict = email_validator(new_user)
    error_msg += return_dict['errorMsg']

    return_dict = address_validator(new_user)
    error_msg += return_dict['errorMsg']

    return_dict = phone_validator(new_user)
    error_msg += return_dict['errorMsg']

    return error_msg


def all_tests_setup(test_user, id_number: int, name: str, password: str, email: str, address: str, phone: str):
    test_user.user_id = id_number
    test_user.name = name
    test_user.password = password
    test_user.email = email
    test_user.home_address = address
    test_user.phone = phone


# Functions to setup database before all tests
def setup_database(test_user: BaseUser, test_user_model: User):
    all_tests_setup(test_user_model, test_user.user_id, test_user.name, test_user.password, test_user.email,
                    test_user.home_address, test_user.phone)

    skill_collection = {}
    skill_to_add = Skill()
    for skill in test_user.skills:
        if skill not in skill_collection:
            skill_collection[skill] = 1
        else:
            skill_collection[skill] += 1

        skill_to_add.name = skill
        skill_to_add.count = skill_collection[skill]
        skill_to_add.save()
        test_user_model.skills.add(skill)

    test_user_model.save()
