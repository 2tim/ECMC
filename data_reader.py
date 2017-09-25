import struct
import pprint

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
    dollar_debits = 0.0
    dollar_credits = 0.0
    autopays = 0
    ended = 0
    special_balance = 0.0
    # Found number of records to be
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
            amount = struct.unpack('!d', raw_float)[0]
            record.update({"amount": amount})
            # Debit
            if record.get("enum") == 0x00:
                dollar_debits += amount
                if record.get("uid") == 2456938384156277127:
                    special_balance += amount
            # Credit
            else:
                dollar_credits += amount
                if record.get("uid") == 2456938384156277127:
                    special_balance -= amount
        # StartAutopay
        elif record.get("enum") == 0x02:
            autopays += 1
        # EndAutopay
        elif record.get("enum") == 0x03:
            ended += 1
        records.append(record)
    print("What is the total amount in dollars of debits?")
    #Assumes simple rounding here
    print("$%.2f" % dollar_debits)
    print("What is the total amount in dollars of credits?")
    print("$%.2f" % dollar_credits)
    print("How many autopays were started?")
    print("{} autopays where started".format(autopays))
    print("How many autopays were ended?")
    print("{} autopays where ended".format(ended))
    print("What is balance of user ID 2456938384156277127?")
    print("$%.2f" % special_balance)
