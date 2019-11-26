#!/usr/bin/env python
# coding:utf-8
#
# Author:                Thewizy
# Date:                  Project Started 28-01-2019 | Last update 26-11-2019
# Purpose:               Find password from hashes using wordlists
# Prerequisites:         A big wordlist and of course hashes
#
# And now - the fun part :>

import datetime
import argparse
import itertools
import string
import hashlib
import secrets
import time
import sys
import os


def main():
    if args.brut:
        bruteforce()
    else:
        normal()


def countlines_hashfile():
    # count lines in hashfile
    with open(h) as myfile:
        count = sum(1 for line in myfile)
        return count


def countlines_wordfile():
    # count lines in wordfile
    with open(w) as myfile:
        count2 = sum(1 for line in myfile)
        return count2


def hashmethod():
    # find hash algorythms of hashes in hashfile with the length of it else raise an error message
    i = 0
    hash_file = open(h).read()

    for hash in hash_file.split("\n"):
        lenght = len(hash)
        i += 1
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

        hash_list.append(hash)


def wordhasher(word,hashline):
    # hash words depending on the hash algorythm with leght of the hash found in hashmethod()
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
        result_list.append(+" /!\ Invalid Hash Line: " + str(hashline + 1) + " /!\ ")

    return hashedguess


def numberToBase(n, b):  # converts number N base 10 to a list of digits base b
    # all characters possibilities generator
    digits = []
    while n:
        digits.append(int(n % b))
        n //= b
    return digits[::-1]


def passwordgenerator(password_length):
    # random password generator
    mypw = ""
    alphabet_number = "abcdefghijklmnopqrstuvwxyz0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    symbols = "!?@%#$"

    for i in range(password_length):

        #  Random number in range [0,3] 1 chance out of n for every char
        #  numbers can be added to lower the % of symbols
        symbolprint = int(secrets.choice("012345"))
        if symbolprint == 3:

            # pick a random symbol everytime symbolprint == 3 and add it to the password
            new_symbols = secrets.choice(symbols)
            mypw = mypw + new_symbols

        else:

            # pick a random number or letter and add it to the pw
            new_alphabetnumber = secrets.choice(alphabet_number)
            mypw = mypw + new_alphabetnumber

    return mypw


def bruteforce():

    bf_random, random = bruteforce_options()

    # bruteforce algorythms
    hashline = 0
    chars = list(string.printable)[:95]
    base = len(chars)
    n = 1
    word = ""
    solved = False
    while not solved:

        if hashline >= lines_hashfile:
            hashline = 0
            lst = numberToBase(n, base)
            word = ''
            if bf_random:
                word = passwordgenerator(random)
            else:
                for x in lst:
                    word += str(chars[x])
                    n += 1
            if args.show:
                print("[" + RED + "-" + WHITE + "]" + BLUE +"Trying word: " + YELLOW + word + WHITE)
        hash = hash_list[hashline]

        if wordhasher(word, hashline) == hash:
            result = ("[" + GREEN + "+" + WHITE + "]" + "Hash: " + hash + " | Found at line " + BLUE + str(
                    hashline + 1) + WHITE + " matched word: " + YELLOW + word + WHITE)
            result_list.append(result)
            if args.prog:
                input(result)

        hashline += 1


def bruteforce_options():
    # bruteforce menu
    bf_random = False
    random = 0
    print(GREEN + "{-----BRUTEFORCE MODE-----} " + WHITE)
    print("[" + YELLOW + "1" + WHITE + "]" + BLUE + " Random Passwords" + WHITE)
    print("[" + YELLOW + "2" + WHITE + "]" + BLUE + " All Possibilities" + WHITE)
    print("[" + YELLOW + "3" + WHITE + "]" + BLUE + " Exit" + WHITE)
    option = int(input(GREEN + "=====>" + WHITE))
    if option == 1:
        bf_random = True
        random = int(input("How many characters does the randomized passwords need to have? "))
        if random < 0:
            print("You need to input a positive number")
    elif option == 2:
        bf_random = False
    else:
        os.system("cls")
        quit()

    # animation
    starting("bruteforce")

    return bf_random, random


