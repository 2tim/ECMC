import struct
import pprint

with open("byte-reader/data.dat", 'rb') as data:
    print(data.read(4))
    version = int(data.read(1).hex())
    num_records = int.from_bytes(data.read(4), 'big', signed=False)
    records = []
    dollar_debits = 0.0
    dollar_credits = 0.0
    autopays = 0
    ended = 0
    special_balance = 0.0
    for _ in range(num_records+1):
        record = {"enum": int(data.read(1).hex())}
        record.update(
            {
                "time_stamp": int.from_bytes(data.read(4), 'big', signed=False),
                "uid": int.from_bytes(data.read(8), 'big', signed=False)
            }
        )
        if record.get("enum") <= 0x01:
            # TODO: adjust for network byte order for float
            raw_float = data.read(8)
            # amount = str.fromhex(raw_float)
            amount = struct.unpack('!ff ', raw_float)[0]
            record.update({"amount": amount})
            if record.get("enum") == 0x00:
                dollar_debits += amount
                if record.get("uid") == 2456938384156277127:
                    special_balance += amount
            else:
                dollar_credits += amount
                if record.get("uid") == 2456938384156277127:
                    special_balance -= amount
        elif record.get("enum") == 0x02:
            autopays += 1
        elif record.get("enum") == 0x03:
            ended += 1
        records.append(record)
    print("What is the total amount in dollars of debits?")
    print("$%.2f" % dollar_debits)
    print("What is the total amount in dollars of credits?")
    print("$%.2f" % dollar_credits)
    print("How many autopays were started?")
    print("{} autopays where started".format(autopays))
    print("How many autopays were ended?")
    print("{} autopays where ended".format(ended))
    print("What is balance of user ID 2456938384156277127?")
    print("$%.2f" % special_balance)
    # pprint.pprint(records)
