from selenium import webdriver
from datetime import datetime
import psycopg2
import time


def setup():
    # Create database connection
    conn = psycopg2.connect(database="postgres", user="postgres",
                            password="Aa@123456", host="127.0.0.1", port="5432")

    # create selenium web driver
    opts = webdriver.ChromeOptions()
    opts.add_experimental_option("detach", True)
    driver = webdriver.Chrome(executable_path=r"./chromedriver")

    return conn, driver


def scrape_data():
    conn, driver = setup()

    driver.get(
        "https://coinmarketcap.com/currencies/bitcoin/")
    previous_price = 0

    while (1):
        time.sleep(3)
        # get currently displayed price
        price = driver.find_elements_by_xpath(
            "//div[@class='priceValue___11gHJ ']")
        price = price[0].text[1:].replace(',', '')

        # in case the website close the session
        if price == previous_price:
            driver.refresh()
            time.sleep(1)
            price = driver.find_elements_by_xpath(
                "//div[@class='priceValue___11gHJ ']")
            price = price[0].text[1:].replace(',', '')

        previous_price = price
        current_time = datetime.now()
        cur = conn.cursor()
        cur.execute(
            f"INSERT INTO BT_Price (Created_at,Price) VALUES ('{str(current_time)}', {price})")
        conn.commit()
        time.sleep(20)


if __name__ == "__main__":
    scrape_data()
