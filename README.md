# ⚡ Speedo Bot — Telegram VPS Speedtest 📡

Not just a bot — a sysadmin assistant. A one-bot NOC panel for your VPS.  
Speedo performs full diagnostics, plots performance trends, monitors health, and exports logs — all from Telegram.  
Built on `aiogram` and optimized for deployment clarity, emoji-rich feedback, and admin-only control 👑🤩

---

## 🛠️ Features

- `/start` — Welcome message with usage tips (admin only)
- `/speedtest` — Full diagnostic utilizing the **official Ookla CLI** for high precision:
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
- `/pwatch` — Top 5 Resources-Heavy processes (with a refresh button 🔥)
- `/anomalywatch` — 👻 Auto watches your system with set threshold percentage & sends alerts ☄️
- `/anomalyreport` — ☄️ Manually pull anomaly report logs
- `/anomalystatus` — 👻 Anomalywatch status
- `/resetanomaly` — ☄️ Reset Anomaly 
- `/ping` — ICMP ping test to 8.8.8.8, 1.1.1.1 ... if target address not specified (packet loss, latency stats)
- `/exportlog` — Sends the full `speedlog.json` file as a document
- `/sysinfo` — Current VPS system info:
  - 🧠 CPU model
  - ⏱️ Uptime
  - 💾 Disk usage
  - 📦 Memory usage
  - 📊 Load average
  
- `/bootcheck` — VPS boot time & uptime snapshot (admin only)

- `/loadrings` — VPS rings 💍

- `/syschart` — Graphical system telemetry panel:
  - RAM & Disk usage bars
  - CPU load + temperature
  - Load average trend
  - Network I/O stats
  - Last speedtest overlay
  - Random caption flair 🤩

- Auto Speedtest loop:
  - Runs silently every hour
  - Appends results to `speedlog.json`
  - Sends HTML summary to admin with timestamp & uptime
    
- 🖼️ Cleanly formatted results using HTML + emoji
- 🔒 Admin-only command access
- ⚙️ Built on Aiogram 3.7+

---

## 📦 Installation

> *There mayhap a 15sec cool down after deploy to enable auto monitor without error (bot will boot after 15sec)(maybe cos 🦔 is 👑)*

### 1. Clone the Repo

```bash
git clone https://github.com/yuIlariy/speedo.git
```

```bash
cd speedo
```

### 2. Install Official Ookla Speedtest (Required)

To prevent network bottlenecks and ensure accurate readings, this bot uses the official Ookla binary via asynchronous execution. Install it easily using snap:
```bash
sudo snap install speedtest

```
*(Note: If your distribution doesn't have Snap installed out of the box, run sudo apt update && sudo apt install snapd first).*

### 3. Install Python and pip
```bash
sudo apt update
sudo apt install python3 python3-venv python3-pip

```
### 4. Create Virtual Environment (recommended)
```bash
python3 -m venv speedo
source speedo/bin/activate

```
### 5. Install Required Packages
```bash
pip3 install -r requirements.txt

```
## ⚙️ Configuration
Edit the config.py file:
```python
TOKEN = "your_telegram_bot_token"
ADMIN_ID = 123456789       # Your Telegram numeric user ID
THUMBNAIL_URL = "[https://telegra.ph/file/e292b12890b8b4b9dcbd1.jpg](https://telegra.ph/file/e292b12890b8b4b9dcbd1.jpg)"

```
## 🚀 Running the Bot
### Manual Start
```bash
python3 bot.py

```
### 🦔 Run in Background with Screen
```bash
screen -S speedo

```
```bash
python3 bot.py

```
Detach: Ctrl + A, then Ctrl + D
Resume:
```bash
screen -r speedo

```
Stop: Ctrl + C, then
```bash
screen -S speedo -X quit

```

## 🧪 Available Commands
| Command | Description |
|---|---|
| /start | Welcome & usage guide |
| /speedtest | Full VPS speedtest with thumbnail |
| /trend | Speed history graph (last 30 tests) |
| /monthlytrend | Plot only the tests from the current month |
| /lastspeed | Latest speedtest summary |
| /healthscore | VPS performance rating with emoji verdict |
| /ping | Ping a target address (or defaults) to check network health |
| /exportlog | Download speedlog.json |
| /sysinfo | VPS system snapshot |
| /bootcheck | VPS boot time & uptime |
| /syschart | Graphical telemetry panel with caption overlay |
| /loadrings | Graphical rings panel with caption overlay(LOTR) |
| /anomalywatch | Auto watch your system against set threshold points & sends alerts 👻 |
| /anomalyreport | Manually pull anomaly report 👻 |
| /anomalystatus | Know your anomalywatch status 👻 |
| /resetanomaly | Reset anomalywatch  👻 |
| /netstatus | Current network status 👻 |
| /pwatch | Top 5 resource-heavy processes 👻 |


## 📦 Requirements
```txt
aiogram>=3.7.0
matplotlib
psutil

```
## 📎 Developer Credits 🤩🚨
Original repo: [YuIlariy/speedo](https://github.com/yuIlariy/speedo)
🍥 Telegram VPS bot extension by 🧠 Yuilariy x MS Copilot
🌍 Speedtest with style. Fork it. Use it. Credit it. Rule it 👑
```
