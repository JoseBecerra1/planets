# Define a dictionary to store bugs based on the number of legs
bug_legs = {
    "No legs": [],
    "2 legs": [],
    "4 legs": [],
    "6 legs": [],
    "More than 6 legs": []
}

# Input bug names and the number of legs
while True:
    bug_name = input("Enter the name of a bug (or 'done' to finish): ")
    if bug_name.lower() == 'done':
        break

    leg_count = int(input(f"How many legs does {bug_name} have? "))

    # Categorize the bug based on the number of legs
    if leg_count == 0:
        bug_legs["No legs"].append(bug_name)
    elif leg_count == 2:
        bug_legs["2 legs"].append(bug_name)
    elif leg_count == 4:
        bug_legs["4 legs"].append(bug_name)
    elif leg_count == 6:
        bug_legs["6 legs"].append(bug_name)
    else:
        bug_legs["More than 6 legs"].append(bug_name)

# Display the categorized bugs
for category, bugs in bug_legs.items():
    if bugs:
        print(f"{category}: {', '.join(bugs)}")

