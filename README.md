# DOIscrape
DOIscrape takes DOIs as input and searches for email addresses connected to the authors of the corresponding articles.

The script uses a Python package called Selenium, which allows direct input and manipulation of the browser engine.
The script uses this in combination with the dx.doi.org, a website to resolve the DOI's, access the journal sites, and
scrape the emails from the journal sites.

Running the script opens a Chrome browser window on your computer.

The tool is pretty slow and inefficient, as it opens a browser window for each DOI it scrapes the emails for. 
It also clicks on every possible clickable thing on the site to look for possible email addresses to scrape.

# Install
Before using you should make sure: 

* Python 3.0.0 or above is installed on your system
* Google Chrome is installed on your system
* You have pipenv

The script was made and tested in Linux Mint environment.
I suspect running it on Windows would require some extra troubleshooting.

# Usage
The main scraping function ('scrape') is in the 'scraper_main.py' file. Change the function arguments in this file according to your needs, then run the following code in the project folder: `pipenv run python scraper_main.py` 

After a successful run the root folder should be populated with multiple '.csv' files containing the DOIs and the corresponding email addresses. 

You can find an 'example_doi_list.csv' file in the root folder which you can use to test the code.


 
