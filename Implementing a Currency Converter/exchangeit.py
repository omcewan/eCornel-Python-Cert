"""
User interface for module currency

When run as a script, this module prompts the user for two currencies and amount.
It prints out the result of converting the first currency to the second.

Author: Orlando McEwan
Date:   09/02/2022
"""

import currency

first_currency = input("3-letter code for original currency: ")

second_currency = input("3-letter code for the new currency: ")

amount = float(input("Amount of the original currency: "))

conversion = round(currency.exchange(first_currency, second_currency, amount), 3)

print(f'You can exchange {amount} {first_currency.upper()} for {conversion} {second_currency.upper()}.')
