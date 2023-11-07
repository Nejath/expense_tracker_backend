from django.core.exceptions import ValidationError

def validate_password_complexity(password,k):
    if len(password) < 8:
        raise ValidationError("Password must be at least 8 characters long.")
    if not any(char.isupper() for char in password):
        raise ValidationError("Password must contain at least one uppercase letter.")
    if not any(char in "!@#$%^&*()" for char in password):
        raise ValidationError("Password must contain at least one special character (!@#$%^&*()).")