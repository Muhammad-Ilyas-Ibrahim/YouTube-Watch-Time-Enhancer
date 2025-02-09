# YouTube Watch Time Enhancer

[![GitHub Repo](https://img.shields.io/badge/GitHub-Repository-blue?logo=github)](https://github.com/Muhammad-Ilyas-Ibrahim/YouTube-Watch-Time-Enhancer)

A Python automation tool that **scrapes YouTube videos from channels and enhances watch time** by automatically playing them in a browser. This project leverages **Selenium, BeautifulSoup, and yt-dlp** to gather video data and simulate video watching.

---

## 🚀 Features

✅ **Scrape Videos**: Extract video titles and URLs from YouTube channels.  
✅ **Auto-Play Videos**: Opens and plays YouTube videos in the browser.  
✅ **Simulates Watch Time**: Waits for the video duration before moving to the next.  
✅ **Headless Execution**: Runs in the background without opening a visible browser.  
✅ **CSV Export**: Saves scraped video data for later use.  

---

## 🛠️ Tech Stack

- **Python** 🐍
- **Selenium** (Web Automation)  
- **BeautifulSoup** (Web Scraping)  
- **yt-dlp** (Extract video metadata)  
- **Pandas** (CSV Handling)  

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
1. The script **scrapes video links** from YouTube channels.
2. Saves the extracted videos into a CSV file (`scraped_videos.csv`).
3. Reads video URLs from the CSV and **automatically plays them**.
4. Waits for the **full duration** of each video before moving to the next.

---

## 📌 Configuration

You can modify the YouTube **channel URLs** in `main.py`:

```python
channel_url_1 = "https://www.youtube.com/@techwizard137/videos"
channel_url_2 = "https://www.youtube.com/@360sakuragaming/videos"
```

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
