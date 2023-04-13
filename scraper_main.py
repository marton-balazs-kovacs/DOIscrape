from scraper_engine import *
import pandas as pd
import numpy as np
import os

# Example usage of the DOIscraper functions
# Loading DOIs to scrape
doi_df = pd.read_csv(os.path.abspath("./example_doi_list.csv"))
# Turning the column containing the DOIs into a list
doi_list = doi_df["doi"].to_numpy()
# Scraping DOIs iteratively
# This is especially important if you have a lot of DOIs and you want to save any progress
# Creating sub arrays to iterate over
n = 2
doi_nested_list = np.array_split(doi_list, n)
for index, dois in enumerate(doi_nested_list):
    # Scraping the email addresses
    results = scrape(dois, all_links=False)
    # Saving the results
    save_path = os.path.abspath(f"doiscaper_results_{index}-batch.csv")
    results.to_csv(save_path, index=False)
    print(f"Results saved to {save_path}.")







       
