import os
import pathlib
import pandas as pd

from scraper.collect_data import collect_category_url_from_homepage, collect_product_url_from_category, \
    collect_data_from_product

# Project directories
PROJECT_DIRECTORY = pathlib.Path().absolute()
PRODUCTS_DIRECTORY = os.path.join(PROJECT_DIRECTORY, 'products')

if __name__ == '__main__':

    # Get every categories as a dict
    category_dict = collect_category_url_from_homepage('http://books.toscrape.com/')

    for key, value in category_dict.items():  # Loop on the categories dict

        # Get every product URLs as a list
        product_list = collect_product_url_from_category(value)

        for product_page in product_list:  # Loop on each product from a category

            # Get every data from a product page
            data_dict = collect_data_from_product(product_page)

            # Declare the current csv file
            filename = key.replace(' ', '').replace('\n', '') + '.csv'
            csv_file = os.path.join(PRODUCTS_DIRECTORY, filename)

            # Generate the DataFrame from the data dictionary
            df = pd.DataFrame([data_dict])

            if os.path.exists(csv_file):

                # Append data into the existing csv file
                df.to_csv(csv_file, mode='a', header=False)

            else:

                # Create the csv file and add data inside
                df.to_csv(csv_file)
