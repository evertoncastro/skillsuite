from email_validator import validate_email, EmailNotValidError


def is_valid_email(email):
    try:
        valid = validate_email(email)
        return valid is not None
    except EmailNotValidError:
        return False
