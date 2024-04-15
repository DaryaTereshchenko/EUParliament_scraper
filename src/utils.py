import os
import json
from urllib.request import urlopen 
from urllib.error import HTTPError 
from bs4 import BeautifulSoup
from urllib.error import URLError
import re

def save_as_json(data, dir, filename):
    """
    Save data as json file
    :param data: data to save
    :param dir: directory to save the file
    :param filename: name of the file
    
    """
    # Check if the directory exists
    if not os.path.exists(dir):
        os.makedirs(dir)
    path = os.path.join(dir, filename)

    # Save data as json file
    with open(path, 'w', encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False) 
    print(f"Data saved in {path}")


def load_json(file_path):
    """
    Load data from json file
    :param file_path: path to the file
    :return: data
    """
    try:
        with open(file_path, 'r', encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"File {file_path} not found")
        return None
    return data


def load_page(url):
    """
    Load page from url
    :param url: url of the page
    :return: BeautifulSoup object
    """

    try:
        html = urlopen(url)
    # Check if the page exists
    except HTTPError as e:
        return None
    # Check if the server is not found
    except URLError as e:
        return None
    # Check if the contect of the page can be parsed
    try:
        bsObj = BeautifulSoup(html.read(), 'html.parser')
    except AttributeError as e:
        return None
    # Return the BeautifulSoup object
    return bsObj

def extract_links(html_content):
    """
    Extract links from the HTML content
    :param html_content: HTML content
    :return: list of links
    """
    # Parse the HTML content
    soup = BeautifulSoup(html_content, "html.parser")

    # Find all elements with class="notice"
    notice_elements = soup.find_all(class_="notice")

    # Initialize an empty list to store the links
    links = []

    # Iterate through each notice element
    for notice in notice_elements:
        # Find all anchor elements within the notice element
        anchor_elements = notice.find_all("a")
        # Check if the title does not contain the word "vote"
        title = notice.get_text(strip=True)
        if "vote" in title.lower():
            continue
        # Extract the href attribute from each anchor element and append it to the links list
        for anchor in anchor_elements:
            link = anchor.get("href")
            links.append(link)

    return links


def clean_title(title):
    """
    Clean the title of a page
    :param title: title of the page
    :return: cleaned title
    """
    
    # Replace invalid characters with underscores
    title = re.sub(r'[^\w\s\-]', '', title)
    # Replace spaces with underscores
    title = title.replace(' ', '_')
    # Replace multiple underscores with a single underscore
    title = re.sub(r'_+', '_', title)
    return title