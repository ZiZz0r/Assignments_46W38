import string


def count_words(filename):
    """Count the number of words in a file."""
    try:
        with open(filename, "r", encoding="utf-8") as file:
            text = file.read()
    except FileNotFoundError:
        return None

    # Remove punctuation from the text and split it into words.
    for punctuation in string.punctuation:
        text = text.replace(punctuation, "")

    words = text.split()
    return len(words)


# Show an example of how to use the count_words function.
filename = "The_Zen_of_Python.txt"
word_count = count_words(filename)

print(f"The file '{filename}' contains {word_count} words.")