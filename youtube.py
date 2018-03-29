from bs4 import BeautifulSoup as soup
from selenium import webdriver
driver = webdriver.Firefox()


def search(*args):
    # Site to read
    root_url = "https://www.youtube.com/results?search_query="

    # Read site
    driver.get(root_url + "+".join(args))
    html = driver.page_source

    # Parse site
    page_soup = soup(html, "lxml")

    # Filter query
    array = page_soup.findAll("yt-formatted-string", id="result-count")
    # result-count

    results = "None"
    titles = []

    if array:
        for item in array:
            if item:
                results = item.string

        #array = page_soup.findAll("a", id="video-title", limit=3)
        array = page_soup.findAll(lambda tag:
                                  tag.name == "a" and tag.findParent("div", {"id": "dismissable"}), attrs={"id": "video-title"}, limit=5)

        if array:
            for item in array:
                if item:
                    titles.append(item.string)

    result = []

    result.append("Query: " + root_url + "+".join(args))
    result.append(results)

    index = 0

    for item in titles:
        index += 1
        result.append("Result #" + str(index) + ": " + item)

    return result

def save_options(*args):
    cache = open("w", "cache_link_list.txt")

    index = 0
    for item in args:
        if item.startswith("https://"):
            cache.write("a", str(index) + ": " + item.string)
            index += 1

def getList():
    array = []

    array.append("something 1")
    array.append("something 2")
    array.append("something 3")

    return array
