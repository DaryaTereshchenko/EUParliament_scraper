# *Web crawler and scraper to extract texts of European Parliament debates.*

## Description
The [Crawler](https://github.com/DaryaTereshchenko/EUParliament_scraper/blob/main/src/crawler.py) is used to iterate over the dropdown menu on the [page](https://www.europarl.europa.eu/plenary/en/debates-video.html#sidesForm), and extract links with pertinent debates and presentations. 
The links are then saved in a JSON file. The [Scraper](https://github.com/DaryaTereshchenko/EUParliament_scraper/blob/main/src/scraper.py) is used to extract the text of the debates and presentations from the links saved in the JSON file. The extracted data is stored in a csv file.

## Example Usage - Crowler 
Call the `crawler.py` file with the following arguments:
```python crawler.py```
**You will be prompted to enter:**
- a URL of the webpage;
- a query (topic) to search for; 
- a directory to save the links;
- a filename;

## Example Usage - Scraper
Once you have the necessary links, you can use the [scraper](https://github.com/DaryaTereshchenko/EUParliament_scraper/blob/main/src/scraper.py) to extract texts from the urls.

Call the file `scraper.py` with the following arguments:
```python scraper.py```
**You will be prompted to enter:**
- a directory where the links are saved;
- a file name to save a final csv file;

**The extracted data is stored in a csv file with the following columns:**
- title of a debate or presentation;
- date;
- speaker;
- text of the speech;
- link to the original source.

## Installation
To install the dependencies listed in the `requirements.txt` file, use the following command:
```pip install -r requirements.txt```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.