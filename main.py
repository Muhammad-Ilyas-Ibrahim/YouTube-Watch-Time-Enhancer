import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager 
from bs4 import BeautifulSoup
import yt_dlp

# Global Variables 
url_file = 'scraped_videos.csv'
channel_url_1 = "https://www.youtube.com/@techwizard137/videos"
channel_url_2 = "https://www.youtube.com/@360sakuragaming/videos"

base_url = "https://youtube.com"
global page_source
global scraped_data
scraped_data = []

def open_channel_and_retrieve_page_source(channel_url):
    global page_source
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--disable-extensions")
    
    # Automatically download and set up ChromeDriver using webdriver-manager
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    # Open the YouTube channel page
    driver.get(channel_url)

    # Scroll to the bottom of the page to load all videos
    last_height = driver.execute_script("return document.documentElement.scrollHeight")
    scroll_pause_time = 5  # Time to wait after scrolling

    while True:
        # Scroll down to the bottom
        driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")

        # Wait to load the new content
        time.sleep(scroll_pause_time)

        # Calculate new scroll height and compare with the last height
        new_height = driver.execute_script("return document.documentElement.scrollHeight")
        if new_height == last_height:
            break  # Exit the loop when no more new content is loaded
        last_height = new_height

    # Get page source after all videos have been loaded
    page_source = driver.page_source

    # Close the browser
    driver.quit()

def scrape_videos_data():
    global scraped_data
    # Use BeautifulSoup to parse the page source
    soup = BeautifulSoup(page_source, "html.parser")

    # Find all video elements
    videos = soup.find_all('a', id='video-title-link')

    # Prepare data to export
    for video in videos:
        video_title = video['aria-label'].split(' by ')[0]  # Extract title from 'aria-label'
        video_url = base_url + video['href']  # Create full URL
        scraped_data.append([video_title, video_url])


def write_scraped_data_to_csv():
    global scraped_data
    # Convert the scraped data into a DataFrame
    df = pd.DataFrame(scraped_data, columns=['Title', 'URLs'])
    print("Number of rows: ", df.shape[0])
    
    # Export the DataFrame to a CSV file using pandas
    csv_file = "scraped_videos.csv"
    df.to_csv(csv_file, index=False, encoding='utf-8')

    print(f"Scraped data saved to {csv_file}")

def get_video_duration(youtube_url):
    try:
        ydl_opts = {
            'quiet': True,
            'skip_download': True,  # Skip the actual download
            'extract_flat': True,  # Extract metadata only
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(youtube_url, download=False)
            return info_dict.get('duration', None)  # Returns duration in seconds or None if not found

    except Exception as e:
        print(f"Error getting duration for {youtube_url}: {e}")
        return None

if __name__ == '__main__':
    
    open_channel_and_retrieve_page_source(channel_url_1)
    scrape_videos_data()
    open_channel_and_retrieve_page_source(channel_url_2)
    scrape_videos_data()
    write_scraped_data_to_csv()
    
    # Read URLs from CSV
    urls_df = pd.read_csv(url_file)

    # Get the list of URLs from the 'URLs' column
    youtube_links = urls_df['URLs'].tolist()

    # Set up Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--start-maximized")  # Open browser in maximized mode
    chrome_options.add_argument("--disable-extensions")  # Disable extensions for cleaner execution

    # Automatically download and set up ChromeDriver using webdriver-manager
    service = Service(ChromeDriverManager().install())

    # Initialize the WebDriver using the service and options
    driver = webdriver.Chrome(service=service, options=chrome_options)

    # Loop through each YouTube video link
    for link in youtube_links:
        try:
            # Get video duration
            duration = get_video_duration(link)
            
            print(f'Opening {link}')
            print("Video duration: ", duration)
            
            duration = int(duration)
            
            # Open the video using Selenium
            driver.get(link)
            time.sleep(5)  # Let the page load for a few seconds
            driver.refresh()  # Refresh the page to ensure video loads properly

            # Wait for the video to finish playing
            time.sleep(duration)
        except Exception as e:
            print(f"An error occurred with {link}: {e}")

    # Close the browser after watching all videos
    driver.quit()
