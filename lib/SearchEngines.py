import youtube_engine as yt
import google_engine as gg


def select(index):
    return{
        'google': 'google',
        'youtube': 'youtube',
        'duck': 'duckduckgo'
    }.get(index, 'google')


def search(engine, *query):
    hardcoded = []
    hardcoded.append("item 1")
    hardcoded.append("item 2")
    hardcoded.append("item 3")

    if engine == 'youtube':
        return yt.search(*query)
    elif engine == 'google':
        return gg.search(*query)
    elif engine == 'duckduckgo':
        return hardcoded
    else:
        return hardcoded
