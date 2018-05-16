import pip

dependencies = [
    "discord.py[voice]", "profanity", "selenium", "beautifulsoup4", "youtube-dl", "lxml"
]

installList = []

def main():
    uninstallAll()
    if checkDependencies():
        installDependencies()


def checkDependencies():
    print("Checking Dependencies")
    print("----------")

    global installList

    for module in dependencies:
        try:
            import module
            print(module + "... OK")

        except:
            installList.append(module)
            print(module + "... ERROR")

    if len(installList) == 0:
        print("\nAll dependendies are already installed")

        return False
    else:
        print("\nMissing " + str(len(installList)) + " dependencies\n\n")

    return True

def installDependencies():
    print("Installing Dependencies")
    print("----------")

    global installList
    index = 1

    for module in installList:
        print(module + "... INSTALLING (" + str(index) + "/" + str(len(installList)) + ")")
        pip.main(["install", "-q", module])

        index += 1

    print("\nAll modules installed")

def uninstallAll():
    for module in dependencies:
        print(module + "... UNINSTALLING")
        pip.main(["uninstall", "-y", "-q", module])

if __name__ == "__main__":
    #uninstallAll()
    main()
    input("pause")
