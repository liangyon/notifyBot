import requests
from bs4 import BeautifulSoup
from plyer import notification
import time
from emailHandler import send_email
from dotenv import load_dotenv
import os


# Function to send notifications
def send_notification(title, message):
    notification.notify(
        title=title,
        message=message,
        timeout=10  # Notification will disappear after 10 seconds
    )


# Function to parse HTML and check for changes
def parse_html(url, last_content):
    try:
        # Send HTTP request and get the webpage content
        response = requests.get(url)

        if response.status_code == 200:
            print("Website is accessible.")
        else:
            print("Website is not accessible. Status code:", response.status_code)

        soup = BeautifulSoup(response.text, 'html.parser')
        load_dotenv()
        # Customize this part based on the structure of the webpage
        current_content = soup.find_all(class_="product-item__text")
        content_body = ""
        for link in current_content:
            content_body += link.text + " "
        print(content_body)
        # Check if content has changed since the last check
        if current_content != last_content:
            send_notification("Web Crawler Notification", "New content detected on the webpage!")
            subject = "There are new mats on sale!"
            body = content_body
            sender = os.getenv("SENDER")
            recipients = os.getenv("RECIPIENTS")
            password = os.getenv("PASSWORD")
            send_email(subject, body, sender, recipients, password)
        return current_content

    except Exception as e:
        print(f"Error: {e}")
        return last_content


# Main loop to run the script continuously
def main():
    url = "https://pvramid.com/collections/in-stock-artisan-field-cloths"  # or any example url
    last_content = ""

    while True:
        last_content = parse_html(url, last_content)
        time.sleep(3600)  # Check for changes every hour


if __name__ == "__main__":
    main()
