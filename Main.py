import traceback
from email.mime.multipart import MIMEMultipart

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import ChromeHandler
import time
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoSuchElementException
from time import sleep
import smtplib
from email.mime.text import MIMEText
from selenium.webdriver.common.by import By
import logging

toaddrs = 'paulholmes531@gmail.com'
username = 'paulholmes531'
password = 'lastvraceswejpfc'

def checkItems(links):
    message = ''
    itemNum = 1

    for link in links:
        logging.info('Item #%s \r\nLink: %s' % (itemNum, link))

        print(1, link)
        try:
            chrome.get(link)
            time.sleep(3)
            cartCount = None

            cart_elements = chrome.find_elements(By.XPATH, "//*[contains(text(), 'cart')]")
            print(2, cart_elements)
            for cart_element in cart_elements:
                element_text = cart_element.text.lower()
                if 'in' in element_text:
                    text_tokens = element_text.split(' ')
                    index = 0
                    print(text_tokens)
                    for text_token in text_tokens:
                        print('index: ', index)
                        print('token: ', text_token)
                        if 'cart' in text_token:
                            print('Item detected: ', link)
                            cartCount = text_tokens[index-1]
                            print('cartCount ', cartCount)
                            continue
                        index += 1
            print(3, cartCount)
            title = chrome.find_element(By.CSS_SELECTOR, '#listing-page-cart > div.wt-mb-xs-2 > h1').text
            price = chrome.find_element(By.CSS_SELECTOR, '#listing-page-cart > div:nth-child(2) > div > div.wt-display-flex-xs.wt-align-items-center.wt-flex-wrap > p').text
            if 'Price' in price:
                priceLines = price.splitlines()
                price = priceLines[1]
            if cartCount is None:
                continue
            elif cartCount == '1':
                message += 'Item #%s (In %s cart)<br>' % (itemNum, cartCount)
            else:
                message += 'Item #%s (In %s carts)<br>' % (itemNum, cartCount)
            message += "%s - %s<br>%s<br><br>" % (title, price, link)

            print(message)
            itemNum += 1
        except NoSuchElementException:
            print('No tag on %s' % link)
            continue


    print(message)
    logging.info('Message:\r\n%s' % message)
    chrome.close()

    if message != '':
        logging.info('Constructing email')
        msg = MIMEMultipart()
        msg['Subject'] = 'ASimplerTimeFinds - %s Items in carts' % (itemNum-1)

        # Record the MIME types of text/html.
        msg.attach(MIMEText(message, 'html'))    # Assume we know that the image files are all in PNG format
        fromaddr = 'paulholmes531@gmail.com'
        # to = ["paulholmes531@gmail.com", "brian.trosper@verizon.net", "maddy.trosper@gmail.com", 'brian.h.trosper@gmail.com']
        to = ["paulholmes531@gmail.com"]
        msg['To'] = ",".join(to)
        logging.info('Preparing to send email')

        # Send the email via our own SMTP server.
        server = smtplib.SMTP('smtp.gmail.com:587')
        server.starttls()
        server.login(username, password)

        server.sendmail(fromaddr, to, msg.as_string().encode('utf-8'))
        logging.info('Email sent')

        server.quit()


    quit()
if __name__ == '__main__':
    logging.basicConfig(filename='D:/workspace/MaddyScript/Logs/Maddy_%s' % str(time.strftime("%m_%d_%Y_%H_%M_%S", time.localtime())), level=logging.INFO, format='%(asctime)s: %(levelname)s - %(message)s')

    for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler)
    logging.info('Starting chrome...')
    chrome = ChromeHandler.getChrome()
    logging.info('Started chrome successfully...')


    links = []
    items = []
    pageNum = 1
    while True:
        chrome.get('https://www.etsy.com/shop/ASimplerTimeFinds?ref=items-pagination&page=%s&sort_order=date_desc' % pageNum)
        logging.info('Going to A Simpler Time Finds...')

        time.sleep(3)
        if 'No items listed at this time' in chrome.page_source:
            logging.info('On last page...')
            testLinks = []
            # testLinks.append(links[1])
            # testLinks.append(links[2])
            testLinks.append(links[3])
            # testLinks.append(links[4])
            # testLinks.append(links[5])
            # quit()
            logging.info('Links: %s...' % links)
            # checkItems(links)
            checkItems(testLinks)
        logging.info('Gathering item links on page %s...' % pageNum)
        for item in chrome.find_elements(By.CLASS_NAME, 'listing-link'):
            title = item.text.split('\n')[0]
            link = item.get_attribute('href')
            if title not in items and title != '':
                items.append(title)
                links.append(link)
        pageNum += 1
