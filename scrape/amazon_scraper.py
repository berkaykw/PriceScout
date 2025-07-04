from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import chromedriver_autoinstaller
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from time import sleep
import streamlit as st
import re
from selenium.common.exceptions import ElementClickInterceptedException

chromedriver_autoinstaller.install()

def get_amazon_products(search_word, selected_sort_amazon):
    driver = webdriver.Chrome()
    driver.set_window_size(1280, 900)
    driver.get("https://www.amazon.com.tr/")

    try:
        WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.ID, "sp-cc-accept"))
        ).click()
    except TimeoutException:
        st.write("Çerez butonu görünmedi, geçildi.")

    sleep(2)

    search_box = driver.find_element(By.ID, "twotabsearchtextbox")
    search_box.send_keys(search_word)
    search_box.send_keys(Keys.ENTER)

    sleep(3)

    def apply_sort(driver, sort_text):
        try:
        # Sıralama menüsü görünene kadar bekle
            sort_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.ID, "a-autoid-0-announce"))
            )
            try:
                sort_button.click()
            except ElementClickInterceptedException:
            # Eğer tıklanamazsa JavaScript ile zorla tıkla
                driver.execute_script("arguments[0].click();", sort_button)

        # Seçenekler görünene kadar bekle
            options = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, "a-dropdown-link"))
            )

        # Doğru sıralama seçeneğini bul ve tıkla
            for option in options:
                if sort_text.lower() in option.text.lower():
                    try:
                        option.click()
                    except ElementClickInterceptedException:
                        driver.execute_script("arguments[0].click();", option)
                    break

        except Exception as e:
            st.warning(f"Sıralama uygulanırken bir hata oluştu: {e}")
    
    apply_sort(driver, selected_sort_amazon)

    sleep(6)
    
    product_elements = driver.find_elements(By.CSS_SELECTOR, "div.s-main-slot div[data-component-type='s-search-result']")
    products_amazon = []

    for product_element in product_elements[:8]:  # ilk 8 ürünü alıyoruz
        try:
        # Ürün adı
            name = product_element.find_element(By.CSS_SELECTOR, "a.a-link-normal.s-line-clamp-4.s-link-style.a-text-normal > h2 > span").text
        except NoSuchElementException:
            name = "Ürün Adı Yok"

        try:
            price = product_element.find_element(By.CSS_SELECTOR, "span.a-price > span.a-offscreen").text
    # Örnek: "1.259,00 TL"
            if price.strip() == "":  # boşsa tekrar dene
                raise NoSuchElementException
        except NoSuchElementException:
            try:
                whole = product_element.find_element(By.CSS_SELECTOR, "span.a-price-whole").text
                fraction = product_element.find_element(By.CSS_SELECTOR, "span.a-price-fraction").text
                price = whole + "," + fraction + " TL"
            except NoSuchElementException:
                price = "Fiyat Yok"


        try:
            rating_text = product_element.find_element(By.CSS_SELECTOR, "span.a-icon-alt").text
            rating_match = re.search(r"(\d+[.,]?\d*)", rating_text)
            if rating_match:
                rating = rating_match.group(1).replace(',', '.')
            else:
                rating = "Puan Yok"
        except NoSuchElementException:
            rating = "Puan Yok"

        try:
            comment_count = product_element.find_element(By.CSS_SELECTOR, "span.a-size-base").text
        except NoSuchElementException:
            comment_count = "Yorum Yok"

        try:
        # Ürün linki (a etiketi içindeki href)
            link = product_element.find_element(By.CSS_SELECTOR, "a.a-link-normal.s-line-clamp-4.s-link-style.a-text-normal").get_attribute("href")
        except NoSuchElementException:
            link = "Link Yok"

        try:
        # Resim URL'si
            img_url = product_element.find_element(By.CSS_SELECTOR, "img.s-image").get_attribute("src")
        except NoSuchElementException:
            img_url = "Resim Yok"

        products_amazon.append({
            "name": name,
            "price": price,
            "rating": rating,
            "comment": comment_count,
            "link": link,
            "img": img_url
        })



    driver.quit()
    return products_amazon

