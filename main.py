import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import requests
from bs4 import BeautifulSoup
import time
import json
import os


url = 'webiste'
old_kots_file = 'old_studio.json'


def get_kots():
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    kots = []
    # Adapt based on website
    for kot in soup.find_all('div', class_='class'):
        title = kot.find('h2').text if kot.find('h2') else 'No Title'
        link = kot.find('a')['href'] if kot.find('a') else 'No Link'
        if not link.startswith('website'):
            link = 'website' + link
        hours = kot.find('li', class_='class').text.strip() if kot.find('li',class_='class') else 'No Price'
        price = kot.find('span', class_='class').text if kot.find('span', class_='class') else 'No Time'
        kots.append({'title': title, 'link': link, 'price': price, 'hours': hours})
    return kots



def send_email(new_kots):
    email = 'email'
    password = 'password'
    recipient = 'email'

    msg = MIMEMultipart()
    msg['From'] = email
    msg['To'] = recipient
    msg['Subject'] = 'New Studio'

    body = 'New studio:\n\n'
    for kot in new_kots:
        body += f"{kot['title']}\n{kot['link']}\n{kot['price']}\n{kot['hours']}\n\n"

    msg.attach(MIMEText(body, 'plain'))

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(email, password)
    text = msg.as_string()
    server.sendmail(email, recipient, text)
    server.quit()

def load_old_kots():
    if os.path.exists(old_kots_file):
        with open(old_kots_file, 'r') as file:
            return json.load(file)
    return []


def save_old_kots(old_kots):
    with open(old_kots_file, 'w') as file:
        json.dump(old_kots, file)

def main():
    old_kots = []

    while True:
        new_kots = get_kots()

        new_kots_diff = [kot for kot in new_kots if kot['link'] not in [old_kot['link'] for old_kot in old_kots]]
        if new_kots_diff:
            send_email(new_kots_diff)
            old_kots = new_kots
            save_old_kots(old_kots)

        time.sleep(900)  # Wait 15 min before checking again


if __name__ == '__main__':
    old_kots = load_old_kots()
    new_kots = get_kots()

    new_kots_diff = [kot for kot in new_kots if kot['link'] not in [old_kot['link'] for old_kot in old_kots]]
    if new_kots_diff:
        send_email(new_kots_diff)
        save_old_kots(new_kots)

    main()