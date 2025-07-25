# ⚡ Speedo Bot — Telegram VPS Speedtest 📡

Not just a bot — a sysadmin assistant. A one-bot NOC panel for your VPS.  
Speedo performs full diagnostics, plots performance trends, monitors health, and exports logs — all from Telegram.  
Built on `aiogram` and optimized for deployment clarity, emoji-rich feedback, and admin-only control 👑🤩

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
- `/trend` — Speed graph using the last 30 tests
- `/monthlytrend` — Graph showing only results from the current month
- `/lastspeed` — Displays the latest speedtest snapshot in text format
- `/healthscore` — Emoji-based VPS performance rating (ping, bandwidth)
- `/pingtest` — ICMP ping test to 8.8.8.8 (packet loss, latency stats)
- `/exportlog` — Sends the full `speedlog.json` file as a document
- `/sysinfo` — Current VPS system info:
  - 🧠 CPU model
  - ⏱️ Uptime
  - 💾 Disk usage
  - 📦 Memory usage
  - 📊 Load average
- 🖼️ Cleanly formatted results using HTML + emoji
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

### 3. Create Virtual Environment (recommended)

```bash
python3 -m venv speedo
source speedo/bin/activate
```

### 4. Install Required Packages

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

```bash
screen -S speedo
```
```bash
python3 bot.py
```

Detach: `Ctrl + A`, then `Ctrl + D`  
Resume: 
```bash
screen -r speedo
```
Stop: `Ctrl + C`, then 
```bash
screen -S speedo -X quit
```

---

## 🧪 Available Commands

| Command           | Description                                      |
|-------------------|--------------------------------------------------|
| `/start`          | Welcome & usage guide                           |
| `/speedtest`      | Full VPS speedtest with thumbnail                |
| `/trend`          | Speed history graph (last 30 tests)              |
| `/monthlytrend`   | Plot only the tests from the current month       |
| `/lastspeed`      | Latest speedtest summary                        |
| `/healthscore`    | VPS performance rating with emoji verdict        |
| `/pingtest`       | Ping 8.8.8.8 to check network health             |
| `/exportlog`      | Download `speedlog.json`                         |
| `/sysinfo`        | VPS system snapshot                             |

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
🌍 Speedtest with style. Fork it. Use it. Credit it. Rule it 👑
