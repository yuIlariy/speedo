# ⚡ Speedo Bot — Telegram VPS Speedtest 📡

This bot runs a full-speed diagnostic on your VPS using `speedtest-cli`, formats the results with enhanced metadata, masks IPs intelligently, and sends the output with a thumbnail via Telegram. Only the admin can trigger the test.

---

## 🛠️ Features

- `/start` — Welcome and usage hint (admin only)
- `/speedtest` — Full-speed diagnostic with:
  - Download / Upload / Ping
  - Data sent / received
  - Server location + sponsor
  - Client location + ISP
  - Masked IP (randomized)
  - Thumbnail image
- 🔒 Admin-only access
- ⚙️ Aiogram 3.7+ compatible
- 🖼️ Sends result as a photo with formatted caption

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

```bash
sudo apt install screen
screen -S speedo
python3 bot.py
```

> ⏹️ To detach screen: `Ctrl + A`, then `D`  
> 🔙 To resume screen: `screen -r speedo`

---

## 🧪 Example Commands

- `/start` → Replies with usage hint  
- `/speedtest` → Sends thumbnail + full metrics

---

## 🧰 Built With

- [Aiogram 3.7+](https://docs.aiogram.dev/en/latest/)
- [speedtest-cli](https://github.com/sivel/speedtest-cli)
- Python 3.10+

---

## 🧹 Optional Cleanup

```bash
rm logs/bot.log
```

---

## 📎 DEVELOPER 🤩🚨

[github.com/yuIlariy/speedo](https://github.com/yuIlariy/speedo)
