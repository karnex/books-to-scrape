import requests

from bs4 import BeautifulSoup


def home_page(home_page):
    """
    From the product page, extract and return some useful data as a dict
    """
    response = requests.get(home_page)

    # When a valid response is returned
    if response.ok:

        # Parse the returned content and initialize the dictionary to return
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract useful data and ad them into the dictionary
        category_tags = soup.find('ul', {'class': 'nav-list'}).find('ul').findAll('a')

        dict_to_return = {}

        for category_tag in category_tags:

            dict_to_return.update({category_tag.text: home_page + category_tag['href']})

        # Finally, return the dictionary
        return dict_to_return

    # Otherwise when an error is occured, return an exception with the status code
    else:

        raise Exception(response.status_code)
