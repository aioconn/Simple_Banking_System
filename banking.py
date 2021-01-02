# Aiden O'Connor
# Project template from intellij academy


import random
import sqlite3

conn = sqlite3.connect('card.s3db')
cur = conn.cursor()
cur.execute("""CREATE TABLE IF NOT EXISTS card(
                id INTEGER,
                number TEXT,
                pin TEXT,
                balance INTEGER DEFAULT 0
                )
                """)
conn.commit()


def check_card(card_num):
    checksum = int(card_num[-1])
    card_num = card_num[:-1]
    new_card_num = list(card_num)
    map_ob = map(int, new_card_num)
    my_list = list(map_ob)
    for i in range(0, len(my_list), 2):
        my_list[i] *= 2
    for i in range(0, len(my_list)):
        if my_list[i] > 9:
            my_list[i] -= 9
    total = 0
    for i in range(0, len(my_list)):
        total += my_list[i]
    if (total + checksum) % 10 == 0:
        return True
    else:
        return False


class SimpleBank:
    cards = {}

    def __init__(self):
        self.intro()

    def get_can(self):
        temp = "%09d" % random.randint(0, 999999999)
        if temp in self.cards.keys():
            self.get_can()
        else:
            return temp

    def get_checksum(self, iin, can):
        temp1 = iin + can
        temp2 = list(temp1)
        map_ob = map(int, temp2)
        my_list = list(map_ob)
        for i in range(0, len(my_list), 2):
            my_list[i] *= 2
        for i in range(0, len(my_list)):
            if my_list[i] > 9:
                my_list[i] -= 9
        total = 0
        for i in range(0, len(my_list)):
            total += my_list[i]
        while True:
            x = random.randint(0, 9)
            if (total + x) % 10 == 0:
                break
            else:
                continue
        return x

    def create(self):

        print('\nYour card has been created')
        print('Your card number:')
        iin = '400000'
        cus_acc_num = self.get_can()
        checksum = self.get_checksum(iin, cus_acc_num)
        card_num = iin + cus_acc_num + str(checksum)
        print(card_num)
        print('Your card PIN:')
        pin = "%04d" % random.randint(0, 9999)
        print(pin)
        self.cards[card_num] = pin
        cur.execute('SELECT COUNT(id) FROM card')
        rows = int(''.join(map(str, cur.fetchone()))) + 1
        cur.execute('INSERT INTO card (id, number, pin) VALUES (?, ?, ?)', (rows, card_num, pin))
        conn.commit()

    def log(self):
        print('')
        print('Enter your card number:')
        card_number = input()
        print('Enter your pin:')
        pin_number = input()
        card_exist = cur.execute("SELECT EXISTS(SELECT 1 FROM card WHERE number == (?))", [card_number]).fetchone()
        pin_exist = cur.execute("SELECT EXISTS(SELECT 1 FROM card WHERE pin == ? AND number == ?)",
                                [pin_number] + [card_number]).fetchone()
        conn.commit()
        if card_exist[0] == 1 and pin_exist[0] == 1:
            print('')
            print('You have successfully logged in!')
            while True:
                print('\n1. Balance')
                print('2. Add income')
                print('3. Do transfer')
                print('4. Close account')
                print('5. Log out')
                print('0. Exit')
                choice = input()
                cur.execute("SELECT balance FROM card WHERE number = (?) AND pin = (?)",
                            [card_number] + [pin_number])
                balance = cur.fetchone()
                if choice == '1':
                    print('')
                    print(balance)
                    conn.commit()
                elif choice == '2':
                    add_income = input('\nEnter income:')
                    cur.execute("UPDATE card SET balance = balance + (?) WHERE number = (?)",
                                [add_income] + [card_number])
                    conn.commit()
                    print('Income was added!')
                elif choice == '3':
                    print('\nTransfer')
                    transfer_card_num = input('Enter card number:')
                    transfer_card_exist = cur.execute("SELECT EXISTS(SELECT 1 FROM card WHERE number = (?))",
                                                      [transfer_card_num]).fetchone()
                    conn.commit()
                    if not check_card(transfer_card_num):
                        print('Probably you made a mistake in the card number. Please try again!')
                        continue
                    elif transfer_card_exist[0] != 1:
                        print('Such a card does not exist')
                        continue
                    transfer_amount = int(input('Enter how much money you want to transfer'))
                    print(balance)
                    if balance[0] < transfer_amount:
                        print('Not enough money!')
                    else:
                        cur.execute("UPDATE card SET balance = balance - (?) WHERE number = (?)",
                                    (transfer_amount, card_number))
                        cur.execute("UPDATE card SET balance = balance + (?) WHERE number = (?)",
                                    (transfer_amount, transfer_card_num))
                        conn.commit()
                        print('Success!')
                elif choice == '4':
                    cur.execute("DELETE FROM card WHERE number = (?)", [card_number])
                    conn.commit()
                    print('\nThe account has been closed!')
                    break
                elif choice == '5':

                    print('\nYou have successfully logged out!')
                    self.intro()
                elif choice == '0':

                    print('\nBye!')
                    exit(0)
        else:
            print('Wrong card number or PIN!')

    def intro(self):
        while True:
            print('\n1. Create an account')
            print('2. Log into account')
            print('0. Exit')
            my_input = input()
            if my_input == '1':
                self.create()
            elif my_input == '2':
                self.log()
            elif my_input == '0':

                print('\nBye!')
                break
            else:
                continue


bank = SimpleBank()
conn.close()
