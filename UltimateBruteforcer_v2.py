#!/usr/bin/env python
# coding:utf-8
#
# Author:                Wizy
# Date:                  28-01-2019
# Purpose:               Find password from hashes using wordlists
# Prerequisites:         A big wordlist and of course hashes
#
# And now - the fun part :>

import datetime
import argparse
import itertools
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


def hashmethod():

    hash_file = open(h).read()

    for hash in hash_file.split("\n"):
        # find kind of hash is the hash in the has file with the length of it else raise an error message
        lenght = len(hash)
        if lenght == 32:     # MD5
            hashmethod_list.append(1)

        elif lenght == 40:   # sha1
            hashmethod_list.append(2)

        elif lenght == 56:  # sha224
            hashmethod_list.append(3)

        elif lenght == 64:   # sha256
            hashmethod_list.append(4)

        elif lenght == 96:   # sha284
            hashmethod_list.append(5)

        elif lenght == 128:  # sha512
            hashmethod_list.append(6)

        else:
            hashmethod_list.append(0)
            print(" /!\ Invalid Hash: " + hash + " /!\ ")

        hash_list.append(hash)


def wordhasher(hashline,word):

    if hashmethod_list[hashline] == 1:
        hashedguess = hashlib.md5(bytes(word, "utf-8")).hexdigest()
    elif hashmethod_list[hashline] == 2:
        hashedguess = hashlib.sha1(bytes(word, "utf-8")).hexdigest()
    elif hashmethod_list[hashline] == 3:
        hashedguess = hashlib.sha224(bytes(word, "utf-8")).hexdigest()
    elif hashmethod_list[hashline] == 4:
        hashedguess = hashlib.sha256(bytes(word, "utf-8")).hexdigest()
    elif hashmethod_list[hashline] == 5:
        hashedguess = hashlib.sha384(bytes(word, "utf-8")).hexdigest()
    elif hashmethod_list[hashline] == 6:
        hashedguess = hashlib.sha512(bytes(word, "utf-8")).hexdigest()
    else:
        hashedguess = "ERROR"
        parser.error(" /!\ Invalid Hash Line: " + str(hashline + 1) + " /!\ ")  # should QUIT doesnt work now

    return hashedguess


def normal():
    hashline = 0
    i = 0
    word_list = open(w).read()
    l = len(digits_list)

    for word in word_list.split("\n"):

        if args.replace:
            word = replace(word)
        if args.repeat:
            word = word + word
        if args.uppercase:
            word = word.upper()
        if args.title:
            word = word.title()

        savedword = word

        while True:

            # Reset the hash line to line 0 when all hashes have been checked and print the guessed password
            if hashline >= lines_hashfile:
                print(word)
                hashline = 0

                if args.numbers:
                    if i - 1 >= int(l -1):
                        i = 0
                        break
                    else:
                        nd = digits_list[i]
                        i += 1
                        if args.front:
                            word = str(nd) + savedword
                        elif args.extremity:
                            word = str(nd) + savedword + str(nd)
                        else:
                            word = savedword + str(nd)

                else:
                    break

            # Read the next hash in the list
            hash = hash_list[hashline]

            # Check if the word hashed is equal to the hash in file
            if wordhasher(hashline, word) == hash:
                result = word + " Line " + str(hashline + 1) + ": " + hash
                result_list.append(result)

            hashline += 1

    readresult()


def replace(word):
    word = word.replace("e", "3").replace("a", "4").replace("o", "0")

    return word


def dates():
    dates_day = ["1","2","3","4","5","6","7","8","9","01","02","03","04","05","06","07","08","09","10","11","12","13",
                 "14","15","16","17","18","19","20","21","22","23","24","25","26","27","28","29","30","31"]
    dates_month = ["1","2","3","4","5","6","7","8","9","01","02","03","04","05","06","07","08","09","10","11","12"]
    dates = []
    for days, month in itertools.product(dates_day, dates_month):
        dates.append(days+month)

    for years in range(1875,2020):
        dates.append(years)

    return dates


def numbers(number_digits):
    i = 0
    digits_list = []

    while i <= int(number_digits):
        n = str(i)
        digits_list.append(n)
        i += 1

    print(digits_list)
    return digits_list


