import requests

from bs4 import BeautifulSoup


def product_page(product_page):
    """
    From the product page, extract and return some useful data as a dict
    """
    response = requests.get(product_page)

    # When a valid response is returned
    if response.ok:

        # Parse the returned content and initialize the dictionary to return
        soup = BeautifulSoup(response.text, 'html.parser')
        dict_to_return = {'product_page_url': product_page}

        # Extract useful data and add them into the dictionary
        upc = soup.find('table', {'class': 'table-striped'}).findAll('td')[0].text
        dict_to_return.update({'universal_product_code': upc})
        title = soup.find('div', {'class': 'product_main'}).find('h1').text
        dict_to_return.update({'title': title})
        price_incl_tax = soup.find('table', {'class': 'table-striped'}).findAll('td')[3].text.replace('Â', '')
        dict_to_return.update({'price_including_tax': price_incl_tax})
        price_excl_tax = soup.find('table', {'class': 'table-striped'}).findAll('td')[2].text.replace('Â', '')
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

        # Finally, return the dictionary
        return dict_to_return

    # Otherwise when an error occurs, return an exception with the status code
    else:

        raise Exception(response.status_code)
