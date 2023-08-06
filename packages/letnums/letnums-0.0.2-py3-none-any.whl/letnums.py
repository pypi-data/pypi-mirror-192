from random import choices


def letter():
    amt = input("Enter Amount Of Letters: ")
    letters = ''.join(choices('abcdefghijklmnopqrstuvwxyz', k=int(amt)))
    print(letters)

def letter_number():
    amt = input("Enter Amount of letters: ")
    let_num = ''.join(choices('abcdefghijklmnopqrstuvwxyz1234567890',k=int(amt)))
    print(let_num)

def number():
    amt = input("Enter Amount of Numbers: ")
    numbers = ''.join(choices('0123456789',k=int(amt)))
    print(numbers)