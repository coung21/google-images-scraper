
# google-images-scraper

A tool to scraping images from google with provided keywords.

## Pre-requisites

1.Google Chrome<br>
2.Python Packages (requests, selenium, unidecode, python-dotenv)

## Installation

Use [pip](https://pip.pypa.io/en/stable/installation/) package manager to install libraries.

```bash
  git clone https://github.com/coung21/google-images-scraper.git
```
```bash
  pip install selenium
```
```bash
  pip install python-dotenv
```
```bash
  pip install unidecode
```


## Usage

Step 1: Create `.env` then add your folder path to scraping:    
```env
FOLDER_PATH={your/folder/path}
```

Step 2: Add the keywords you want to scrape into the `keywords.txt` file with one keyword per line:
```txt
cat
dog
bird
house
```
Step 3: Run the following cmd:
```bash
py script.py --limit {NUMBERS_OF_IMAGES}
```
Note: `NUMBERS_OF_IMAGES` is the number of images you want to retrieve for each keyword.<br>

***If you find this tool useful, please give this repo 1 star. Thank you very much ❤️***