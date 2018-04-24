from bs4 import BeautifulSoup
from selenium import webdriver
import manage_data as db
import time


def search(*query):
    # Prepare variables
    driver = webdriver.Firefox()
    result = []
    root_url = "https://www.youtube.com/results?search_query="

    # Read Site
    driver.get(root_url + "+".join(query))
    html = driver.page_source
    page_soup = BeautifulSoup(html, "lxml")
    driver.close()

    # Filter query
    # Get result count of videos
    result.append(getResultCount(page_soup))

    # Get videos
    videos = getVideos(page_soup)
    for item in videos:
        result.append(item)

    # For debugging purposes, print result array
    """
    for item in result:
        print(str(item))
    """

    return result


def getResultCount(html):
    result = "None"
    count_array = html.findAll("yt-formatted-string", id="result-count")

    if count_array[1]:
        result = count_array[1].string

    return result


def getVideos(html):
    result = []
    search_data = []

    titles = html.findAll(lambda tag: tag.name == "a" and tag.findParent(
        "div", {"id": "dismissable"}), attrs={"id": "video-title"}, limit=12)

    counter = 0
    for item in titles:
        if counter > 1:
            result.append(str(counter - 2) + ": " + item.string)
            search_data.append([(counter - 2), item.string, item['href']])

        counter += 1

    db.saveSearchData("youtube", search_data)

    return result
