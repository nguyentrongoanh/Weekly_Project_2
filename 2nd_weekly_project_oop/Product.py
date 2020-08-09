from DatabaseUtilities import connection

db = connection()

class Product:
    def __init__(self, category, name, final_price, regular_price, 
                 discount_percentage, installment, cross_border, 
                 sponsor, reviews, rating, rating_by_stars, url, image_url, product_id=None):
        self.product_id = product_id
        self.category = category
        self.name = name
        self.final_price = final_price
        self.regular_price = regular_price
        self.discount_percentage = discount_percentage
        self.installment = installment
        self.cross_border = cross_border
        self.sponsor = sponsor
        self.reviews = reviews
        self.rating = rating
        self.rating_by_stars = rating_by_stars
        self.url = url
        self.image_url = image_url
        
    def __repr__(self):
        return f"ID: {self.product_id}, Category: {self.category}, Name: {self.name}, Final Price: {self.final_price}, Regular Price: {self.regular_price}"
    
    def save_into_db(self, conn=db):
        query = """
            INSERT INTO products (category, name, final_price,
                                    regular_price, discount_percentage,
                                    installment, cross_border, sponsor,
                                    reviews, rating, rating_by_stars, url, image_url)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
        """
        val = (self.category, self.name, self.final_price,
                  self.regular_price, self.discount_percentage,
                  self.installment, self.cross_border, self.sponsor,
                  self.reviews, self.rating, self.rating_by_stars, self.url, self.image_url)
        try:
            cur = conn.cursor()
            cur.execute(query, val)
            self.product_id = cur.lastrowid
            conn.commit()
        except Exception as err:
            print('ERROR BY INSERT:', err)