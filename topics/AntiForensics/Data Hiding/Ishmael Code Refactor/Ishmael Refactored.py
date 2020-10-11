"""POC for a cipher system that translates 1 char into multiple words
"""
import string as s
import math
import random
from collections import OrderedDict
import base64

# A list of valid characters in base64
base_chars = list(s.ascii_letters + s.digits + "+" + "/" + "=")


# Code below from following site
# https://www.geeksforgeeks.org/break-list-chunks-size-n-python/
def divide_chunks(list_to_chunk, n):
    """Yields successive n-sized chunks from list list_to_chunk

    :param list_to_chunk: (list) A list to be chunked
    :param n: (int) The number of elements to be put into each chunk
    :return: The chunks of equal size using a yield statement
    """

    # Yield each chunk.
    for x in range(0, len(list_to_chunk), n):
        yield list_to_chunk[x:x + n]


# Function for generation the word lists used for encoding.
def wordlistgen():
    """Generates an encode and decode table out of a list of mixed words.

    :return: Two lists, one for encoding, one for decoding.
    """

    # Provide user context for what their input should do
    print(
        "To encode or decode a message a word list is required."
        "A longer list will give better results."
        "If decoding, the same list used to encode, must decode"
    )
    print("Ex. The full text of Moby Dick; or, The Whale")

    # Create the master word list as a set to prevent duplicate words.
    word_list = list()

    # Read the contents of the file and save it to a variable.
    while True:
        try:
            # Prompt user for input
            file_path = input(
                "Please enter the full path (including extension) of your file"
                ": "
            )

            with open(file_path, 'r', encoding='utf-8') as text_file:
                text = text_file.read()
            break
        except FileNotFoundError:
            print("File not found, please ensure the path/filename is correct")

    # Cast all upper case characters to lowercase
    text = text.lower()

    # Split up the line into it's component words
    raw_words = text.split()

    # Create a translate table to remove punctuation
    remove_punctuation = str.maketrans('', '', s.punctuation + "”" + "“" + "—")

    # Use a list comprehension. For each word, strip punctuation
    words = [w.translate(remove_punctuation) for w in raw_words]

    # DEBUG print the contents of raw_words
    # print(word_list)

    # Remove the blank entry that can sometimes be created for the wordlist
    try:
        word_list.remove('')
    except ValueError:
        pass

    # Briefly cast the word list as keys in an ordered dict to remove dupes
    words = list(OrderedDict.fromkeys(words))

    # Determine how many words should be in each chunk.
    words_per_chunk = math.ceil(len(words) / len(base_chars))

    # Call divide_chunks to break the cipher_list into equally sized chunks
    chunked_wordlist = divide_chunks(list(words), words_per_chunk)
    chunked_wordlist = list(chunked_wordlist)

    # Create the encoding table as an empty dictionary
    encode_table = dict()

    # Create an iterator i to track progress through chunked_wordlist
    i = 0

    # Loop through all the characters in valid characters
    for char in base_chars:
        # Selected a chunk as the value for the character
        encode_table[char] = chunked_wordlist[i]

        # Add one to the iterator to get next chunk.
        i += 1

    # Create the decoding table as an empty dictionary
    decode_table = dict()

    # For each word in original dictionary, create a word -> character rel.
    for key in encode_table.keys():
        for word in encode_table[key]:
            decode_table[word] = key

    return encode_table, decode_table


# Prompt user for initial wordlist generation
encrypt_list, decrypt_list = wordlistgen()

# Ask user which function they want to perform
while True:
    print("1. Encode a file")
    print("2. Decode a file")
    print("3. Change wordlist")
    print("4. Quit")

    # Prompt user for a number, handle non number answers.
    try:
        choice = int(input("Please enter your choice: "))
    except ValueError:
        print("Please enter a valid number")
        continue

    # Encode Message
    if choice == 1:

        # Open the file as raw bytecode
        while True:
            try:
                # Prompt user for input filepath.
                encode_path = str(
                    input("Enter the path for the file to be encoded: "))

                with open(encode_path, "rb") as file:
                    file_raw = file.read()
                break
            except FileNotFoundError:
                print("We cannot find a file with that name/path. Try again.")

        # Cast raw byte code to base64 encoded bytecode
        file_base = base64.b64encode(file_raw)

        # Cast base64 bytecode into base64 encoded strings
        base_string = file_base.decode("utf-8")

        # Create a list to store the encoded message.
        ish_list = []

        # Loop through all the characters, include whitespaces
        for character in base_string:
            # For each character, add a random word from all words that are
            # associated with that character to the list.
            ish_list.append(random.choice(encrypt_list[character]))

        # Cast the encoded message back into a string.
        ish_string = ' '.join(ish_list)

        # Prompt user for save
        save_path = str(input("Enter the path to save the encoded data: "))
        print("Saving your encoded message...")

        while True:
            try:
                with open(save_path, "w") as file:
                    file.write(ish_string)
                break
            except FileNotFoundError:
                print("We cannot save using that directory/name. Try again.")

    # Decode Message
    elif choice == 2:
        while True:
            try:
                # Get filepath
                decode_path = str(
                    input("Enter in the file path for file to decode: "))

                with open(decode_path, "r") as file:
                    ish_string = file.read()
                break
            except FileNotFoundError:
                print("We cannot find a file with that name/path. Try again.")

        # Cast the list encoded by ish to a string
        ish_list = ish_string.split(" ")

        # Cast the ish string to a base64 encoded list
        base_list = [decrypt_list[word] for word in ish_list]

        # Cast the base64 encoded list to a base64 encoded string
        base_string = " ".join(base_list)

        # Cast the base64 encoded string to a base64 encoded bytecode
        decode_base = base_string.encode("utf-8")

        # Cast base64 encoded bytecode to raw bytecode for writing
        new_file_base = base64.b64decode(decode_base)

        # Prompt user for filepath and write bytecode
        save_path = str(input("Enter the path to save the file to: "))
        print("Saving your decoded message...")

        while True:
            try:
                with open(save_path, "wb") as file:
                    file.write(new_file_base)
                break
            except FileNotFoundError:
                print("We cannot save using that directory/name. Try again.")

    # Change Wordlist
    elif choice == 3:
        encrypt_list, decrypt_list = wordlistgen()

    # Exit program by breaking main loop
    elif choice == 4:
        break

    # Catch exception where user provides number not associated with a choice
    else:
        print("The entered number does not correspond to a choice.")
