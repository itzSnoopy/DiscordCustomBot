from bs4 import BeautifulSoup as soup
from selenium import webdriver


def search(*query):
    driver = webdriver.Firefox()
    result = []
    root_url = "https://www.youtube.com/results?search_query="

    # Read site
    driver.get(root_url + "+".join(query))
    html = driver.page_source

    # Parse Site
    page_soup = soup(html, "lxml")

    # Filter query
    # Get result count of videos
    array = page_soup.findAll("yt-formatted-string", id="result-count")

    results = "None"
    titles = []

    if array:
        for item in array:
            if item:
                results = item.string

        array = page_soup.findAll(lambda tag:
                                  tag.name == "a" and tag.findParent("div", {"id": "dismissable"}), attrs={"id": "video-title"}, limit=5)

        if array:
            for item in array:
                if item:
                    titles.append(item.string)

    result.append("Query: " + root_url + "+".join(query))
    result.append(results)

    index = 0
    for item in titles:
        index += 1
        result.append("Result #" + str(index) + ": " + item)

    return result
