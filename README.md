## 💻 Requirements

- Python 3.11 or higher
- Stable internet connection
- Valid [Firstmail](https://firstmail.ltd/en-US) email accounts
- Working proxies (HTTP)
- Captcha service subscription [capsolver](https://www.capsolver.com/)

## 🛠️ Installation

1. **Clone the Repository**
   ```bash
   git clone https://github.com/Tih000/GradientV4
   ```

2. **Set Up Virtual Environment**
   ```bash
   python -m venv venv
   source venv/Scripts/activate  # Windows
   source venv/bin/activate      # Unix/MacOS
   ```

3. **Install Dependencies**
   ```bash
   pip install -r req.txt
   ```

## ⚙️ Configuration

### 📁 config.py

```
HEADLESS = True
shuffle = False                     # Shuffle the mail or go in order (True or False)

delay_min = 30                      # Delay between accounts for the farming and regestration modes
delay_max = 50                      # (for correct operation, we do not recommend making a small delay)

DELAY_BETWEEN_GETTING_STATS = 500   # The average value (+-100) when checking statistics in farming mode
DINAMIC_PROXY = True                # Is your proxy dinamic? (True or False)

API_KEY_CAPSOLVER = ''              # API_KEY Capsolver
TELEGRAM = False                    # Use Telegram ? (True or False)
TELEGRAM_STATS_DELAY = 3600         # The delay between the output of statistics in Telegrams
BOT_TOKEN = ''                      # Token Telegram Bots (You can create the your Telegram bot on @BotFather)
CHAT_ID = ''                        # Your chatid (@getmyid_bot)
```

### 📁 Input Files Structure

#### emails.txt
```
email:password
email:password
```

#### proxies.txt
```
username:password:host:port
username:password:host:port
```

#### ref_codes.txt
```
8SVWZ4
8SVWZ4
8SVWZ4
```

## 🚀 Usage

1. Configure all necessary files as described above
2. Soft has 5 modes:
   - Registration accounts
   ```bash
    python main.py registratin
   ```
   - Farming points
   ```bash
    python main.py farming
   ```
   - Update stats
   ```bash
    python main.py update_stats
   ```
   - Get stats about points on accounts
   ```bash
    python main.py all_points
   ```
   - Get stats about active node on acounts
   ```bash
    python main.py active_node
   ```
   - Check status connection your proxy
   ```bash
    python main.py proxy
   ``` 

## 🧩 Navigation
**The /logs directory can contain 4 files with various information and statistics** 

#### app.txt (All program's logs)
```
2024-11-24 18:04:26 | INFO | 0 | email | Farming | Waiting for getting the stats...
2024-11-24 18:04:37 | INFO | 0 | email | Farming | Logining...
2024-11-24 18:04:53 | INFO | 0 | email | Farming | Status node: Good; Points: 22.22 pt
```

#### registered_accounts.txt (Program's logs about succesfully registration accounts)
```
2024-12-01 18:17:46 | 0 | email | Already registered accounts
2024-12-01 18:18:25 | 1 | email | Already registered accounts
```

#### STATS.txt (Info about statistics accounts after the running mode <update_stats>)
```
№: 0, Email: email, Points: 0.765, Code: 8SVWZ4, Referred By: 8SVWZ4, Work Active: 0
№: 1, Email: email, Points: 1.785, Code: 8SVWZ4, Referred By: 8SVWZ4, Work Active: 0
```

#### status_nodes.txt (Program's logs with current status nodes on famring accounts)
```
2024-12-01 21:28:30 | 0 | email | Farming | Status node: Good; Points: 0.76 pt
2024-12-01 21:29:35 | 1 | email | Farming | Status node: Unsupported; Points: 0.25 pt
```

## 🔧 Troubleshooting

### Common Issues and Solutions

#### 📧 Email Registration Failed
- Change the proxy for the registration

#### 🧩 Captcha Problems
- Verify API key validity
- Check service balance
- Ensure selected service is operational

#### 🌐 Proxy Issues
- Validate proxy format
- Check proxy functionality
- Ensure proxy authentication is correct

## 📞 Support

Join our Telegram community for support:
- 📢 Channel: [Maykanlnvest](https://t.me/Maykanlnvest)
