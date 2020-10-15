"""Commandline Only Version of Ishmael"""
import string as s
import math
import random
from collections import OrderedDict
import base64
import argparse


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


def wordlistgen(file_path):
    """Generates an encode and decode table out of a list of mixed words

    :param file_path: (str) filepath for the base wordlist to be used.
    :return:  Two lists, one for encoding, one for decoding.
    """

    # Create the master word list as a set to prevent duplicate words.
    word_list = list()

    # Open the wordlist and read it's contents into the variable 'text'
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()

        # Cast all upper case characters to lowercase
        text = text.lower()

        # Split up the line into it's component words
        raw_words = text.split()

        # Create a translate table to remove punctuation
        remove_punctuation = str.maketrans('', '',
                                           s.punctuation + "”" + "“" + "—")

        # Use a list comprehension. For each word, strip punctuation
        words = [w.translate(remove_punctuation) for w in raw_words]

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


def encrypt(encrypt_list, file_path, save_path):
    """Function to encrypt a file using ish.

    :param encrypt_list: (dict) The wordlist translation table from wordlistgen
    :param file_path: The filepath for the file to be encrypted
    :param save_path: The filepath for the encrypted file to be saved to

    :return: Nothing, just saves encrypted file.
    """

    # Open the file to be encrypted as bytecode.
    with open(file_path, 'rb') as file:
        file_raw = file.read()

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

    # Save the resulting file.
    with open(save_path, "w") as file:
        file.write(ish_string)


def decrypt(decrypt_list, file_path, save_path):
    """Function to decrypt a file using ish.

    :param decrypt_list: (dict) the wordlist translation table from wordlistgen
    :param file_path: The filepath for the file to be decrypted
    :param save_path: The filepath for the decrypted file to be saved to.

    :return: Nothing, just saves decrypted file.
    """

    # Open filepath to decrypt and save contents as ish_string.
    with open(file_path, "r") as file:
        ish_string = file.read()

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

    # Write new_file_base to file.
    with open(save_path, "wb") as file:
        file.write(new_file_base)


def main():
    """Main function

    :return: Nothing, just runs the program.
    """

    # Create the arg parser
    parser = argparse.ArgumentParser(description="Process arguments for ish "
                                                 "modes.")

    # Defining encryption argument for parser
    parser.add_argument("-e", "--encrypt", type=str, nargs=3,
                        metavar=('encrypt_path', 'file_path', 'save_path'),
                        default=None,
                        help="Encrypt file at file_path using wordlist at "
                             "encrypt_path. Save results to save_path.")

    # Defining decryption argument for parser
    parser.add_argument("-d", "--decrypt", type=str, nargs=3,
                        metavar=('decrypt_path', 'file_path', 'save_path'),
                        default=None,
                        help="Decrypt file at file_path using wordlist at "
                             "decrypt_path. Save results to save_path.")

    # Parse the arguments from standard input
    args = parser.parse_args()

    if args.encrypt:
        encryptlist, decryptlist = wordlistgen(args[0])
        encrypt(encryptlist, args[1], args[2])
    elif args.decrypt:
        encryptlist, decryptlist = wordlistgen(args[0])
        decrypt(decryptlist, args[1], args[2])


if __name__ == "__main__":
    # Calling the main function
    main()
