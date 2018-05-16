results = []
"""
results.append(["Index", "Title", 'Path'])
results.append([1, "Apocalypsis Noctis", "https://youtube.com"])


print(results)

print("SEPARATE THE WATER OF BLOOOOOOOOOD")


def get():
    return [row[1] for row in results]


print(get())
"""

# Add a row to the array


def append(title, path):
    new_index = len(result)
    results.append([new_index, title, path])


# Refresh the data with new one
def setResult(*args):
    global results
    results = []
    new_index = 0

    if args[0] and args[1]:
        for item in args:
            results.append([new_index, args[0], args[1]])
            new_index += 1
    else:
        raise Exception("Data format incorrect")


# Get a row from index or title
def getResult(arg):
    try:
        if isinstance(arg, int):
            print("searching for Index")
            return [row[arg] for row in results]
        else:
            print("searching for Title")
            return "Not currently implemented"

    except IndexError as indexErr:
        print("Seach index out of range")
        print(indexErr.args)
        return "Index out of range"
    except Exception as genErr:
        print(genErr.args)
        return "Error, check console"


def load():
    try:
        print("load cache into results array")
    except Exception as err:
        print(err.args)


if __name__ == "__main__":
    print("Running as main thread, for some reason")
else:
    load()
