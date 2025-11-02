# ca_nhan_2\examples\sample_code.py

def calculate_total(items):
    # Missing docstring - policy violation
    total = 0
    for item in items:
        total = total + item
    return total

# Hardcoded credential - security violation
API_KEY = "sk-1234567890abcdef"

class User:
    # Missing type hints - policy violation
    def __init__(self, name, email):
        self.name = name
        self.email = email
