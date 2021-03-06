import datetime

from django.core.exceptions import ValidationError


def year_validator(value):
    if value > datetime.datetime.now().year:
        raise ValidationError(
            f"{value}' is not a correct year!"
        )
