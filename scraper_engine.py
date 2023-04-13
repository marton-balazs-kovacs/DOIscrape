from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
import time
import pandas as pd
import os


def doi_to_url(doi):
    """
    This function finds the link to a webpage of a research article
    corresponding to the given DOI. The function opens a browser window
    and populates a webpage designed for this purpose.
    :param doi: str. A digital object identifier (DOI) of a research article.
    :return: Link to the webpage that contains the article.
    """
    driver = webdriver.Firefox()
    # For maximizing window
    driver.maximize_window()
    # Gives an implicit wait for the page to load
    driver.implicitly_wait(1)
    # Populate link searching site form with the DOI
    link = "https://dx.doi.org/"
    driver.get(link)
    box = driver.find_element(by=By.ID, value="nameID")
    box.send_keys(doi)
    box.submit()

    # Wait for the new page to load
    while link == driver.current_url:
        time.sleep(1)

    url = driver.current_url
    driver.quit()
    return url


def scrape_url(url, all_links=True):
    """
    This function scrapes a wepage at the given URL for email addresses. To do this,
    the function opens a browser window and parses the whole javascript code.
    :param url: str. URL to the webpage containing the research article.
    :param all_links: boolean. If True all links of the initial webpage will be searched for additional email addresses.
    :return: The function returns an array of email addresses found on the webpage/webpages.
    """
    # Using Selenium to get the page source with javascript executed
    driver = webdriver.Firefox()
    driver.get(url)
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    # Extracting emails using BeautifulSoup
    emails = []
    for link in soup.find_all('a'):
        email = link.get('href')
        if email and 'mailto:' in email:
            email = email.replace('mailto:', '')
            emails.append(email)

    # Search for emails by opening all links
    if all_links:
        # Collecting all links from the website
        links = []
        for link in soup.find_all('a'):
            link = link.get('href')
            if link and link.startswith(url):
                links.append(link)
            elif link and not link.startswith(url):
                links.append(url + link)

        # Repeat the process for all the links found in the initial page
        for link in links:
            try:
                driver.get(link)
                html = driver.page_source
                soup = BeautifulSoup(html, 'html.parser')
                for link in soup.find_all('a'):
                    email = link.get('href')
                    if email and 'mailto:' in email:
                        email = email.replace('mailto:', '')
                        emails.append(email)
            except:
                pass

    # Removing duplicates
    emails = list(set(emails))
    driver.quit()
    return emails


def scrape(path, all_links=True):
    """
    This function looks up the webpages of research articles corresponding to a list of DOIs,
    and extracts any email address from them. The function saves the DOIs at every tenth percentile
    of the DOI lists' length.
    :param path: str. The path to the .csv file containing the DOIs as strings in the first column.
    :param all_links: boolean. If True all links of the initial webpage will be searched for additional email addresses.
    :return: The function returns a .csv file with two columns named 'doi' and 'emails'.
    """
    # Creating a pandas df to store the results
    results = pd.DataFrame(columns=["doi", "emails"])

    # Loading DOIs to scrape
    doi_df = pd.read_csv(os.path.abspath(path))
    print(f"Starting with {len(doi_df)} DOIs.")
    # Stripping white spaces
    doi_df[doi_df.columns[0]] = doi_df[doi_df.columns[0]].str.strip()
    # Excluding duplicates
    doi_df.drop_duplicates(subset=doi_df.columns[0], keep=False, inplace=True)
    print(f"{len(doi_df)} DOIs remained after duplicate removal.")
    # Transforming df to list
    doi_list = doi_df.to_numpy()

    # Scrape the email addresses based on the DOIs
    for i, doi in enumerate(doi_list):
        print(f"Checking DOI: {doi[0]}")
        url = doi_to_url(doi[0])
        emails_from_doi = scrape_url(url, all_links=all_links)
        results = pd.concat([results, pd.DataFrame([{"doi": doi[0], "emails": emails_from_doi}])])

        # Save results at every tenth percentile of the doi list
        if (i + 1) % (len(doi_list) // 10) == 0 or i == len(doi_list) - 1:
            save_path = os.path.abspath(f"./doiscaper_results_{int((i + 1) * 10 / len(doi_list))}.csv")
            results.to_csv(save_path, index=False)
            print(f"Results saved to {save_path}.")

            # Reset results dataframe
            results = pd.DataFrame(columns=["doi", "emails"])