def normal():
    hashline = 0
    i = 0
    word_list = open(w).read()

    # number options
    if args.numbers:
        digits_list = number_options()

    if args.word:
        replaceword, repeat, upper, title, addword = word_options()
        if addword:
            word2 = input("Word to add:")
        else:
            word2 = ""
    # animation
    starting("")
    # set start time
    start_time = datetime.datetime.now()  # Save the time the program started

    # change the word depending on the options
    for word in word_list.split("\n"):
        if args.word:
            if repeat:
                word = word + word
            if replaceword:
                word = replace(word)
            if upper:
                word = word.upper()
            if title:
                word = word.title()
            if addword:
                if args.front:
                    word = word2 + word
                elif args.extremity:
                    word = word2 + word + word2
                else:
                    word = word + word2

        savedword = word

        while True:

            # Reset the hash line to line 0 when all hashes have been checked and print the guessed password
            if hashline >= lines_hashfile:
                hashline = 0
                if args.show:
                    print("[" + RED + "-" + WHITE + "]" + BLUE +"Trying word: " + YELLOW + word + WHITE)
                if args.numbers:
                    l = len(digits_list)
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

            # Check if the word hashed is equal to the hash in file with wordhasher()

            if wordhasher(word,hashline) == hash:
                result = ("[" + GREEN + "+" + WHITE + "]" + "Hash: " + hash + " | Found at line " + BLUE + str(
                    hashline + 1) + WHITE + " matched word: " + YELLOW + word + WHITE)
                result_list.append(result)
                if args.prog:
                    input(result)

            hashline += 1
    end_time = datetime.datetime.now()
    readresult(end_time)


def number_options():
    print(GREEN + "{-----NUMBERS OPTIONS-----} " + WHITE)
    print("[" + YELLOW + "1" + WHITE + "]" + BLUE + " Use 0-9x[length] numbers" + WHITE)
    print("[" + YELLOW + "2" + WHITE + "]" + BLUE + " Use all possible dates" + WHITE)
    print("[" + YELLOW + "3" + WHITE + "]" + BLUE + " Use most common number used in password only" + WHITE)
    print("[" + YELLOW + "4" + WHITE + "]" + BLUE + " Exit" + WHITE)
    option = int(input(GREEN + "=====>" + WHITE))
    if option == 1:
        while True:
            number_digits = input("How many numbers do you want to put" + "(/!\max is 6 numbers!\)")
            if number_digits.isdigit() and int(number_digits) <= 6:
                number_digits = "9" * int(number_digits)
                digits_list = numbers(number_digits)
                break
            else:
                parser.error('A number lower or equal to 6 is required for the lenght of the numbers')
    elif option == 2:
        digits_list = dates()
    elif option == 3:
        digits_list = ["1", "12", "123", "1234", "12345", "123456", "1234567", "12345678", "123456789", "00", "01",
                       "10", "11", "13", "19", "22", "23", "42", "69", "77", "99", "314", "666", "777", "111",
                       "100", "200"]
    else:
        os.system("cls")
        quit()

    return digits_list


