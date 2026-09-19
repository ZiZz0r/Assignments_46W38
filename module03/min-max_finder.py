"""This program takes numbers as input from the user and finds the minimum and maximum values among them. 
The user can enter as many numbers as they want, and they can type 'end' to stop entering numbers.
It will display the list of numbers entered, as well as the minimum and maximum values found."""

numbers = []

while True:
    user_input = input("Enter a number, or type 'end' to stop: ") #Input any numbers you want to sort

    if user_input == "end":
        break
    else:
        numbers.append(float(user_input))

if len(numbers) == 0:
    minimum = None
    maximum = None
else:
    minimum = numbers[0]
    maximum = numbers[0]

    for n in numbers: #Find the minimum and maximum values of numbers in the list
        if n < minimum:
            minimum = n
        if n > maximum:
            maximum = n

print(f"The list of numbers is: {numbers}")
print(f"The minimum number is: {minimum}")
print(f"The maximum number is: {maximum}")