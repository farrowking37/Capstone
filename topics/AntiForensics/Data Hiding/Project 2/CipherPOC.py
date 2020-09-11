"""POC for a cipher system that translates 1 char into multiple words
"""
import string as s
import math
import random
from collections import OrderedDict
import base64

# A list of valid characters for ascii encoding
ascii_chars = list(s.ascii_letters + s.whitespace + s.punctuation + s.digits)

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
	"""Generates a list of unique words when passed a list of mixed words

	:return: A list of unique words in order of appearance in original list
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
				"Please enter the full path (including extension) of your file: "
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

	return words


# Ask user which function they want to perform
while True:
	print("1. Encode a text message")
	print("2. Decode a text message")
	print("3. Encode a file")
	print("4. Decode a file")
	print("5. Quit")

	# Prompt user for a number, handle non number answers.
	try:
		choice = int(input("Please enter your choice: "))
	except ValueError:
		print("Please enter a valid number")
		continue

	# Encode message
	if choice == 1:
		# Call wordlistgen() to generate the word list needed for cipher
		cipher_list = wordlistgen()

		message = str(input("Please enter in the message to be encoded: "))

		# Determine how many words should be in each chunk.
		words_per_chunk = math.ceil(len(cipher_list) / len(ascii_chars))

		# Call divide_chunks to break the cipher_list into equally sized chunks
		chunked_wordlist = divide_chunks(list(cipher_list), words_per_chunk)
		chunked_wordlist = list(chunked_wordlist)

		# Create the encoding table as an empty dictionary
		encode_table = dict()

		# Create an iterator i to track progress through chunked_wordlist
		i = 0

		# Loop through all the characters in valid characters
		for character in ascii_chars:

			# Selected a chunk as the value for the character
			encode_table[character] = chunked_wordlist[i]

			# Add one to the iterator to get next chunk.
			i += 1

		# Create a list to store the encoded message.
		encoded_message = []

		# Loop through all the characters, include whitespaces
		for character in list(message):

			# For each character, add a random word from all words that are
			# associated with that character to the list.
			encoded_message.append(random.choice(encode_table[character]))

		# Cast the encoded message back into a string.
		encoded_message = ' '.join(encoded_message)

		print("Your encoded message is....")
		print(encoded_message)

	# Decode message
	elif choice == 2:
		print(
			"You must use the same wordlist to decode that you used to encode."
		)
		decode_list = wordlistgen()

		cipher_text = str(input("Enter in your cipher text: "))

		# TODO Make this chunk of code into a function
		# Determine how many words should be in each chunk.
		words_per_chunk = math.ceil(len(decode_list) / len(ascii_chars))

		# Call divide_chunks to break the cipher_list into equally sized chunks
		chunked_wordlist = divide_chunks(list(decode_list), words_per_chunk)
		chunked_wordlist = list(chunked_wordlist)

		# Create the encoding table as an empty dictionary
		association_table = dict()

		# Create an iterator i to track progress through chunked_wordlist
		i = 0

		# Loop through all the characters in valid characters
		for character in ascii_chars:
			# Selected a chunk as the value for the character
			association_table[character] = chunked_wordlist[i]

			# Add one to the iterator to get next chunk.
			i += 1

		decode_table = dict()

		for key in association_table.keys():
			for word in association_table[key]:
				decode_table[word] = key

		cipher_text = cipher_text.split(" ")

		message = [decode_table[word] for word in cipher_text]
		print("Your decoded message is...")
		print(''.join(message))

	# Encode Message
	elif choice == 3:

		# Prompt user for filepath where file to be translated is located
		encode_path = str(input("Enter the path for the file to be encoded: "))

		# Open the file as raw bytecode
		with open(encode_path, "rb") as file:
			file_raw = file.read()

		# Cast raw byte code to base64 encoded bytecode
		file_base = base64.b64encode(file_raw)

		# Cast base64 bytecode into base64 encoded strings
		base_string = file_base.decode("utf-8")

		# Call wordlistgen() to generate the word list needed for cipher
		cipher_list = wordlistgen()

		# Determine how many words should be in each chunk.
		words_per_chunk = math.ceil(len(cipher_list) / len(base_chars))

		# Call divide_chunks to break the cipher_list into equally sized chunks
		chunked_wordlist = divide_chunks(list(cipher_list), words_per_chunk)
		chunked_wordlist = list(chunked_wordlist)

		# Create the encoding table as an empty dictionary
		encode_table = dict()

		# Create an iterator i to track progress through chunked_wordlist
		i = 0

		# Loop through all the characters in valid characters
		for character in base_chars:
			# Selected a chunk as the value for the character
			encode_table[character] = chunked_wordlist[i]

			# Add one to the iterator to get next chunk.
			i += 1

		# Create a list to store the encoded message.
		ish_list = []

		# Loop through all the characters, include whitespaces
		for character in base_string:
			# For each character, add a random word from all words that are
			# associated with that character to the list.
			ish_list.append(random.choice(encode_table[character]))

		# Cast the encoded message back into a string.
		ish_string = ' '.join(ish_list)

		# Prompt user for save
		save_path = str(input("Enter the path to save the encoded data: "))
		print("Saving your encoded message...")
		with open(save_path, "w") as file:
			file.write(ish_string)

	# Decode Message
	elif choice == 4:

		# Generate a wordlist used to decode the text
		decode_list = wordlistgen()

		# Get filepath
		decode_path = str(input("Enter in the file path for file to decode: "))
		with open(decode_path, "r") as file:
			ish_string = file.read()

		# TODO Make this chunk of code into a function
		# Determine how many words should be in each chunk.
		words_per_chunk = math.ceil(len(decode_list) / len(base_chars))

		# Call divide_chunks to break the cipher_list into equally sized chunks
		chunked_wordlist = divide_chunks(list(decode_list), words_per_chunk)
		chunked_wordlist = list(chunked_wordlist)

		# Create the encoding table as an empty dictionary
		association_table = dict()

		# Create an iterator i to track progress through chunked_wordlist
		i = 0

		# Loop through all the characters in valid characters
		for character in base_chars:
			# Selected a chunk as the value for the character
			association_table[character] = chunked_wordlist[i]

			# Add one to the iterator to get next chunk.
			i += 1

		# Create a dictionary to use to decode
		decode_table = dict()

		# For each word in original dictionary, create a word -> character rel.
		for key in association_table.keys():
			for word in association_table[key]:
				decode_table[word] = key

		# Cast the list encoded by ish to a string
		ish_list = ish_string.split(" ")

		# Cast the ish string to a base64 encoded list
		base_list = [decode_table[word] for word in ish_list]

		# Cast the base64 encoded list to a base64 encoded string
		base_string = " ".join(base_list)

		# Cast the base64 encoded string to a base64 encoded bytecode
		decode_base = base_string.encode("utf-8")

		# Cast base64 encoded bytecode to raw bytecode for writing
		new_file_base = base64.b64decode(decode_base)

		# Prompt user for filepath and write bytecode
		save_path = str(input("Enter the path to save the file to: "))
		print("Saving your decoded message...")
		with open(save_path, "wb") as file:
			file.write(new_file_base)

	# Exit program by breaking main loop
	elif choice == 5:
		break

	# Catch exception where user provides number not associated with a choice
	else:
		print("The entered number does not correspond to a choice.")
