# books-to-scrape

###### The goal of the repository is to scrape the content of the each product page from books.toscrape.com

#### How to configure the project

1. Into the terminal, go to the directory of your choice: `cd path_of_your_choice`
2. Initialize git for the project: `git init`
3. Create the connection with the repository, BTS is the short name as an example: `git remote add BTS https://github.com/karnex/books-to-scrape.git`
4. Clone the repository to the local: `git clone https://github.com/karnex/books-to-scrape.git`
5. Create the virtual environment:
    - For the Windows devices: `python -m venv env`
    - For the Unix devides: `python3 -m venv env`
6. Activate the virtual environment:
    - For the Windows devices: `env\Scripts\activate`
    - For the Unix devices: `source env/bin/activate`
7. Install the requirements:
    - For Windows devices: `pip install -r requirements.txt`
    - For Unix devices: `pip3 install -r requirements.txt`

#### How to use the project

Here wo go ! Once run_scraper.py is running, please find the generated csv files into the **_csv_** directory and the downloaded images into the **_thumbnails_** directory.
- For the Windows devices: `python run_scraper.py`
- For the Unix devices: `python3 run_scraper.py`
