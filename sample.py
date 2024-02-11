from datetime import datetime

def calculate_age(birthdate):
    # Assuming birthdate is in the format 'YYYY-MM-DD'
    birthdate = datetime.strptime(birthdate, '%Y-%m-%d')
    today = datetime.today()

    # Calculate the difference in years
    age = today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))

    return age

# Example usage with a predefined birthdate
birthdate_example = '1990-01-15'
age = calculate_age(birthdate_example)
print("Age:", age, "years")
