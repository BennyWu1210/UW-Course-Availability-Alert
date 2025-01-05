# **🎓 Class Spot Checker Script**
A Python script that monitors class enrollment availability at the University of Waterloo and sends instant SMS notification via Twilio when a spot becomes available.

---

## 🚀 **Features**
- 📊 **Class Enrollment Monitoring:** Scrapes the course enrollment page regularly
- 📱 **SMS Notifications:** Get instant alerts via Twilio SMS when a spot is available.  
---

## 🛠️ **Setup & Installation**

### **1. Clone the Repository**
```bash
git clone https://github.com/yourusername/class-spot-checker.git
cd class-spot-checker
```

### **2. Install Dependencies**
Ensure you have Python 3 and pip installed:
```bash
pip install -r requirements.txt
```

### **3. Create a `config.json` File**
Create a `config.json` file in the root directory with the following format:

```json
{
    "twilio": {
        "account_sid": "your_account_sid",
        "auth_token": "your_auth_token",
        "twilio_phone_number": "+1234567890",
        "your_phone_number": "+0987654321"
    },
    "scraper": {
        "url": "https://classes.uwaterloo.ca/cgi-bin/cgiwrap/infocour/salook.pl?level=under&sess=1249&subject=CO&cournum=250",
        "enrollment_threshold": 150,
        "check_frequency_minutes": 10
    }
}
```

- Replace `your_account_sid` and `your_auth_token` with your Twilio credentials.  
- Adjust the `url` and `enrollment_threshold` based on your class requirements.  

### **4. Run the Script**
```bash
python3 app.py
```

---

Alternatively, you can automate the script on a cron job!
