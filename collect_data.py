import csv
import os
import pathlib
import requests
import urllib.request

from bs4 import BeautifulSoup

# Project directories
PROJECT_DIRECTORY = pathlib.Path().absolute()
THUMBNAILS_DIRECTORY = os.path.join(PROJECT_DIRECTORY, 'thumbnails')


def save_csv(data_dict, csv_file):
    """
    From the data dictionary and the scsv file name, add data into the csv file
    """
    if os.path.exists(csv_file):
        # Append data into the existing csv file
        access_right = 'a'
    else:
        # Create the csv file and add data inside
        access_right = 'w'

    with open(csv_file, access_right, newline='\n', errors='replace') as file:
        writer = csv.DictWriter(file, delimiter=';', fieldnames=[
            'product_page_url', 'universal_product_code', 'title',
            'price_including_tax', 'price_excluding_tax', 'number_available',
            'product_description', 'category', 'review_rating', 'image_url'])
        if access_right == 'w':
            writer.writeheader()

        writer.writerow(data_dict)


def save_thumbnail(folder_name, filename, img_url):
    """
    From the data dictionary, save the thumbnail to a local directory
    """
    # Save that image and rename the filename with the book upc
    final_name = filename + os.path.splitext(img_url)[1]

    # Declare the directory and create it when needed
    ctg_directory = os.path.join(THUMBNAILS_DIRECTORY, folder_name)
    if not os.path.exists(ctg_directory):
        os.mkdir(ctg_directory)

    try:
        urllib.request.urlretrieve(img_url,
                                   os.path.join(ctg_directory, final_name))
    except Exception as e:
        print(e)
        pass


def collect_category_url_from_homepage(home_page):
    """
    From the home page, collect and return some useful data as a dict
    """
    response = requests.get(home_page)

    # When a valid response is returned
    if response.ok:

        # Format the response to encoding utf-8
        response.encoding = 'utf-8'

        # Parse the returned content
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract useful data and add them into the dictionary
        category_tags = soup.find(
            'ul', {'class': 'nav-list'}).find('ul').findAll('a')

        # Return a dict with the category name as key and the URL as value
        return {ctg_tag.text.strip(): home_page + ctg_tag['href']
                for ctg_tag in category_tags}

    # Otherwise when an error occurs, return the status code as an exception
    else:

        raise Exception(response.status_code)


def collect_product_url_from_category(ctg_page):
    """
    From the category page, collect and return every product URL as a list
    """
    list_to_return = []  # List that will be returned
    i = 1  # var to increment

    while True:

        # According to the current page, get the response
        curr_page = ctg_page if i <= 1 else ctg_page.replace('index.html',
                                                             f'page-{i}.html')
        response = requests.get(curr_page)

        # When a valid response is returned
        if response.ok:

            # Format the response to encoding utf-8
            response.encoding = 'utf-8'

            # Parse the returned content and initialize the list to return
            soup = BeautifulSoup(response.text, 'html.parser')

            product_tags = soup.find(
                'section').findAll('div', {'class': 'image_container'})

            list_to_return += [f"{ctg_page}/../{product_tag.find('a')['href']}"
                               for product_tag in product_tags]

            i += 1

        # Otherwise, when an error occurs
        else:

            break  # Leave the loop

    # Finally, return the list
    return list_to_return


def collect_data_from_product(product_page):
    """
    From the product page, collect and return some useful data as a dict
    """
    response = requests.get(product_page)

    # When the success status is returned
    if response.ok:

        # Format the response to encoding utf-8
        response.encoding = 'utf-8'

        # Parse the returned content
        soup = BeautifulSoup(response.text, 'html.parser')

        # Collect useful data
        upc = soup.find(
            'table', {'class': 'table-striped'}).findAll('td')[0].text
        title = soup.find('div', {'class': 'product_main'}).find('h1').text
        price_incl_tax = soup.find(
            'table', {'class': 'table-striped'}).findAll('td')[3].text
        price_excl_tax = soup.find(
            'table', {'class': 'table-striped'}).findAll('td')[2].text
        availability = soup.find(
            'table', {'class': 'table-striped'}).findAll('td')[5].text
        description = soup.find(
            'article', {'class': 'product_page'}).findAll('p')[3].text
        category = soup.find(
            'ul', {'class': 'breadcrumb'}).findAll('li')[2].find('a').text
        review = soup.find(
            'div', {'class': 'product_main'}).find(
            'p', {'class': 'star-rating'})['class'][1]
        img_url = soup.find('div', {'thumbnail'}).find('img')['src']

        # Finally, return a dictionary containing the collected data
        return {'product_page_url': product_page,
                'universal_product_code': upc, 'title': title,
                'price_including_tax': price_incl_tax,
                'price_excluding_tax': price_excl_tax,
                'number_available': availability,
                'product_description': description, 'category': category,
                'review_rating': review,
                'image_url': f'{product_page}/../{img_url}'}

    # Otherwise when an error occurs, return the status code as an exception
    else:

        raise Exception(response.status_code)
