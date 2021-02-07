import os
import pathlib
import urllib
import requests

from bs4 import BeautifulSoup

# Project directories
PROJECT_DIRECTORY = pathlib.Path().absolute()
PRODUCTS_DIRECTORY = os.path.join(PROJECT_DIRECTORY, 'products')
THUMBNAILS_DIRECTORY = os.path.join(PRODUCTS_DIRECTORY, 'thumbnails')


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

        dict_to_return = {}

        for category_tag in category_tags:

            # dict_to_return.update({category_tag.text: home_page + category_tag['href']})
            dict_to_return[category_tag.text] = home_page + category_tag['href']

        # Finally, return the dictionary
        return dict_to_return

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

            for product_tag in product_tags:
                list_to_return.append(category_page + '/../' + product_tag.find('a')['href'])

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

        # Parse the returned content and initialize the dictionary to return
        soup = BeautifulSoup(response.text, 'html.parser')
        dict_to_return = {'product_page_url': product_page}

        # Extract useful data and add them into the dictionary
        upc = soup.find('table', {'class': 'table-striped'}).findAll('td')[0].text
        dict_to_return.update({'universal_product_code': upc})

        title = soup.find('div', {'class': 'product_main'}).find('h1').text
        dict_to_return.update({'title': title})

        price_incl_tax = soup.find('table', {'class': 'table-striped'}).findAll('td')[3].text
        dict_to_return.update({'price_including_tax': price_incl_tax})

        price_excl_tax = soup.find('table', {'class': 'table-striped'}).findAll('td')[2].text
        dict_to_return.update({'price_excluding_tax': price_excl_tax})

        availability = soup.find('table', {'class': 'table-striped'}).findAll('td')[5].text
        dict_to_return.update({'number_available': availability})

        description = soup.find('article', {'class': 'product_page'}).findAll('p')[3].text
        dict_to_return.update({'product_description': description})

        category = soup.find('ul', {'class': 'breadcrumb'}).findAll('li')[2].find('a').text
        dict_to_return.update({'category': category})

        review = soup.find('div', {'class': 'product_main'}).find('p', {'class': 'star-rating'})['class'][1]
        dict_to_return.update({'review_rating': review})

        img_url = soup.find('div', {'thumbnail'}).find('img')['src']
        dict_to_return.update({'image_url': product_page + '/../' + img_url})

        # Save that image and rename the filename with the book title
        filename = title.replace(' ', '').replace('\n', '') + str(os.path.splitext(img_url)[1])

        # Declare the category directory and create it when needed
        category_directory = os.path.join(THUMBNAILS_DIRECTORY, category)
        if not os.path.exists(category_directory):
            os.mkdir(category_directory)

        try:
            urllib.request.urlretrieve(product_page + '/../' + img_url, os.path.join(category_directory, filename))
        except Exception as e:
            print(e)
            pass

        # Finally, return the dictionary
        return dict_to_return

    # Otherwise when an error occurs, return an exception with the status code
    else:

        raise Exception(response.status_code)