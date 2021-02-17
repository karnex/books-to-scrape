import os
import pathlib

from collect_data import collect_category_url_from_homepage, \
    collect_product_url_from_category, collect_data_from_product, \
    save_thumbnail, save_csv

# Project directories
PROJECT_DIRECTORY = pathlib.Path().absolute()
CSV_DIRECTORY = os.path.join(PROJECT_DIRECTORY, 'csv')


def main():
    # Get every categories as a dict
    ctg_dict = collect_category_url_from_homepage('http://books.toscrape.com/')

    for key, value in ctg_dict.items():  # Loop on the categories dict

        # Get every product URLs as a list
        product_list = collect_product_url_from_category(value)

        # Loop on each product from a category
        for product_page in product_list:

            # Get every data from a product page
            data_dict = collect_data_from_product(product_page)

            # Declare the current csv file
            csv_file = os.path.join(CSV_DIRECTORY, key + '.csv')

            try:
                save_csv(data_dict, csv_file)
            except Exception as e:
                print(e)
                pass

            try:
                save_thumbnail(data_dict['category'],
                               data_dict['universal_product_code'],
                               data_dict['image_url'])
            except Exception as e:
                print(e)
                pass


if __name__ == '__main__':

    # Execute the main function containing the scraping workflow
    main()
