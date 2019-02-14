#!/usr/bin/env python
# coding:utf-8
import datetime
import argparse
from urllib.request import hashlib


def main():
    normal()


def countlines_hashfile():
    with open(h) as myfile:
        count = sum(1 for line in myfile)
        return count


def countlines_wordfile():
    with open(w) as myfile:
        count2 = sum(1 for line in myfile)
        return count2


def hashmethod(hash_list, word, hashline):

    # find kind of hash is the hash in the has file with the length of it else raise an error message
    if len(hash_list) == 32:     # MD5
        hashedguess = hashlib.md5(bytes(word, "utf-8")).hexdigest()

    elif len(hash_list) == 40:   # sha1
        hashedguess = hashlib.sha1(bytes(word, "utf-8")).hexdigest()

    elif len(hash_list) == 56:  # sha224
        hashedguess = hashlib.sha224(bytes(word, "utf-8")).hexdigest()

    elif len(hash_list) == 64:   # sha256
        hashedguess = hashlib.sha256(bytes(word, "utf-8")).hexdigest()

    elif len(hash_list) == 96:   # sha284
        hashedguess = hashlib.sha384(bytes(word, "utf-8")).hexdigest()

    elif len(hash_list) == 128:  # sha512
        hashedguess = hashlib.sha512(bytes(word, "utf-8")).hexdigest()

    else:
        hashedguess = (" /!\ Invalid Hash Line: " + str(hashline + 1) + hash_list + " /!\ ")
    return hashedguess


def normal():
    hashline = 0
    i = 0
    word_list = open(w).read()

    for word in word_list.split("\n"):

        savedword = word
        if args.replace:
            word = replace(word)

        while True:

            # Reset the hash line to line 0 when all hashes have been checked and print the guessed password
            if hashline >= lines_hashfile:
                print("Password guess", word)
                hashline = 0

                if args.digits:
                    if i + 1 >= int(digits_list[-1]):
                        i = 0
                        break
                    else:
                        i += 1
                        nd = digits_list[i]
                        if args.front:
                            word = str(nd) + savedword
                        else:
                            word = savedword + str(nd)

                else:
                    break

            # Read the next hash in the list
            hash_list = open(h).readlines()[hashline]
            hash_list = "".join(hash_list)
            hash_list = hash_list.strip("\n")

            # Check if the word hashed is equal to the hash in file
            if hashmethod(hash_list, word, hashline) == hash_list:
                result = " Password found: " + word + " Line " + str(hashline + 1) + ": " + hash_list
                result_list.append(result)

            hashline += 1

    readresult()


def replace(word):
    word = word.replace("e", "3")
    word = word.replace("a", "4")
    word = word.replace("o", "0")
    return word


def digits(m):
    i = 0
    digits_list = []
    while i < int(m):
        i += 1
        n = str(i)
        digits_list.append(n)

    print(digits_list)
    return digits_list


def readresult():
    if not result_list:
        print("No Password Found")
        print(result_list)
    else:
        for a in result_list:
            print(a)
        end_time = datetime.datetime.now()
        print("Time taken: -{" + str(end_time - start_time) + "}-")


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description="Ultimate Sha1/256/512 and MD5 hashes Bruteforcer with dictionaries by Wizy",
                                     prog="UltimateBrutforcer",
                                     usage="%(prog)s.py <your_wordlist.txt> <your_hashlist.txt> -option1 etc...")

    parser.add_argument("wordlist", help="The wordlist you wish to use.(Example: wordlist.txt)", type=str)
    parser.add_argument("hashlist", help="The hashlist you wish to find the password.(Example: hashlist.txt)", type=str)
    parser.add_argument("-d", "--digits",default=False, dest="digits", action="store_true",
                        help="Put digits at the end of each word")

    parser.add_argument("--front", default=False, dest="front", action="store_true",
                        help="Change the digits to be at the beggining of the word")

    parser.add_argument("-r", "--replace", default=False, dest="replace", action="store_true")
    args = parser.parse_args()

    if args.front and not args.digits:
        parser.error('-d is required when --front is set.')

    w = args.wordlist
    h = args.hashlist
    lines_hashfile = countlines_hashfile()
    lines_wordfile = countlines_wordfile()
    result_list = []

    if args.digits:
        number_digits = input("How many digits do you want to put"
                              "(/!\If you put to many digits it's going to take ages/!\)")
        if number_digits.isdigit():
            m = "9" * int(number_digits)
            digits_list = digits(m)
        else:
            parser.error('A number is required for the lenght of the digits')

    print("Found " + str(lines_hashfile) + " hashes in hashlist and " + str(lines_wordfile) +
          " words in wordlist")

    input("Press <ENTER> to start")

    start_time = datetime.datetime.now()  # Save the time the program started

    main()

    print("Over")
