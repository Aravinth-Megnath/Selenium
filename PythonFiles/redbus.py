from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import time
from selenium.webdriver.support import expected_conditions as EC

# Initialize the WebDriver
driver = webdriver.Firefox()  # Replace with your ChromeDriver path


# Open the RedBus website
driver.get("https://www.redbus.in/")

# Optional: Maximize the browser window
driver.maximize_window()

# Wait for the element to be present
wait = WebDriverWait(driver, 10)
element = wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/section/div[2]/main/div[3]/div[3]/div[2]/div/div[1]/div[1]/div[1]/div[2]/div[1]/div[1]")))

# Scroll the element into view using JavaScript
driver.execute_script("arguments[0].scrollIntoView(true);", element)

# Wait for the element to be clickable
clickable_element = wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/section/div[2]/main/div[3]/div[3]/div[2]/div/div[1]/div[1]/div[1]/div[2]/div[1]/div[1]")))

# Click the element using JavaScript
driver.execute_script("arguments[0].click();", clickable_element)

# Wait for the second element to be present
second_element_xpath = "/html/body/div[1]/div/div[4]/div[2]/div[1]/a"
second_element = wait.until(EC.presence_of_element_located((By.XPATH, second_element_xpath)))

# Scroll the second element into view using JavaScript
driver.execute_script("arguments[0].scrollIntoView(true);", second_element)

# Wait for the second element to be clickable
clickable_second_element = wait.until(EC.element_to_be_clickable((By.XPATH, second_element_xpath)))

# Click the second element using JavaScript
driver.execute_script("arguments[0].click();", clickable_second_element)
 # Scroll down to ensure that elements with the specified class are in view
# Scroll down in steps to ensure all content is loaded
last_height = driver.execute_script("return document.body.scrollHeight")
while True:
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)  # Wait to load the page
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height

# Find all elements with the class name "travels lh-24 f-bold d-color"
elements = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "travels")))

# Print the text of the first three elements
for element in elements:
    print(element.text)

# Keep the browser open for some time to observe the result
    

# Additional actions can be added here

# Keep the browser open for some time to observe the result
import time
time.sleep(10)