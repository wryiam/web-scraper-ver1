from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from tkinter import *
from tkinter import ttk
import time


def scrapeit():
    base_xpath = '//*[@id="default"]/div/div/div/div/section/div[2]/ol/li['
    inner_html_price_list = []
    inner_html_book = []

    for i in range(1, 10):
        current_xpath = base_xpath + str(i) + ']/article/div[2]/p[1]'
        current_name_xpath = base_xpath + str(i) + ']/article/h3/a'

        try:
            element = driver.find_element("xpath", current_xpath)
            element2 = driver.find_element("xpath", current_name_xpath)
            inner_html_price_list.append(element.get_attribute("innerHTML"))
            inner_html_book.append(element2.text)
        except:
            print(f"Element {current_xpath} not found")
            break

    return inner_html_book, inner_html_price_list


def display_gui(categories_data):
    window = Tk()
    window.geometry("600x500")
    window.title("Book Scraper Demo")

    notebook = ttk.Notebook(window)
    notebook.pack(expand=1, fill='both')

    for category_name, (booknames, bookprices) in categories_data.items():
        frame = Frame(notebook)
        notebook.add(frame, text=category_name)

        for idx, (price, book) in enumerate(zip(booknames, bookprices), start=1):
            price_label = Label(frame, text=f"Price {idx}: {price}", font=("Consolas", 12))
            price_label.pack()
            book_label = Label(frame, text=f"Book {idx}: {book}", font=("Consolas", 12))
            book_label.pack()

    window.mainloop()


options = Options()
options.add_experimental_option("detach", True)

# Initialize the WebDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
driver.get("https://books.toscrape.com")

first_xpath = '//*[@id="default"]/div/div/div/aside/div[2]/ul/li/ul/li['

categories_data = {}

for i in range(1, 11):
    try:

        driver.get("https://books.toscrape.com")
        time.sleep(0)

        thexpath = first_xpath + str(i) + ']/a'
        element = driver.find_element("xpath", thexpath)
        category_name = element.text
        print(f"Scraping category: {category_name}")
        element.click()
        time.sleep(0)

        booknames, bookprices = scrapeit()
        categories_data[category_name] = (booknames, bookprices)

    except Exception as e:
        print(f"An error occurred: {e}")
        break

driver.quit()

display_gui(categories_data)
