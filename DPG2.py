import streamlit as st
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# SCRAPERAPI_KEY from Streamlit secrets
SCRAPERAPI_KEY = "542c23a8f94fa76d41106eff0fad63c6"
proxy = f"http://scraperapi:{SCRAPERAPI_KEY}@proxy-server.scraperapi.com:8001"

# ✅ Caching WebDriver instance for better performance
@st.cache_resource
def get_driver():
    options = Options()
    options.add_argument(f"--proxy-server={proxy}") 
    options.add_argument("--disable-gpu")
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")  # Helps with memory issues

    # ✅ Use a real User-Agent to bypass bot detection
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
    options.add_argument(f"user-agent={user_agent}")

    service = Service(ChromeDriverManager(chrome_type="chromium").install())
    driver = webdriver.Chrome(service=service, options=options)
    return driver

# Open the page showing your IP address
def show_ip():
    driver = get_driver()
    driver.get("https://httpbin.org/ip")

    # Wait for the element with the class 'objectBox objectBox-string' to be present
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "objectBox-objectBox-string"))
    )

    # Use a more specific CSS selector to target the IP address
    ip_address_element = driver.find_element(By.CSS_SELECTOR, ".objectBox.objectBox-string")
    ip_address = ip_address_element.text
    
    driver.quit()
    return ip_address


# Display the IP Address in Streamlit
if st.button("Get My IP Address"):
    ip = show_ip()
    st.write(f"My IP Address is: {ip}")
