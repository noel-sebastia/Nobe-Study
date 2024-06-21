import os
from flask import Flask, render_template, request
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time

app = Flask(__name__)

def get_youtube_videos(channel_url):
    # Setup Selenium WebDriver
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    try:
        # Navigate to the YouTube channel URL
        driver.get(channel_url)
        
        # Wait until the page is fully loaded
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'a#video-title'))
        )
        
        # Get page source and parse with BeautifulSoup
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        
        # Extract video details
        videos = []
        for video in soup.select('a#video-title'):
            title = video.get('title')
            url = 'https://www.youtube.com' + video.get('href')
            videos.append({'title': title, 'url': url})
        
    finally:
        driver.quit()
    
    return videos

@app.route('/', methods=['GET', 'POST'])
def index():
    videos = []
    channel_url = ''
    if request.method == 'POST':
        channel_url = request.form['channel_url']
        videos = get_youtube_videos(channel_url)
    return render_template('index.html', videos=videos, channel_url=channel_url)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 4000))
    app.run(host="0.0.0.0", port=port)
