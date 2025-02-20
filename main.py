import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager 
from bs4 import BeautifulSoup
import yt_dlp
import requests
import json
import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from threading import Lock

USERNAME = os.environ.get('USERNAME')
url_file = 'scraped_videos.csv'
channel_url_1 = 'https://www.youtube.com/@360sakuragaming/videos'
channel_url_2 = 'https://www.youtube.com/@techwizard137/videos'  
scraped_data = []
csv_lock = Lock()
driver = None

def get_video_duration(url):
    ydl_opts = {
        'quiet': True,
        'extract_flat': True,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            info = ydl.extract_info(url, download=False)
            return info.get('duration', 0)
        except Exception as e:
            print(f"Error getting video duration: {e}")
            return 0

def open_channel_and_retrieve_page_source(channel_url):
    try:
        chrome_options = Options()
        # chrome_options.add_argument("--headless")
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        driver.get(channel_url)
        time.sleep(5)  # Let the page load
        page_source = driver.page_source
        driver.quit()
        return page_source
    except Exception as e:
        print(f"Error retrieving page source: {e}")
        return None

def scrape_videos_data():
    global scraped_data
    try:
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')
        
        # Find video elements (try multiple selectors as YouTube's structure might vary)
        video_elements = soup.find_all('a', id='video-title-link')
        if not video_elements:
            video_elements = soup.find_all('a', {'class': 'yt-simple-endpoint'})
        
        print(f"Found {len(video_elements)} video elements in the page")
        
        for video in video_elements:
            title = video.get('title', '').strip()
            href = video.get('href', '')
            if href and title and 'watch?v=' in href:
                full_url = f"https://youtube.com{href}"
                print(f"Found video: {title}")
                scraped_data.append([title, full_url])
        
        print(f"Successfully processed {len(scraped_data)} videos")
        
    except Exception as e:
        print(f"Error in scrape_videos_data: {str(e)}")
        print("Page source:", page_source[:500])  # Print first 500 chars for debugging

def send_to_discord(msg):
    webhook_url=''

    # The message you want to send
    message = {
        "content": f"{msg}",
        "username": f"{USERNAME}"
    }

    # Convert the message to JSON format
    data = json.dumps(message)

    # Set the headers to specify that the content type is JSON
    headers = {
        "Content-Type": "application/json"
    }

    # Send the POST request to the webhook URL
    response = requests.post(webhook_url, data=data, headers=headers)

    # Check the response status
    if response.status_code == 204:
        print("Message sent successfully!")
    else:
        print(f"Failed to send message. Status code: {response.status_code}")

def delete_row_from_csv(url):
    df = pd.read_csv(url_file)
    df = df[df['URLs'] != url]
    if len(df) == 0:
        os.remove(url_file)
        return True
    df.to_csv(url_file, index=False)
    return False

def split_video_into_chunks(video_url, video_title, duration):
    chunk_duration = 1200  # 20 minutes in seconds
    chunks = []
    
    if duration > chunk_duration:
        num_chunks = (duration + chunk_duration - 1) // chunk_duration
        for i in range(num_chunks):
            time_param = f"&t={i * chunk_duration}s" if i > 0 else ""
            chunk_url = f"{video_url}{time_param}"
            chunks.append([f"{video_title} (Part {i+1})", chunk_url])
        
        # Save chunks to CSV immediately
        create_or_prepend_to_csv(chunks, url_file)
    else:
        chunks.append([video_title, video_url])
        create_or_prepend_to_csv([[video_title, video_url]], url_file)

    print(f"Chunks: {chunks}")
    return chunks

def create_or_prepend_to_csv(new_data, filename):
    if not new_data:
        return
        
    with csv_lock:
        if os.path.exists(filename):
            existing_df = pd.read_csv(filename)
            new_df = pd.DataFrame(new_data, columns=['Title', 'URLs'])
            combined_df = pd.concat([new_df, existing_df], ignore_index=True)
            combined_df.to_csv(filename, index=False)
        else:
            new_df = pd.DataFrame(new_data, columns=['Title', 'URLs'])
            new_df.to_csv(filename, index=False)

def scroll_and_wait(driver, scroll_times=5):
    for _ in range(scroll_times):
        # Scroll to bottom
        driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
        time.sleep(2)  # Wait for content to load

def process_video(video_data):
    title, url = video_data
    print(f"Getting duration for: {title}")
    duration = get_video_duration(url)
    if duration:
        return split_video_into_chunks(url, title, duration)
    print(f"Could not get duration for: {title}")
    return None

def watch_videos():
    if not os.path.exists(url_file):
        if not channel_url_1 and not channel_url_2:
            print("Please set channel_url_1 and/or channel_url_2 before running")
            return
            
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        service = Service(ChromeDriverManager().install())
        global driver
        driver = webdriver.Chrome(service=service, options=chrome_options)
        
        driver.set_window_size(1920, 1080)
        
        # Perform scraping if CSV doesn't exist
        if channel_url_1:
            print(f"Scraping channel 1: {channel_url_1}")
            try:
                driver.get(channel_url_1)
                time.sleep(5)
                scroll_and_wait(driver)
                scrape_videos_data()
            except Exception as e:
                print(f"Error scraping channel 1: {str(e)}")
            
        if channel_url_2:
            print(f"Scraping channel 2: {channel_url_2}")
            try:
                driver.get(channel_url_2)
                time.sleep(5)
                scroll_and_wait(driver)
                scrape_videos_data()
            except Exception as e:
                print(f"Error scraping channel 2: {str(e)}")
            
        driver.quit()
        
        # Process videos in parallel using ThreadPoolExecutor
        print(f"Processing {len(scraped_data)} videos found...")
        all_chunks = []
        max_workers = min(32, len(scraped_data))  # Use up to 32 threads
        
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            future_to_video = {executor.submit(process_video, video): video for video in scraped_data}
            for future in as_completed(future_to_video):
                video = future_to_video[future]
                try:
                    chunks = future.result()
                    if chunks:
                        all_chunks.extend(chunks)
                except Exception as e:
                    print(f"Error processing video {video[0]}: {str(e)}")
        
        # Save all chunks at once
        if all_chunks:
            create_or_prepend_to_csv(all_chunks, url_file)
        
        if not scraped_data:
            print("No videos were found to process")
            return
            
        print(f"Scraped data saved to {url_file}")
    
    if not os.path.exists(url_file):
        print("No videos file was created. Please check channel URLs and try again")
        return

    # Read URLs from CSV
    urls_df = pd.read_csv(url_file)
    youtube_links = urls_df['URLs'].tolist()
    titles = urls_df['Title'].tolist()

    # Set up Chrome options with muted audio
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--mute-audio")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    for link, title in zip(youtube_links, titles):
        try:
            # Extract time parameter if present
            time_param = 0
            if "&t=" in link:
                time_param = int(link.split("&t=")[1].replace("s", ""))
            
            # Get full video duration
            base_url = link.split("&t=")[0] if "&t=" in link else link
            full_duration = get_video_duration(base_url)
            
            if full_duration:
                print(f'Opening {link}')
                
                # Calculate remaining duration
                remaining_duration = full_duration - time_param
                watch_duration = min(1200, remaining_duration)
                
                print(f"Watching for {watch_duration} seconds")
                send_to_discord(f'**{title}** is being played\nFull Video Duration: {full_duration}\nWatching for {watch_duration} seconds\nURL of Video: {base_url}')
                driver.get(link)
                time.sleep(5)  # Initial buffer
                driver.refresh()
                
                # Wait for calculated duration
                time.sleep(watch_duration)
                
                # Delete the watched chunk from CSV
                if delete_row_from_csv(link):
                    print("All videos watched. CSV file deleted.")
                    break

        except Exception as e:
            print(f"An error occurred with {link}: {e}")

    driver.quit()

if __name__ == "__main__":
    while True:
        try:
            watch_videos()
        except:
            time.sleep(10)