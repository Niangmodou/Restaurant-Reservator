from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.common.action_chains import ActionChains
import smtplib, ssl
from email.mime.text import MIMEText
import os
from dotenv import load_dotenv
import logging

load_dotenv()

EMAIL = os.getenv("EMAIL")
PASSWORD = os.getenv("PASSWORD")


service = Service("./chromedriver")
options = webdriver.ChromeOptions()
DRIVER = webdriver.Chrome(service=service, options=options)


def find_reservation(month, day) -> str:
    month = "0" + str(month)
    if day < 10:
        day = "0" + str(day)
    link = "https://resy.com/cities/ny/carbone?date=2022-{}-{}&seats=2".format(
        month, day
    )
    print("MAKING CALL TO:", link)
    DRIVER.get(link)

    time.sleep(2)

    DRIVER.find_element(
        By.XPATH,
        "/html/body/div[1]/main/div/div[2]/div/article[1]/section[1]/resy-inline-booking/div/div/div[3]/div/resy-reservation-button-list",
    )

    return link


def send_email(month, day, link):
    month_map = {1: "January", 2: "February"}
    message = (
        "CARBONE HAS AN OPENING ON "
        + month_map[month]
        + " "
        + str(day)
        + ". Make a reservation at: "
        + link
    )

    # Creating the email
    sender = "niangmodou100@gmail.com"
    receivers = ["niangmodou100@gmail.com", "aam1040@nyu.edu"]

    msg = MIMEText(message, "html")
    msg["Subject"] = "CARBONE HAS AN OPENING MFFFFF"
    msg["From"] = sender
    msg["To"] = ",".join(receivers)

    # Sending the email using Simple Mail Transfer Protocool
    s = smtplib.SMTP_SSL(host="smtp.gmail.com", port=465)
    s.login(user=EMAIL, password=PASSWORD)
    s.sendmail(sender, receivers, msg.as_string())
    s.quit()
    print("SUCCESS!")


def main():
    for month in range(1, 3):
        for day in range(1, 31):
            try:
                link = find_reservation(month, day)

                send_email(month, day, link)

            except Exception as _:
                print("NOT FOUND:")


if __name__ == "__main__":
    main()
