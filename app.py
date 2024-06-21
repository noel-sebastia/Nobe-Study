from flask import Flask, render_template, request
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
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
    
    # Navigate to the YouTube channel URL
    driver.get(channel_url)
    time.sleep(5)  # Let the page load completely

    # Get page source and parse with BeautifulSoup
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    driver.quit()

    # Extract video details
    videos = []
    for video in soup.select('a#video-title'):
        title = video.get('title')
        url = 'https://www.youtube.com' + video.get('href')
        videos.append({'title': title, 'url': url})
    
    return videos

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        channel_url = request.form['channel_url']
        videos = get_youtube_videos(channel_url)
        return render_template('index.html', videos=videos, channel_url=channel_url)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True, port=3000)