def readresult():

    end_time = datetime.datetime.now()
    print("Time taken: -{" + str(end_time - start_time) + "}-")

    if not result_list:
        print("No Password Found")
        print(result_list)
    else:
        for a in result_list:
            print(a)
            if args.save:
                s = open(save, "a")
                s.write(str(result_list))


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description="Ultimate Sha1/256/512 and MD5 hashes Bruteforcer with dictionaries",
                                     prog="UltimateBrutforcer",
                                     usage="%(prog)s.py <your_wordlist.txt> <your_hashlist.txt> -option1 etc...")

    parser.add_argument("wordlist", help="The wordlist you wish to use.(Example: wordlist.txt)", type=str)
    parser.add_argument("hashlist", help="The hashlist you wish to find the password.(Example: hashlist.txt)", type=str)
    parser.add_argument("-n", "--numbers",default=False, dest="numbers", action="store_true",
                        help="Put numbers at the end of each word")
    parser.add_argument("--common", default=False, dest="common", action="store_true",
                        help="Use most common number used in password only")
    parser.add_argument("--dates", default=False, dest="dates", action="store_true",
                        help="Use all possible dates")

    parser.add_argument("--fr", default=False, dest="front", action="store_true",
                        help="Change the numbers to be at the beggining of the word")
    parser.add_argument("--ex", default=False, dest="extremity", action="store_true",
                        help="Change the numbers to be at the extremity of the word")

    parser.add_argument("-r", "--replace", default=False, dest="replace", action="store_true",
                        help="Replace every E by 3, every A by 4, and every = O by 0(zéro)")
    parser.add_argument("-p", "--repeat", default=False, dest="repeat", action="store_true",
                        help="repeat the word two times")
    parser.add_argument("-u", "--upper", default=False, dest="uppercase", action="store_true",
                        help="Change the word in uppercase")
    parser.add_argument("-t", "--title", default=False, dest="title", action="store_true",
                        help="Write the word as a title, ex: title word -> Title Word")

    parser.add_argument("-s", "--save", default=False, dest="save", action="store_true",
                        help="Save the results in a text file.")

    args = parser.parse_args()
    if args.front and not args.numbers:
        parser.error('-n is required when --front is set.')
    if args.extremity and not args.numbers:
        parser.error('-n is required when --front is set.')
    if args.common and not args.numbers:
        parser.error('-n is required when --common or -c is set.')
    if args.extremity and args. front:
        parser.error('you cannot put those two option to -n')
    if args.common and not args.dates:
        parser.error('you cannot put those two option to -n.')

    w = args.wordlist
    h = args.hashlist
    lines_hashfile = countlines_hashfile()
    lines_wordfile = countlines_wordfile()
    result_list = []
    hashmethod_list = []
    hash_list = []
    digits_list = []

    if args.numbers:
        if args.common:
            digits_list = ["1", "12", "123", "1234", "12345", "123456", "1234567", "12345678", "123456789", "00", "01",
                           "10", "11", "13", "19","22", "23", "42", "69", "77", "99", "314", "666", "777", "111",
                           "100", "200", ]
        elif args.dates:
            digits_list = dates()

        else:
            while True:

                number_digits = input("How many numbers do you want to put"
                                      "(/!\max is 6 numbers!\)")
                if number_digits.isdigit() and int(number_digits) <= 6:
                    number_digits = "9" * int(number_digits)
                    print(number_digits)
                    digits_list = numbers(number_digits)
                    break
                else:
                    parser.error('A number lower or equal to 6 is required for the lenght of the numbers')

    if args.save:
        run = True
        while run:
            save = input("How do you want to name the save file?")
            if save != "":
                save = save+".txt"
                break

    print("\n" + "-Found [" + str(lines_hashfile) + "] hashes in hashlist " +
          "\n" + "-Found [" + str(lines_wordfile) + "] words in wordlist")

    hashmethod()

    input("\n"+"Press <ENTER> to start")

    start_time = datetime.datetime.now()  # Save the time the program started

    main()

    print("Scan finished")
