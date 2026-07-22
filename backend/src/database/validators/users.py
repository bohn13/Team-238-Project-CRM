import re

import email_validator


PHONE_NUMBER_PATTERN = r"^\+[1-9]\d{7,14}$"


def validate_password_strength(password: str) -> str:
    if len(password) < 8:
        raise ValueError("Password must contain at least 8 characters.")
    if not re.search(r"[A-Z]", password):
        raise ValueError("Password must contain at least one uppercase letter.")
    if not re.search(r"[a-z]", password):
        raise ValueError("Password must contain at least one lower letter.")
    if not re.search(r"\d", password):
        raise ValueError("Password must contain at least one digit.")
    if not re.search(r"[@$!%*?&#]", password):
        raise ValueError(
            "Password must contain at least one special character: @, $, !, %, *, ?, #, &."
        )
    return password


def validate_email(user_email: str) -> str:
    try:
        email_info = email_validator.validate_email(
            user_email, check_deliverability=False
        )
    except email_validator.EmailNotValidError as error:
        raise ValueError(str(error)) from error
    return email_info.normalized


def normalize_phone_number(phone_number: str) -> str:
    normalized_phone_number = re.sub(r"[\s()-]", "", phone_number)
    if not re.fullmatch(PHONE_NUMBER_PATTERN, normalized_phone_number):
        raise ValueError(
            "Phone number must be in international E.164 format, "
            "for example +380501112233."
        )
    return normalized_phone_number
