# YouTube Watch Time Enhancer

[![GitHub Repo](https://img.shields.io/badge/GitHub-Repository-blue?logo=github)](https://github.com/Muhammad-Ilyas-Ibrahim/YouTube-Watch-Time-Enhancer)

A Python automation tool that **scrapes YouTube videos from channels and enhances watch time** by automatically playing them in a browser. This project leverages **Selenium, BeautifulSoup, and yt-dlp** with advanced features like multi-threading and video chunk splitting for optimal performance.

---

## 🚀 Features

✅ **Multi-threaded Video Processing**: Parallel processing of video data for faster execution  
✅ **Long Video Splitting**: Automatically splits videos longer than 20 minutes into manageable chunks  
✅ **Auto-Retry Mechanism**: Continuously runs even with connectivity issues  
✅ **Discord Integration**: Sends notifications about video playback status  
✅ **Scrape Videos**: Extract video titles and URLs from YouTube channels  
✅ **Auto-Play Videos**: Opens and plays YouTube videos in the browser  
✅ **Simulates Watch Time**: Waits for the video duration before moving to the next  
✅ **Headless Execution**: Runs in the background without opening a visible browser  
✅ **CSV Export**: Saves scraped video data with smart thread-safe operations  

---

## 🛠️ Tech Stack

- **Python** 🐍
- **Selenium** (Web Automation)  
- **BeautifulSoup** (Web Scraping)  
- **yt-dlp** (Extract video metadata)  
- **Pandas** (CSV Handling)  
- **ThreadPoolExecutor** (Parallel Processing)
- **Discord Webhooks** (Notifications)

---

## 📌 Installation

### **1. Clone the Repository**
```sh
git clone https://github.com/Muhammad-Ilyas-Ibrahim/YouTube-Watch-Time-Enhancer.git
cd YouTube-Watch-Time-Enhancer
```

### **2. Install Dependencies**
```sh
pip install -r requirements.txt
```

> **Note**: The script uses **webdriver-manager** to automatically install ChromeDriver.

---

## 🎯 Usage

### **Run the Script**
```sh
python main.py
```

### **How It Works**
1. The script **scrapes video links** from YouTube channels
2. **Processes videos in parallel** using multi-threading for faster execution
3. **Splits long videos** into 20-minute chunks for better management
4. Saves the extracted videos into a CSV file (`scraped_videos.csv`)
5. Reads video URLs from the CSV and **automatically plays them**
6. **Sends Discord notifications** for video playback status
7. **Auto-retries** on connection failures

### **Advanced Features**

#### Multi-threading
- Uses ThreadPoolExecutor for parallel video processing
- Implements thread-safe CSV operations
- Optimizes performance with up to 32 concurrent threads

#### Video Chunk Splitting
- Automatically splits videos longer than 20 minutes
- Creates manageable chunks with proper time stamps
- Maintains playback continuity across chunks

#### Auto-Retry Mechanism
- Continuously runs even with internet issues
- Implements smart error handling and recovery
- Waits 10 seconds before retrying on failures

---

## 📌 Configuration

You can modify the YouTube **channel URLs** in `main.py`:

```python
channel_url_1 = "https://www.youtube.com/@techwizard137/videos"
channel_url_2 = "https://www.youtube.com/@360sakuragaming/videos"
```

Configure Discord webhook URL for notifications in the `send_to_discord` function.

---

## ⚠️ Disclaimer

This project is for **educational purposes only**.  
Using automation to manipulate YouTube metrics may violate their **Terms of Service**. Use responsibly.

---

## 📜 License

This project is open-source and available under the **MIT License**.

---

## 🌟 Contributing

Contributions are welcome! Feel free to **fork** the repo and submit a **pull request**.
