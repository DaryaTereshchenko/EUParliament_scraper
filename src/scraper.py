from utils import load_json, clean_title, load_page
import csv
from bs4 import BeautifulSoup

def extract_role_from_paragraph(paragraph):
    """	
    Extract the party from the name span in the HTML 
    :param paragraph: HTML paragraph element
    :return: party name
    """	
    # Find the span element with class="italic"
    italic_span = paragraph.find('span', {'class': 'italic'})
    
    if italic_span:
        return italic_span.get_text(strip=True)
    else:
        return ""

def scrape_data(urls, filename):
    """
    Scrape data from the given URLs and save it to a CSV file
    :param urls: list of URLs
    :param filename: name of the CSV file

    """
    all_extracted_content = []

    for url in urls:
        soup = load_page(url)

        if soup is None:
            print(f"The page {url} does not exist")
            continue

        extracted_content = {}
        date = soup.find('td', class_='doc_title').get_text(strip=True)
        title = soup.find('td', class_='doc_title', style="background-image:url(/doceo/data/img/gradient_blue.gif)").get_text(strip=True)
        filtered_title = clean_title(title)

        extracted_content["title"] = filtered_title
        extracted_content["date"] = date
        extracted_content["link"] = url
        extracted_content["speakers"] = {}

        for speaker_tag in soup.findAll('p', {'class': 'contents'}):
            speaker_name_span = speaker_tag.find('span', {'class': 'doc_subtitle_level1_bis'})
            if speaker_name_span:
                speaker_name = speaker_name_span.get_text(strip=True)
                speaker_role = extract_role_from_paragraph(speaker_tag)
                speaker_name = f"{speaker_name} ({speaker_role})" if speaker_role else speaker_name

                if speaker_name not in extracted_content["speakers"]:
                    extracted_content["speakers"][speaker_name] = {"text": ""}
                
                # Directly append the text from the <p class="contents"> element
                text = speaker_tag.get_text(strip=True)
                extracted_content["speakers"][speaker_name]["text"] += text

        all_extracted_content.append(extracted_content)

    with open(f"{filename}.csv", "w", newline="", encoding="utf-8") as csvfile:
        fieldnames = ["title", "date", "speaker", "text", "link"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for content in all_extracted_content:
            title = content["title"]
            date = content["date"]
            url = content["link"]
            for speaker, details in content["speakers"].items():
                writer.writerow({
                    "title": title,
                    "date": date,
                    "speaker": speaker,
                    "text": details["text"],
                    "link": url
                })

    print("CSV file saved successfully!")

if __name__ == "__main__":
    # Get a directory with URLs from the user (should be a JSON file)
    links = input("Enter the directory of the URLs (JSON format): ")
    # Get a filename from the user
    filename = input("Enter the filename of the csv: ")
    # Load the URLs from the JSON file
    urls = load_json(links)
    # Scrape the data and save it to a CSV file
    scrape_data(urls, filename)