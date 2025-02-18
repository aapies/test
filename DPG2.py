import streamlit as st
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

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

# Fetch and print the HTML source of the page
def print_html():
    driver = get_driver()
    driver.get("https://httpbin.org/ip")

    # Get the page source and print it
    page_source = driver.page_source
    driver.quit()
    
    # Display the page source as pretty-printed HTML in Streamlit
    st.code(page_source, language='html')

# Display the HTML in Streamlit
if st.button("Show HTML Source"):
    print_html()
