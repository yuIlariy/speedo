# ⚡ Speedo Bot — Telegram VPS Speedtest 📡

This bot runs a full-speed diagnostic on your VPS using `speedtest-cli`, formats the results with enhanced metadata, masks IPs intelligently, and sends the output with a thumbnail via Telegram. Only the admin can trigger the test.

---

## 🛠️ Features

- `/start` — Welcome message with usage tips (admin only)
- `/speedtest` — Full diagnostic:
  - Download / Upload / Ping
  - VPS uptime
  - Data sent / received
  - Server location + sponsor
  - Client location + ISP
  - Masked IP (randomized)
  - Thumbnail preview
- `/trend` — Generates speed graph from last 30 results
- `/sysinfo` — Current VPS info:
  - 🧠 CPU model
  - ⏱️ Uptime
  - 💾 Disk usage
  - 📦 Memory usage
  - 📊 Load average
- 🖼️ Cleanly formatted results with HTML captions
- 🔒 Admin-only command access
- ⚙️ Built on Aiogram 3.7+

---

## 📦 Installation

### 1. Clone the Repo

```bash
git clone https://github.com/yuIlariy/speedo.git
cd speedo
```

### 2. Install Python and pip

```bash
sudo apt update
sudo apt install python3 python3-pip
```

### 3. Install Required Packages

```bash
pip3 install -r requirements.txt
```

---

## ⚙️ Configuration

Edit the `config.py` file:

```python
TOKEN = "your_telegram_bot_token"
ADMIN_ID = 123456789       # Your Telegram numeric user ID
THUMBNAIL_URL = "https://telegra.ph/file/e292b12890b8b4b9dcbd1.jpg"
```

---

## 🚀 Running the Bot

### Manual Start

```bash
python3 bot.py
```

### 🧠 Run in Background with Screen

- To run the bot in the background:
  ```bash
  screen -S speedo
  ```
  ```bash
  python3 bot.py
  ```
  - Detach: `Ctrl + A`, then `Ctrl + D`

- To stop:
  ```bash
  screen -r speedo
  ```
  - Use `Ctrl + C` to stop the bot
  ```bash
  screen -S speedo -X quit
  ```

---

## 🧪 Available Commands

| Command       | Description                          |
|---------------|--------------------------------------|
| `/start`      | Welcome & usage guide                |
| `/speedtest`  | Full VPS speedtest with thumbnail    |
| `/trend`      | Speed history graph (last 30 tests)  |
| `/sysinfo`    | VPS system info snapshot             |

---

## 📦 Requirements

```txt
aiogram>=3.7.0
speedtest-cli
matplotlib
```

---

## 📎 Developer Credits 🤩🚨

Original repo: [yuIlariy/speedo](https://github.com/yuIlariy/speedo)  
🍥 Telegram VPS bot extension by 🧠 Yuilariy x MS Copilot  
🌍 Speedtest with style. Fork it. Own it. Rule it 👑
