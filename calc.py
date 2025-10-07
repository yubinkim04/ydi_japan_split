import pandas as pd
import numpy as np
from forex_python.converter import CurrencyRates
c = CurrencyRates()

# read payment book
df = pd.read_excel("payment_book.xlsx")

# create blank payment matrix
payment_matrix = pd.DataFrame(np.zeros((3,3)),
                              index=["david", "yubin", "issac"],
                              columns=["owes_david", "owes_yubin", "owes_issac"])

# iterate through each row in the payment book
for i in range(len(df)):
    item = df.iloc[i]
    price_per = item['Price']/len(item["Who ate"])
    consumers = list(item["Who ate"])
    for i in range(len(consumers)):
        if consumers[i] == "D":
            consumers[i] = "david"
        elif consumers[i] == "Y":
            consumers[i] = "yubin"
        elif consumers[i] == "I":
            consumers[i] = "issac"
    purchaser = item["who paid"]
    if purchaser == "D":
        purchaser = "owes_david"
    elif purchaser == "Y":
        purchaser = "owes_yubin"
    elif purchaser == "I":
        purchaser = "owes_issac"
    for consumer in consumers:
        curr_balance = payment_matrix.loc[consumer, purchaser]
        payment_matrix.loc[consumer, purchaser] = curr_balance + price_per

# create printer function
def printer(currency, d_to_y, d_to_i, y_to_i):
    #round to 2 decimal places
    d_to_y = round(d_to_y, 2)
    d_to_i = round(d_to_i, 2)
    y_to_i = round(y_to_i, 2)
    # print the balances
    if d_to_y > 0:
        print(f"David owes Yubin {currency} {d_to_y}")
    else:
        print(f"Yubin owes David {currency} {-d_to_y}")
    if d_to_i > 0:
        print(f"David owes Issac {currency} {d_to_i}")
    else:
        print(f"Issac owes David {currency} {-d_to_i}")
    if y_to_i > 0:
        print(f"Yubin owes Issac {currency} {y_to_i}")
    else:
        print(f"Issac owes Yubin {currency} {-y_to_i}")

# get balances
d_to_y = payment_matrix.loc["david", "owes_yubin"] - payment_matrix.loc["yubin", "owes_david"]
d_to_i = payment_matrix.loc["david", "owes_issac"] - payment_matrix.loc["issac", "owes_david"]
y_to_i = payment_matrix.loc["yubin", "owes_issac"] - payment_matrix.loc["issac", "owes_yubin"]

# Convert the amounts to KRW
d_to_y_krw = c.convert('JPY', 'KRW', d_to_y)
d_to_i_krw = c.convert('JPY', 'KRW', d_to_i)
y_to_i_krw = c.convert('JPY', 'KRW', y_to_i)

# Convert the amounts to USD
d_to_y_usd = c.convert('JPY', 'USD', d_to_y)
d_to_i_usd = c.convert('JPY', 'USD', d_to_i)
y_to_i_usd = c.convert('JPY', 'USD', y_to_i)

# Print the results
print("\nBalances in JPY:")
printer("JPY", d_to_y, d_to_i, y_to_i)
print("\nBalances in KRW:")
printer("KRW", d_to_y_krw, d_to_i_krw, y_to_i_krw)
print("\nBalances in USD:")
printer("USD", d_to_y_usd, d_to_i_usd, y_to_i_usd)