def word_options():
    # word options
    addword = False
    replaceword = False
    repeat = False
    upper = False
    title = False
    option2 = 10
    while option2 != 0:
        print(GREEN + "{-----WORDS OPTIONS-----} " + WHITE)

        print("[" + GREEN + "0" + WHITE + "]" + BLUE + "Run Bruteforce" + WHITE)

        if not replaceword:
            print("[" + YELLOW + "1" + WHITE + "]" + BLUE + " Replace every E by 3, every A by 4, and every = O by 0(zéro)" + WHITE)
        else:
            print("[" + YELLOW + "1" + WHITE + "]" + RED + " REMOVE Replace" + WHITE)

        if not repeat:
            print("[" + YELLOW + "2" + WHITE + "]" + BLUE + " Repeat the word two times" + WHITE)
        else:
            print("[" + YELLOW + "2" + WHITE + "]" + RED + " REMOVE Repeat" + WHITE)

        if not upper:
            print("[" + YELLOW + "3" + WHITE + "]" + BLUE + " Put the whole word in uppercase" + WHITE)
        else:
            print("[" + YELLOW + "3" + WHITE + "]" + RED + " REMOVE Uppercase" + WHITE)

        if not title:
            print("[" + YELLOW + "4" + WHITE + "]" + BLUE + " Put a capital letter at the beginning" + WHITE)
        else:
            print("[" + YELLOW + "4" + WHITE + "]" + RED + " REMOVE Title" + WHITE)

        if not addword:
            print("[" + YELLOW + "5" + WHITE + "]" + BLUE + " Add a word you choose to each word" + WHITE)
        else:
            print("[" + YELLOW + "5" + WHITE + "]" + RED + " REMOVE Add word" + WHITE)

        print("[" + YELLOW + "6" + WHITE + "]" + BLUE + " Exit" + WHITE)
        option2 = int(input(GREEN + "=====>" + WHITE))
        if option2 == 0:
            break
        if option2 == 1:
            if replaceword:
                replaceword = False
            else:
                replaceword = True

        if option2 == 2:
            if repeat:
                repeat = False
            else:
                repeat = True

        elif option2 == 3:
            if upper:
                upper = False
            else:
                upper = True

        elif option2 == 4:
            if title:
                title = False
            else:
                title = True

        elif option2 == 5:
            if title:
                addword = False
            else:
                addword = True

        elif option2 == 6:
            os.system("cls")
            quit()
        else:
            print(RED + "WRONG INPUT" + WHITE)

    return replaceword, repeat, upper, title, addword


def replace(word):
    # replace e by 3 a by 4 o by 0
    word = word.replace("e", "3").replace("a", "4").replace("o", "0")
    return word


def dates():
    # generate dates
    dates = []
    dates_day = ["1","2","3","4","5","6","7","8","9","01","02","03","04","05","06","07","08","09","10","11","12","13",
                 "14","15","16","17","18","19","20","21","22","23","24","25","26","27","28","29","30","31"]
    dates_month = ["1","2","3","4","5","6","7","8","9","01","02","03","04","05","06","07","08","09","10","11","12"]

    for days, month in itertools.product(dates_day, dates_month):
        dates.append(days+month)

    for years in range(1875,2020):
        dates.append(years)
    return dates


def numbers(number_digits):
    # generate numbers list
    i = 0
    digits_list = []

    while i <= int(number_digits):
        n = str(i)
        digits_list.append(n)
        i += 1

    return digits_list


def readresult(end_time):
    # read the result of the bruteforce
    print("\n" + BLUE + "--------------------------{ Scan Finished }--------------------------" + WHITE)

    print("Time taken: -{" + YELLOW + str(end_time - start_time) + WHITE + "}-")

    if not result_list:
        print(MAGENTA +"No Password Found")
        print(GREEN + "")
        print(result_list)
    else:
        for a in result_list:
            print(a)
            if args.save:
                s = open(save, "a")
                s.write(str(result_list))

def error(error):
    print(RED + error + WHITE)
    quit()
def starting(mode):
    # starting process animation
    print(GREEN + "Starting "+ mode + WHITE)
    for i in range(4):
        print(RED + str(i) + WHITE)
        time.sleep(1)
    os.system("cls")


