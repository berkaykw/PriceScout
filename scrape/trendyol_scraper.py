import streamlit as st
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import chromedriver_autoinstaller
from time import sleep
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException

chromedriver_autoinstaller.install()

def get_products(search_word):
    driver = webdriver.Chrome()
    driver.set_window_size(1280, 900)
    driver.get("https://www.trendyol.com/")

    try:
        WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.ID, "onetrust-accept-btn-handler"))
        ).click()
    except TimeoutException:
        print("Çerez butonu görünmedi, geçildi.")
    
    
    
    search_box = driver.find_element(By.CSS_SELECTOR, "input[data-testid='suggestion']")
    search_box.send_keys(search_word)
    search_box.send_keys(Keys.ENTER)
    
    sleep(3)

# en çok satan seçeneği
    driver.find_element(By.CLASS_NAME,"select-w").click() 
    best_seller = driver.find_elements(By.CLASS_NAME,"search-dropdown-text") 
    
    for cursor in best_seller:
        if "En çok satan" in cursor.text:
            cursor.click()
            break

    sleep(5)
    
    products = []

    
    for i in range(1,10):

        #ürün adı
        name_xpath = f'//*[@id="search-app"]/div/div/div/div[2]/div[4]/div[1]/div/div[{i}]/a/div[2]/div[1]/div[1]/div/h3'
        try:
            product_name = driver.find_element(By.XPATH, name_xpath).text.strip().replace("\n", " ")
        except NoSuchElementException:
            print(f"{i}. ürün adı alınamadı.")
            product_name = "Ürün adı yok"


        #ürün puanı
        rating_xpath = f'//*[@id="search-app"]/div/div/div/div[2]/div[4]/div[1]/div/div[{i}]/a/div[2]/div[1]/div[3]/div/div/span[1]'
        try:
            product_rating = driver.find_element(By.XPATH, rating_xpath).text
        except NoSuchElementException:
            product_rating = "Puan yok"


        #ürün yorum sayısı
        comment_xpath = f'//*[@id="search-app"]/div/div/div/div[2]/div[4]/div[1]/div/div[{i}]/a/div[2]/div[1]/div[3]/div/div/span[2]/span'
        try:
            product_comment = driver.find_element(By.XPATH, comment_xpath).text
        except NoSuchElementException:
            product_comment = "Yorum yok"

        
        #ürün fotografı
        img_url_xpath = f'//*[@id="search-app"]/div/div/div/div[2]/div[4]/div[1]/div/div[{i}]/a/div[1]/div[1]/div[1]/img'
        try:
            product_img_url = driver.find_element(By.XPATH,img_url_xpath).get_attribute("src")
        except:
            print(f"{i}. ürün fotografı alınamadı.")

        
        #ürün linki
        link_xpath = f'//*[@id="search-app"]/div/div/div/div[2]/div[4]/div[1]/div/div[{i}]/a'
        try:
            product_link = driver.find_element(By.XPATH, link_xpath).get_attribute("href")
        except:
            print(f"{i}. ürün linki alınamadı.")

        # FİYAT
        try:
                product_price_discounted = driver.find_element(By.XPATH,f'//*[@id="search-app"]/div/div/div/div[2]/div[4]/div[1]/div/div[{i}]//div[@class="price-item lowest-price-discounted"]').text
        except:
                product_price_discounted = None

        try:
                product_price_original = driver.find_element(By.XPATH,f'//*[@id="search-app"]/div/div/div/div[2]/div[4]/div[1]/div/div[{i}]/a/div[2]/div[1]/div[4]/div[2]/div[1]/div/div').text
        except:
                product_price_original = None

        if product_price_discounted:
                price_to_use = product_price_discounted
        elif product_price_original:
                price_to_use = product_price_original

        products.append((
            product_name, 
            price_to_use, 
            product_rating, 
            product_comment, 
            product_img_url, 
            product_link
        ))

    
    driver.quit()
    return products


# -- Streamlit Arayüz --

st.set_page_config(page_title="Trend Radar", page_icon="🛒", layout="centered")

st.markdown("<h1 style='text-align:center; color:#311B92;'>🛒 Trendyol En Çok Satan Ürünleri Listeleme</h1>", unsafe_allow_html=True)
st.markdown("---")

search_word = st.text_input("Aramak istediğiniz ürünü yazınız:")

st.markdown(
    """
    <p style='text-align:center; font-size:18px;'>
    Aşağıdaki butona basarak ürünlerini Trendyol'dan çekebilirsiniz.
    </p>
    """,
    unsafe_allow_html=True,
)

button_style = """
    <style>
    div.stButton > button {
        background-color: #FFFFFF;
        color: black;
        height: 3em;
        width: 100%;
        border-radius: 10px;
        font-size: 20px !important;
        font-weight: 900 !important;
        transition: background-color 0.3s ease;
    }
    div.stButton > button:hover {
        background-color: #512DA8;
        color: white;
    }
    div.stButton > button > div {
        font-size: 20px !important;
        font-weight: bold !important;
    }
    </style>
"""

st.markdown(button_style, unsafe_allow_html=True)


if st.button("Ürünleri Getir"):
    with st.spinner('Veriler çekiliyor...'):
        products = get_products(search_word)

    for name, price, rating, comment, img_url, product_link in products:
        st.markdown(
            f"""
            <div style='padding:10px; border-bottom:1px solid #eee; display: flex; align-items: center;'>
                <a href="{product_link}" target="_blank">
                    <img src="{img_url}" style="width:100px; height:100px; object-fit:cover; margin-right:20px; border-radius:10px;">
                </a>
                <div>
                    <b style='font-size:17px;'>{name}</b><br>
                    <span style='color: #04d6f7; font-size:18px; font-weight:bold;'>{price}</span><br>
                    <span style='color: #ffa000; font-size:14px;'>Ortalama Puan: {rating}⭐</span><br>
                    <span style='color: #6d6f6f; font-size:13px;'>Yorum Sayısı: {comment}</span>
                </div>
            </div>
        """,
            unsafe_allow_html=True
        )

