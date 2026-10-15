
print("================================")
print("   PASSWORD STRENGTH ANALYZER")
print("================================")

while True:
    password = input("\nEnter a sample password: ")

    length = len(password)

    has_uppercase = False
    has_lowercase = False
    has_number = False
    has_special = False

    for character in password:
        if character.isupper():
            has_uppercase = True
        if character.islower():
            has_lowercase = True
        if character.isdigit():
            has_number = True
        if not character.isalnum() and not character.isspace():
            has_special = True

    score = 0

    if length >= 8:
        score += 1
    if has_uppercase:
        score += 1
    if has_lowercase:
        score += 1
    if has_number:
        score += 1
    if has_special:
        score += 1

    print("\nPassword length:", length)
    print("Password score:", score, "/ 5")

    if score <= 2:
        print("Password strength: Weak")
    elif score <= 4:
        print("Password strength: Medium")
    else:
        print("Password strength: Strong")

    print("\nSuggestions:")

    if length < 8:
        print("- Use at least 8 characters.")
    if not has_uppercase:
        print("- Add an uppercase letter (A-Z).")
    if not has_lowercase:
        print("- Add a lowercase letter (a-z).")
    if not has_number:
        print("- Add a number (0-9).")
    if not has_special:
        print("- Add a special character, such as @ or #.")
    if score == 5:
        print("All five checks passed!")

    again = input("\nAnalyze another password? (yes/no): ")

    if again.lower() != "yes":
        print("Thank you for using Password Strength Analyzer!")
        break