def start():
    sys.stdout.write(YELLOW + '''
    ────╔╗──╔╗────────────╔╗─────     ╔╗──────────╔╗──────╔═╗──────────────────
    ────║║─╔╝╚╗──────────╔╝╚╗────     ║║─────────╔╝╚╗─────║╔╝──────────────────
    ╔╗╔╗║║─╚╗╔╝╔╗╔╗╔╗╔══╗╚╗╔╝╔══╗     ║╚═╗╔═╗╔╗╔╗╚╗╔╝╔══╗╔╝╚╗╔══╗╔═╗╔══╗╔══╗╔═╗
    ║║║║║║──║║─║╣║╚╝║║╔╗║─║║─║║═╣     ║╔╗║║╔╝║║║║─║║─║║═╣╚╗╔╝║╔╗║║╔╝║╔═╝║║═╣║╔╝
    ║╚╝║║╚╗─║╚╗║║║║║║║╔╗║─║╚╗║║═╣     ║╚╝║║║─║╚╝║─║╚╗║║═╣─║║─║╚╝║║║─║╚═╗║║═╣║║─
    ╚══╝╚═╝─╚═╝╚╝╚╩╩╝╚╝╚╝─╚═╝╚══╝     ╚══╝╚╝─╚══╝─╚═╝╚══╝─╚╝─╚══╝╚╝─╚══╝╚══╝╚╝─by Thewizy 
        ''' + RED + '''             [ Disclaimer Alert ]''' + YELLOW + ''' 
        ''' + WHITE + '''           Not Responsible For Misuse ''' + YELLOW + '''
        ''' + WHITE + '''               or Illegal Purposes.''' + YELLOW + '''
        ''' + WHITE + '''           Use it just for''' + RED + ''' WORK''' + WHITE + ''' or ''' + RED + '''EDUCATIONAL''' + WHITE + ''' !
        ''')

    print("\n" + "-Found [" + YELLOW + str(lines_hashfile) + WHITE + "] hashes in" + RED + " hashlist " + WHITE +
          "\n" + "-Found [" + YELLOW + str(lines_wordfile) + WHITE + "] words in " + BLUE + "wordlist " + WHITE)
    print("\n" + BLUE + "--------------------------------------------------{  }--------"
                        "------------------------------------------" + WHITE)

    main()


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description="Ultimate Sha1/256/512 and MD5 hashes Bruteforcer with dictionaries",
                                     prog="UltimateBrutforcer",
                                     usage="%(prog)s.py <your_wordlist.txt> <your_hashlist.txt> -option1 etc...")

    parser.add_argument("wordlist", help="The wordlist you wish to use.(Example: wordlist.txt)", type=str)
    parser.add_argument("hashlist", help="The hashlist you wish to find the password.(Example: hashlist.txt)", type=str)
    parser.add_argument("-n", "--numbers",default=False, dest="numbers", action="store_true",
                        help="Open numbers options( DATES/COMMON/CHOOSEN)")
    parser.add_argument("--fr", default=False, dest="front", action="store_true",
                        help="Change the numbers to be at the beginning of the word")
    parser.add_argument("--ex", default=False, dest="extremity", action="store_true",
                        help="Change the numbers to be at the extremity of the word")
    parser.add_argument("-w", "--word", default=False, dest="word", action="store_true",
                        help="Open word options.")
    parser.add_argument("-s", "--save", default=False, dest="save", action="store_true",
                        help="Save the results in a text file.")
    parser.add_argument("-bf", "--bruteforce", default=False, dest="brut", action="store_true",
                        help="Bruteforce hashes testing all possibilities / Bruteforce hashes testing random passwords")
    parser.add_argument("-pr", "--progression", default=False, dest="prog", action="store_true",
                        help="Stop whenever a password is found")
    parser.add_argument("-sh", "--show", default=False, dest="show", action="store_true",
                        help=" Show the passwords tested (/!\TAKES A LOT MORE TIME/!\)")

    args = parser.parse_args()
    # All errors about options:
    if args.front and not args.numbers:
        parser.error('-n is required when --front is set.')
    if args.extremity and not args.numbers:
        parser.error('-n is required when --front is set.')
    if args.extremity and args. front:
        parser.error('you cannot put those two options to -n')

    # global variables:
    w = args.wordlist
    h = args.hashlist
    lines_hashfile = countlines_hashfile()
    lines_wordfile = countlines_wordfile()
    result_list = []
    hashmethod_list = []
    hash_list = []
    BLUE, RED, WHITE, YELLOW, MAGENTA, GREEN,PURPLE, END = '\33[94m', '\033[91m', '\33[97m', '\33[93m', '\033[1;35m', '\033[1;32m','\033[95m','\033[0m'

    if args.save:
        run = True
        while run:
            save = input("How do you want to name the save file?")
            if save != "":
                save = save+".txt"
                break
    hashmethod()
    start()
