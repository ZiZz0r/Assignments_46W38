def get_a_list_of_numbers():
    """This function takes user input and returns a list of numbers entered by the user. It will keep asking for input until the user types 'end'. If the user enters a non-numeric value, it will raise a ValueError."""
    numbers = []

    while True:
        user_input = input("Enter a number, or type 'end' to stop: ")

        if user_input == "end":
            break
        else:
            try:
                numbers.append(float(user_input))
            except ValueError:
                raise ValueError("Input must be a number or 'end' to stop.")
            
    return numbers


def find_min(list_of_numbers): 
    """This function takes a list of numbers and returns the minimum value found in that list. If the list is empty, it will return None."""
    if len(list_of_numbers) == 0:
        return None
    else:
        minimum = list_of_numbers[0]
        for n in list_of_numbers: #Find the minimum value of numbers in the list, by comparing it to the current minimum value and updating it if a smaller number is found.
            if n < minimum:
                minimum = n
        return minimum


def find_max(list_of_numbers):
    """This function takes a list of numbers and returns the maximum value found in that list. If the list is empty, it will return None."""
    if len(list_of_numbers) == 0:
        return None
    else:
        maximum = list_of_numbers[0]
        for n in list_of_numbers: #Find the maximum value of numbers in the list, by comparing it to the current maximum value and updating it if a larger number is found.
            if n > maximum:
                maximum = n
        return maximum
