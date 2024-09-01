from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import os
import pandas as pd

# Set up the Chrome WebDriver
os.environ['PATH'] += r"C:\Python"
driver = webdriver.Chrome()

# scrape amazon makeup data
def scrape_amazon_makeup_data(search_query,max_items=4000):
  base_url = f"https://www.amazon.com/s?k={search_query}"
  items_collected = 0
  page = 1
  data = []
  
  while items_collected < max_items:
    url = f"{base_url}&page={page}"
    driver.get(url)
    # wait for page load
    time.sleep(3)
    
    product_containers = driver.find_elements(By.CSS_SELECTOR,'div[data-component-type="s-search-result"]')
    
    for container in product_containers:
      if items_collected >= max_items:
        break
      
      # Extract product details
      
      # Product Title
      try:
       title = container.find_element(By.TAG_NAME,'h2').text.strip()
       print(title)
       
      
        
      except:
        pass  
      
      
      # Product Price
      try:
        price_whole = container.find_element(By.CSS_SELECTOR, 'span.a-price-whole').text
        price_fraction = container.find_element(By.CSS_SELECTOR, 'span.a-price-fraction').text
        price = f"${price_whole}.{price_fraction}"

      except:
        price = 'N/A'
      
      # Product Rating
      try:
        rating = container.find_element(By.CSS_SELECTOR,'div [data-cy="reviews-block"] span').get_attribute("aria-label")
        
      except:
        rating = 'N/A'
      
      # Product image url
      try:
        image_url = container.find_element(By.CSS_SELECTOR,'img.s-image').get_attribute("src")
        
      except:
        pass  
      
      # Product Url
      try:
        product_url = container.find_element(By.CSS_SELECTOR,'a.a-link-normal').get_attribute("href")
        print(product_url)
      except:
        pass          
      
     # Store product data
      data.append({
            'Name': title,
            'Price': price,
            'Rating': rating,
            'Image URL': image_url,
            'Product URL': product_url
            })
      
      items_collected += 1
      
    page += 1
    time.sleep(3)  
    
  # close the broeser
  driver.quit()
  
  # Save the data to an Excel sheet
  df = pd.DataFrame(data)
  df.to_excel("amazon_makeup_products.xlsx", index=False)
    
  
# Run the scraping function
scrape_amazon_makeup_data("makeup")    

print("Scraped data saved to amazon_makeup_products.xlsx")
