# README.md

## Instagram Hashtag Scraper

This tool allows you to scrape Instagram posts based on hashtags and save the data to a CSV file. It uses an authenticated session token to bypass login restrictions and collects detailed information about posts.

---

## Features
- Scrape up to a specified number of posts using a hashtag.
- Extracts data such as usernames, full names, post URLs, likes, comments, and media links.
- Outputs the data into a `CSV` file for easy usage.

---

## Requirements

- **Python 3.8 or higher**
- Required Python libraries:
  - `requests`
  - `re` (built-in)
  - `json` (built-in)
  - `csv` (built-in)

---

## Installation Guide

### Prerequisites

1. Install Python:
   - **Windows:**
     - Download the latest Python version from [python.org](https://www.python.org/downloads/).
     - During installation, ensure you check the box *"Add Python to PATH"*.
   - **Linux:**
     ```bash
     sudo apt update
     sudo apt install python3 python3-pip
     ```
   - **macOS:**
     - Python 3 comes pre-installed on macOS.
     - Alternatively, you can use Homebrew:
       ```bash
       brew install python3
       ```

2. Install Required Libraries:
   ```bash
   pip install requests
   ```

---

## How to Use

1. **Clone or Download the Repository:**
   Download this project or clone it using:
   ```bash
   git clone <repository-url>
   cd <repository-folder>
   ```

2. **Prepare the `config.json` File:**
   Open the `config.json` file and provide the required values:
   ```json
   {
       "nrOfPosts": 500,
       "hashtag": "<HASHTAG_TO_SCRAPE>",
       "sessiontoken": "<YOUR_IG_SESSIONTOKEN>"
   }
   ```
   - Replace `<HASHTAG_TO_SCRAPE>` with the hashtag you want to scrape (omit the `#` symbol).
   - Replace `<YOUR_IG_SESSIONTOKEN>` with your Instagram session token. (See instructions below for obtaining your session token.)

3. **Run the Script:**
   Execute the Python script:
   ```bash
   python main.py
   ```

4. **Output:**
   - The scraped posts will be saved in a CSV file named `output.csv` in the same directory.

---

## Obtaining Your Instagram Session Token

1. Log in to Instagram using your browser.
2. Open the browser developer tools (usually `F12` or `Ctrl+Shift+I`).
3. Go to the "Network" tab and reload the Instagram page.
4. Filter requests by "Cookies" and locate the `sessionid` cookie in the headers.
5. Copy the `sessionid` value and paste it into the `sessiontoken` field in `config.json`.

---

## Supported Platforms

- **Windows**
- **Linux**
- **macOS**

---

## Notes

- **Rate Limits:** Instagram enforces rate limits. If you scrape too frequently, your account might be flagged.
- **Ethical Usage:** This tool is for educational and personal use only. Scraping violates Instagram's terms of service. Use it responsibly.

---

## Troubleshooting

- **Python not found?**
  - Ensure Python is installed and added to your system's PATH.

Happy scraping! 😊