import requests
from bs4 import BeautifulSoup
from time import sleep
import pandas as pd

def get_url(url):
    """Get parsed HTML from url
      Input: url to the webpage
      Output: Parsed HTML text of the webpage
    """
    # Send Get request to server to get data
    r = requests.get(url)

    # Parse HTML text
    soup = BeautifulSoup(r.text, 'html.parser')
    
    # return soup object
    return soup

def scrape_tiki(url='https://tiki.vn/may-tinh-bang/c1794?src=c.1789.hamburger_menu_fly_out_banner'):
    """Scrape info of products in Laptop-PC"""
    
    # Begin with page 1
    page = 1
    
    # Get parsed HTML by calling get_url function
    soup = get_url(url)
           
    # Find all products on page 1
    # products = soup.find_all('div', {'class':'product-item'})
    
    # Store product info in a list
    data = []
    
    # Loop through pages
    #while products != None and page < 15:
    while True:    
        # Update url to contain '&page=', convert page to string for string concatenation
        url = url + '&page=' + str(page)
        
        # Get parsed HTML of current page
        soup = get_url(url)
        
        # Find all products on current page
        products = soup.find_all('div', {'class':'product-item'})
        
        # Extract info of each product
        for product in products:    
            d = {'Category':'',
             'Name':'',
             'Final_price':'',
             'Regular_price':'',
             'Discount_percent':'',
             'Installment':'',
             'Cross_border':'',
             'Sponsor':'',
             'Reviews':'',
             'Rating':'',
             'Rating_by_stars':'',
             'Url':'',
             'Image_url':''}
            
            # User try block for not terminate whole program due to error 
            try:
                # Extract product's category
                d['Category'] = product['data-category']
                #print(d['Category'])
                
                # Extract product's name
                d['Name'] = product['data-title']
                #print(d['Name'])
                
                # Extract product's url, prefix with 'https://tiki.vn'
                d['Url'] = 'https://tiki.vn' + product.a['href']
                #print(d['Url'])
                
                # Extract product's image url
                d['Image_url'] = product.find('img', {'class':'product-image img-responsive'})['src']
                #print(d['Image'])
                
                # Use try block to catch case No Discount
                try:
                    # Extract all text of <p class='price-sale'>, split it and convert to a list of integers, extract values of final rice, regular price and discount percent respectively
                    d['Final_price'] = int(list(product.find('p', {'class':'price-sale'}).text.split())[0].replace('đ', '').replace('.', '', -1))
                    #print(d['Final_Price'])
                    d['Regular_price'] = int(list(product.find('p', {'class':'price-sale'}).text.split())[2].replace('đ', '').replace('.', '', -1))
                    #print(d['Regular_Price'])
                    d['Discount_percent'] = int(list(product.find('p', {'class':'price-sale'}).text.split())[1].replace('-', '').replace('%',''))
                except:
                    # If there is no discount, set the regular price = final price, set discount percent = 0
                    d['Regular_price'] = d['Final_price']
                    d['Discount_percent'] = 0
                
                # If installment is available, set installment = YES if not set installment = NO
                if product.find('p', {'class':'installment'}):
                    installment = 'YES'
                else:
                    installment = 'NO'
                d['Installment'] = installment
                #print(d['Installment'])
                
                # If category's text include string 'Quốc Tế', set is_cross_border = YES, if not set is_cross_border = NO
                if 'Quốc Tế' in d['Category']:
                    is_cross_border = 'YES'
                else:
                    is_cross_border = 'NO'
                d['Cross_border'] = is_cross_border
                #print(d['Cross_border'])
                
                # If text in <div class='ship-label-wrapper'> include string 'Tài trợ', sponsor = YES, if not set sponsor = NO
                if 'Tài trợ' in product.find('div', {'class':'ship-label-wrapper'}).text:
                    sponsor = 'YES'
                else:
                    sponsor = 'NO'
                #print(sponsor)

                d['Sponsor'] = sponsor
                
                # Use try block to catch case No rating
                try:
                    # Caculate the rating base on the width of star bar
                    # Extract the width, select only the number and convert to integer
                    d['Rating'] = int(product.find('span', {'class':'rating-content'}).span['style'][6:-1])
                    # Calculate number of stars base on rating value
                    d['Rating_by_stars'] = d['Rating'] * 5 / 100
                except:
                    # If there's no rating, set rating = 0
                    d['Rating'] = 0

                # No rating means no review, no rating == no review == no star
                if d['Rating'] == 0:
                    d['Reviews'] = 0
                    d['Rating_by_stars'] = 0
                else:
                    # Get the text in <p class='review'>, format it to get only number then convert to int
                    d['Reviews'] = int(product.find('p', {'class':'review'}).text.replace('(', '').split()[0])
                
                # add product's info in data list
                data.append(d)
            
            # Print some useful information for debugging in case cannot extract data 
            except:
                print('Cannot retrieve information')
                #print(page)
                #print(d['Name'])
                #print(d['Discount_percent'])
        
        # If tag <div class='product-box-list'> doesn't contain any item stop scraping
        product_list = soup.find('div', {'class':'product-box-list'}).find('div', {'class': 'product-item'})
        #print(product_list)
        if product_list == None:
            break
            
        # Increase page
        page += 1
        print(page)
        
        #Avoid getting banned by Tiki
        sleep(3)
        
    # Return data list
    return data

