from django.core.validators import RegexValidator

alphanumeric = RegexValidator(
    r"^[0-9a-zA-Ζ ]*$", "Only alphanumeric characters are allowed."
)
alphabetic = RegexValidator(
    r"^[a-zA-Z ]*$", "Only alphabetic characters are allowed."
)
