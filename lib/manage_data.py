ENGINE_YOUTUBE = "youtube"
ENGINE_GOOGLE = "google"


def saveSearchData(engine, args):
    if engine == ENGINE_YOUTUBE:
        manageYoutubeCache(args)
        print("save data from " + engine)
    elif engine == ENGINE_GOOGLE:
        print("save data from " + engine)
    else:
        print("no engine provided")


"""
def manageYoutubeCache(args):
    cache = open("search_cache.txt", "w")
    cache.write("Last search on " + ENGINE_YOUTUBE + ";\n")

    for i in range(len(args)):
        cache.write("Index: " + str(args[i][0]) + ";\n")

        try:
            cache.write("Title: " + str(args[i][1]) + ";\n")
        except Exception as err:
            cache.write(
                "                Title with unidentified characters" + ";\n")

        cache.write("Path:  " + "https://youtube.com" +
                    str(args[i][2]) + ";\n")
        cache.write("----------------------" + "\n")

    cache.close()
"""


def manageYoutubeCache(args):
    cache = open("youtube_cache.txt", "w")

    for array in args:
        cache.write(str(array[0]))
        cache.write("https://youtube.com" + str(array[1]))

    cache.close()
