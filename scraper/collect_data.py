import os
import pathlib
import requests
import urllib

from bs4 import BeautifulSoup

# Project directories
PROJECT_DIRECTORY = pathlib.Path().absolute()
PRODUCTS_DIRECTORY = os.path.join(PROJECT_DIRECTORY, 'products')
THUMBNAILS_DIRECTORY = os.path.join(PRODUCTS_DIRECTORY, 'thumbnails')


def save_csv(data_frame, csv_file):
    """
    From the data frame and the scsv file name, add data into the csv file
    """
    if os.path.exists(csv_file):

        # Append data into the existing csv file
        data_frame.to_csv(csv_file, mode='a', header=False)

    else:

        # Create the csv file and add data inside
        data_frame.to_csv(csv_file)


def save_thumbnail(data_dict):
    """
    From the data dictionary, save the thumbnail to a local directory
    """
    # Save that image and rename the filename with the book title
    filename = data_dict['title'].replace(' ', '').replace('\n', '').replace('/', '') + \
               os.path.splitext(data_dict['image_url'])[1]

    # Declare the category directory and create it when needed
    category_directory = os.path.join(THUMBNAILS_DIRECTORY, data_dict['category'])
    if not os.path.exists(category_directory):
        os.mkdir(category_directory)

    try:
        urllib.request.urlretrieve(data_dict['image_url'], os.path.join(category_directory, filename))
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

        # Parse the returned content and initialize the dictionary to return
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract useful data and add them into the dictionary
        category_tags = soup.find('ul', {'class': 'nav-list'}).find('ul').findAll('a')

        # Finally, return a dictionary with the category as key and the category URL as value
        return {category_tag.text: home_page + category_tag['href'] for category_tag in category_tags}

    # Otherwise when an error is occurs, return an exception with the status code
    else:

        raise Exception(response.status_code)


def collect_product_url_from_category(category_page):
    """
    From the category page, colelct and return every product URL as a list
    """
    list_to_return = []  # List that will be returned
    i = 1  # var to increment

    while True:

        if i > 1:
            response = requests.get(category_page.replace('index.html', f'page-{i}.html'))
        else:
            response = requests.get(category_page)

        # When a valid response is returned
        if response.ok:

            # Format the response to encoding utf-8
            response.encoding = 'utf-8'

            # Parse the returned content and initialize the list to return
            soup = BeautifulSoup(response.text, 'html.parser')

            product_tags = soup.find('section').findAll('div', {'class': 'image_container'})

            list_to_return += [f"{category_page}/../{product_tag.find('a')['href']}" for product_tag in product_tags]

            i += 1

        # Otherwise when an error is occurs
        else:

            break  # Leave the loop

    # Finally, return the list
    return list_to_return


def collect_data_from_product(product_page):
    """
    From the product page, collect and return some useful data as a dict
    """
    response = requests.get(product_page)

    # When a valid response is returned
    if response.ok:

        # Format the response to encoding utf-8
        response.encoding = 'utf-8'

        # Parse the returned content
        soup = BeautifulSoup(response.text, 'html.parser')
        # Collect useful data
        upc = soup.find('table', {'class': 'table-striped'}).findAll('td')[0].text
        title = soup.find('div', {'class': 'product_main'}).find('h1').text
        price_incl_tax = soup.find('table', {'class': 'table-striped'}).findAll('td')[3].text
        price_excl_tax = soup.find('table', {'class': 'table-striped'}).findAll('td')[2].text
        availability = soup.find('table', {'class': 'table-striped'}).findAll('td')[5].text
        description = soup.find('article', {'class': 'product_page'}).findAll('p')[3].text
        category = soup.find('ul', {'class': 'breadcrumb'}).findAll('li')[2].find('a').text
        review = soup.find('div', {'class': 'product_main'}).find('p', {'class': 'star-rating'})['class'][1]
        img_url = soup.find('div', {'thumbnail'}).find('img')['src']

        # Finally, return a dictionary containing the collected data
        return {'product_page_url': product_page, 'universal_product_code': upc, 'title': title,
                'price_including_tax': price_incl_tax, 'price_excluding_tax': price_excl_tax,
                'number_available': availability, 'product_description': description, 'category': category,
                'review_rating': review, 'image_url': f'{product_page}/../{img_url}'}

    # Otherwise when an error occurs, return an exception with the status code
    else:

        raise Exception(response.status_code)
