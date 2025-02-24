from selenium import webdriver
import pandas as pd
from io import StringIO

# Initialize the Chrome driver
driver = webdriver.Chrome()

# Navigate to the Wikipedia page
driver.get("https://en.wikipedia.org/wiki/List_of_countries_by_GDP_(nominal)")

# Read the HTML tables from the page
tables = pd.read_html(StringIO(driver.page_source))

# Print the number of tables found
print(f"Number of tables found: {(tables)}")

# You can access specific tables by index, for example:
# print(tables[0])  # First table

# Close the browser
driver.quit()