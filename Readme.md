# *Web crawler and scraper for the European parliament debates.*

## Description
The [Crawler](https://github.com/DaryaTereshchenko/EUParliament_scraper/blob/main/src/crawler.py) is a python programs, aims to be used for iterating over the dropdown menu on the [page](https://www.europarl.europa.eu/plenary/en/debates-video.html#sidesForm), and extracting the links of pertinent debates and statements. The links are then saved in a JSON file.

## Example Usage - Crowler 
Call the file with the following arguments:
```python crawler.py```
**You will be prompted to enter:**
- the URL of the webpage;
- the query to search for; 
- the directory to save the links;
- the filename;

## Example Usage - Scraper
Once you have the necessary links, you can use the [scraper](https://github.com/DaryaTereshchenko/EUParliament_scraper/blob/main/src/scraper.py) to extract the text from the debates.

Call the file with the following arguments:
```python scraper.py```
**You will be prompted to enter:**
- the directory where the links are saved;
- the file name to save the final csv file;

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