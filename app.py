import requests
from bs4 import BeautifulSoup
from twilio.rest import Client
from datetime import datetime
import pytz
import json
import time

# Load configuration from config.json
with open('config.json', 'r') as config_file:
    config = json.load(config_file)


# Twilio credentials
account_sid = config['twilio']['account_sid']
auth_token = config['twilio']['auth_token']
twilio_phone_number = config['twilio']['twilio_phone_number']
your_phone_number = config['twilio']['your_phone_number']

# Scraper settings
URL = config['scraper']['url']
ENROLLMENT_THRESHOLD = config['scraper']['enrollment_threshold']
CHECK_FREQUENCY = config['scraper']['check_frequency_minutes']


# Function to scrape the website
def check_class_spot():
    try:
        response = requests.get(URL)
        response.raise_for_status()  # Raise error for bad HTTP status codes
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find the table rows that contain the enrollment numbers
        element = soup.select('table table tr')[1]
        course = element.find_all("td")

        print("Class ID:", course[0].get_text(strip=True))
        print("Campus:", course[2].get_text(strip=True))
        print("Current spots:", course[7].get_text(strip=True))

        enrolment_total = int(course[7].get_text(strip=True))

        if enrolment_total < ENROLLMENT_THRESHOLD:
            return True
    except requests.RequestException as e:
        print(f"Error during HTTP request: {e}")
    except (IndexError, ValueError) as e:
        print(f"Error parsing HTML or extracting enrollment data: {e}")

    return False


# Function to send an SMS
def send_sms(message="A spot has opened up for CO 331!"):
    try:
        client = Client(account_sid, auth_token)

        message = client.messages.create(
            body=message,
            from_=twilio_phone_number,
            to=your_phone_number
        )

        print(f"SMS sent: {message.sid}")
    except Exception as e:
        print(f"Failed to send SMS: {e}")


# Main function
def main(counter):
    eastern = pytz.timezone('US/Eastern')
    current_time = datetime.now(eastern)

    print("===== Current Time: " + str(current_time) + " =====")
    if check_class_spot():
        send_sms()
        print("Spot available! SMS sent.")
    else:
        if counter == 0:
            send_sms("No spots available yet. Scraper is set up.")
        print("No spot available yet.")


# Run the scraper periodically
if __name__ == "__main__":
    counter = 0
    while True:
        main(counter)
        print(f"Waiting for {CHECK_FREQUENCY} minutes before the next check...\n", flush=True)
        time.sleep(CHECK_FREQUENCY * 60)
        counter += 1
