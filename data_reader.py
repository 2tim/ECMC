import struct
from money import Money

'''
See field definition size and rules in ./byte-reader/README.md

The below code is intended to run on Python 3.5+

TODO: Additional consideration should be taken for effectively handling floating point currency according to ECMC
business rules.
'''

with open("byte-reader/data.dat", 'rb') as data:
    system = data.read(4)
    version = int.from_bytes(data.read(1), 'big', signed=False)
    num_records = int.from_bytes(data.read(4), 'big', signed=False)
    records = []
    dollar_debits = Money(0, currency='USD')
    dollar_credits = Money(0, currency='USD')
    autopays = 0
    ended = 0
    special_balance = Money(0, currency='USD')
    for _ in range(num_records+1):
        record = {"enum": int(data.read(1).hex())}
        record.update(
            {
                "time_stamp": int.from_bytes(data.read(4), 'big', signed=False),
                "uid": int.from_bytes(data.read(8), 'big', signed=False)
            }
        )
        # ENUM 0 (Debit) and 1 (Credit) contain an extra 'amount' record.
        if record.get("enum") <= 0x01:
            raw_float = data.read(8)
            # using '!' for network byte order and 'd' for float64 conversion to double, which is a python float
            raw_amount = struct.unpack('!d', raw_float)[0]
            amount = Money(raw_amount, currency='USD')
            record.update({"amount": amount})
            # Debit
            if record.get("enum") == 0x00:
                dollar_debits = dollar_debits + amount
                if record.get("uid") == 2456938384156277127:
                    special_balance = special_balance + amount
            # Credit
            else:
                dollar_credits = dollar_credits + amount
                if record.get("uid") == 2456938384156277127:
                    special_balance = special_balance - amount
        # StartAutopay
        elif record.get("enum") == 0x02:
            autopays += 1
        # EndAutopay
        elif record.get("enum") == 0x03:
            ended += 1
        records.append(record)
    print("What is the total amount in dollars of debits?")
    # Assumes simple rounding here
    print(dollar_debits.format('en_US'))
    print("What is the total amount in dollars of credits?")
    print(dollar_credits.format('en_US'))
    print("How many autopays were started?")
    print("{} autopays where started".format(autopays))
    print("How many autopays were ended?")
    print("{} autopays where ended".format(ended))
    print("What is balance of user ID 2456938384156277127?")
    print(special_balance.format('en_US'))
