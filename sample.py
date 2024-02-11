def generate_username(first_name, last_name, middle_name=None):
    username = ""

    # Add the first letter of the first name
    if first_name:
        username += first_name[0].lower()

    # Add the first letter of the middle name if available
    if middle_name:
        username += middle_name[0].lower()

    # Add the first letter of the last name if available
    if last_name:
        username += last_name[0].lower()

    return username

# Example usage:
first_name = "John"
middle_name = "Robert"
last_name = "Doe"

username = generate_username(first_name, last_name, middle_name)
print(username)
