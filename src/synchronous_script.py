import csv
import json
import time
import requests
from bs4 import BeautifulSoup


def save_product(book_name, product_info):
    json_file_name = book_name.replace(' ', '_')
    with open(f'data/{json_file_name}.json', 'w') as book_file:
        json.dump(product_info, book_file)


def scrape(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    book_name = soup.select_one('.product_main').h1.text
    rows = soup.select('.table.table-striped tr')
    product_info = {row.th.text: row.td.text for row in rows}
    save_product(book_name, product_info)


def main():
    start_time = time.time()

    print('Saving the output of extracted information')
    with open('urls.csv') as file:
        csv_reader = csv.DictReader(file)
        for csv_row in csv_reader:
            scrape(csv_row['url'])

    time_difference = time.time() - start_time
    print(f'Scraping time: %.2f seconds.' % time_difference)


main()
