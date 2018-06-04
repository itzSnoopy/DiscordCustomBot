# Check format
# Returns bool
import csv


def checkUserFormat(args):
    if not args:
        print("NO DATA SENT")
        return False
    elif len(args) == 1:
        print("USER PROVIDED")
        # check if user in database
        if args[0].isdigit():
            print("VALIDATED")
            return True
        else:
            print("INVALID")
            return False
    elif len(args) == 2:
        print("USER AND DATA PROVIDED")
        if args[0][0] == "i" and len(args[0]) == 10:
            print("VALIDATED")
            return True
        else:
            print("INVALID")
            return False
    else:
        print("FORMAT ERROR")
        return False

# Get user from database


def getUserData(args):
    data = ["error", "Not in database"]
    print("searching for " + args[0])

    with open("db_Bot.csv", "r") as db:
        spamreader = csv.reader(db, delimiter=",")
        try:
            for row in spamreader:
                if len(row) == 0:
                    continue

                if len(args) == 1:  # search by discord id
                    if row[0] == args[0]:
                        print("encontrado: " + row[4])
                        return [row[2], row[3]]

                elif len(args) == 2:  # search by iCode
                    if row[2] == args[0] and row[3] == args[1]:
                        print("encontrado: " + row[4])
                        return [row[2], row[3]]

        except Exception as err:
            print(err)

    return data

# Inser user in DB


def insertUser(args):
    header = ["discord_userID", "discord_userName",
              "site_userID", "site_userPass", "site_userName"]
    result = "error"

    with open("db_Bot.csv", "a+") as db:
        spamwriter = csv.DictWriter(db, fieldnames=header, restval="NULL")
        try:
            spamwriter.writerow(
                {'discord_userID': args[0], 'discord_userName': args[1], 'site_userID': args[2], 'site_userPass': args[3], 'site_userName': args[4]})

            result = "Usuario registrado exitosamente"

        except Exception as err:
            print(err)

    return result


if __name__ == "__main__":
    print(getUserData(["363220777555853323"]))
