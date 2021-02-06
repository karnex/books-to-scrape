import requests

from bs4 import BeautifulSoup


def category_page(category_page):
    """
    From the category page, extract and return every product URL as a list
    """
    another_page = True  # Useful bool for the loop
    list_to_return = []  # List that will be returned
    i = 1  # var to increment

    while another_page:

        if i > 1:
            response = requests.get(category_page.replace('index.html', 'page-' + str(i) + '.html'))
        else:            
            response = requests.get(category_page)

        # When a valid response is returned
        if response.ok:

            # Parse the returned content and initialize the list to return
            soup = BeautifulSoup(response.text, 'html.parser')

            product_tags = soup.find('section').findAll('div', {'class': 'image_container'})

            for url in product_tags:
                product_page = category_page + '/../' + str(url.find('a')['href'])
                list_to_return.append(product_page)

            i += 1       

        # Otherwise when an error is occured
        else:

            # Leave the loop
            another_page = False
            
    # Finally, return the list
    return list_to_return
