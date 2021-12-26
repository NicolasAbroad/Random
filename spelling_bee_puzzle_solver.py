#!/usr/bin/env python3

import os.path
import re
import urllib.request

def get_essential_letter_input():
    print('Please input essential letter:')
    essential_letter = input().lower()

    check_regex = re.compile('^[a-z]$')
    match_obj = check_regex.search(essential_letter)
    if (match_obj is None):
        raise ValueError('Unable to parse input.')

    return essential_letter

def get_optional_letters_input():
    print('Please input 6 optional letters:')
    optional_letters = input().lower()

    check_regex = re.compile('^[a-z]{6}$')
    match_obj = check_regex.search(optional_letters)
    if (match_obj is None):
        raise ValueError('Unable to parse input.')

    return optional_letters

def generate_regex(essential_letter, optional_letters):
    regex = '^[' + essential_letter + optional_letters + ']*[' + essential_letter + '][' + essential_letter + optional_letters + ']*$'
    return re.compile(regex)

def open_english_dictionary(file_path):
    file_exists = os.path.exists(file_path)
    if (file_exists is False):
        download_english_dictionary(file_path)
    return open(file_path, 'r')

def download_english_dictionary(file_path):
    url = 'https://raw.githubusercontent.com/dwyl/english-words/master/words_alpha.txt'
    urllib.request.urlretrieve(url, file_path)

def execute():
    # Get user input
    essential_letter = get_essential_letter_input()
    optional_letters = get_optional_letters_input()

    # Generate regex
    regex = generate_regex(essential_letter, optional_letters)
    print()

    # file = open('words_alpha.txt', 'r')
    file = open_english_dictionary('words_alpha.txt')
    words = file.readlines()
    for word in words:
        # Trim word
        word = word.strip()

        # Check if word matches
        match_obj = regex.search(word)
        if (match_obj is None):
            continue

        # Check word length
        if (len(word) < 4):
            continue

        print(word)

if (__name__ == '__main__'):
    execute()
