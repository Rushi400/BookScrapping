import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

# Base URL with page number placeholder
base_url = "http://books.toscrape.com/catalogue/page-{}.html"

# List to hold all book data
all_books = []

# Loop through 50 pages (the total number on the website)
for page in range(1, 51):
    print(f"Scraping page {page}...")
    url = base_url.format(page)
    
    try:
        # Get the page content with a User-Agent header
        response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        response.raise_for_status()  # Raise error for bad responses
        
        # Parse HTML content using BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Find all book containers
        books = soup.find_all('article', class_='product_pod')

        # Extract data for each book
        for book in books:
            title = book.h3.a['title']
            price = book.find('p', class_='price_color').text
            rating_class = book.find('p')['class']
            rating = rating_class[1]  # e.g., "Three", "One"
            
            all_books.append({
                "Title": title,
                "Price": price,
                "Rating": rating
            })

        # Polite pause to avoid overwhelming the server
        time.sleep(1)
    
    except Exception as e:
        print(f"Failed to scrape page {page}, error: {e}")

# Convert collected data to a dataframe and save as CSV
df = pd.DataFrame(all_books)
df.to_csv('books.csv', index=False)
print("Scraping complete! Data saved to books.csv")
