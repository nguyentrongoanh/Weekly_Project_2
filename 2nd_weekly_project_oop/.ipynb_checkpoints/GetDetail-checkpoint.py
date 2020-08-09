from Webscraping import *
from Category import Category
from Product import Product
import re

TIKI_URL = 'https://tiki.vn'

def get_main_categories(url, save_db=False):
    soup = get_url(url)

    result = []
    for a in soup.find_all('a', {'class': 'MenuItem__MenuLink-sc-181aa19-1 fKvTQu'}):
        name = a.find('span', {'class': 'text'}).text
        url = a['href']
        main_cat = Category(name, url)

        if save_db:
            main_cat.save_into_db()
        result.append(main_cat)
    return result

def get_sub_categories(parent_category, save_db=False):
    parent_url = parent_category.url
    result = []

    try:
        soup = get_url(parent_url)
        div_containers = soup.find_all('div', {'class':'list-group-item is-child'})
        for div in div_containers:
            name = div.a.text

            # replace more than 2 spaces with one space
            name = re.sub('\s{2,}', ' ', name)

            sub_url = TIKI_URL + div.a['href']
            cat = Category(name, sub_url, parent_category.cat_id)
            if save_db:
                cat.save_into_db()
            result.append(cat)
    except Exception as err:
        print('ERROR BY GET SUB CATEGORIES:', err)
    return result

def get_all_categories(categories):
    if len(categories) == 0:
        return
    for cat in categories:
        sub_categories = get_sub_categories(cat, save_db=True)
        print(sub_categories)
        get_all_categories(sub_categories)

def get_product_details(urls, save_db=True):
#     urls = cur.execute("""SELECT DISTINCT url
#         FROM categories
#         WHERE id
#         NOT IN (
#             SELECT DISTINCT parent_id 
#             FROM categories
#             WHERE parent_id NOTNULL)
#         AND parent_id NOTNULL""").fetchall()
    for url in urls:
         for each in (scrape_tiki(url[0])):
            product = Product(each['Category'], each['Name'], each['Final_price'], each['Regular_price'],
                                 each['Discount_percent'], each['Installment'], each['Cross_border'],
                                 each['Sponsor'], each['Reviews'], each['Rating'], each['Rating_by_stars'],
                                 each['Url'], each['Image_url'])
            if save_db:
                product.save_into_db()