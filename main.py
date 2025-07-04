import streamlit as st
from scrape.trendyol_scraper import get_trendyol_products
from scrape.amazon_scraper import get_amazon_products
from PIL import Image
import streamlit as st

image_path = r"C:\Users\Ömer KARATAŞ\calisma\assets\images\logo.png"
image = Image.open(image_path)
col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    st.image(image, width=300)

st.set_page_config(page_title="Price Scout", layout="centered")
st.markdown("<h1 style='text-align:center; color:#0523f9;'>🛒 Price Scout - Ürünleri Hızlıca Karşılaştır ve Kararını Ver.</h1>", unsafe_allow_html=True)
st.markdown("---")

search_word = st.text_input("Aramak istediğiniz ürünü yazınız:", key="search_input")

sort_options = [
    "Önerilen",
    "En düşük fiyat",
    "En yüksek fiyat",
    "En çok satan",
    "En favoriler",
    "En yeniler",
    "En çok değerlendirilen"
]

amazon_sort_options = [
    "Öne Çıkanlar",             
    "Fiyat: Düşükten Yükseğe",    
    "Fiyat: Yüksekten Düşüğe",   
    "Çok Satanlar",                                     
    "En Son Gelenler",            
    "Ort. Müşteri Yorumu"  
]


selected_sort = st.selectbox("Trendyol için sıralama seçeneğini seçin:", sort_options, key="sort_trendyol")
selected_sort_amazon = st.selectbox("Amazon için sıralama seçeneğini seçin:", amazon_sort_options, key="sort_amazon")

st.markdown(
    """
    <p style='text-align:center; font-size:18px;'>
    Aşağıdaki butona basarak Trendyol ve Amazon ürünlerini karşılaştırabilirsiniz.
    </p>
    """,
    unsafe_allow_html=True,
)

button_style = """
    <style>
    div.stButton > button {
        background-color: #ffffff;
        color: black;
        height: 3em;
        width: 100%;
        border-radius: 10px;
        font-size: 20px !important;
        font-weight: 900 !important;
        transition: background-color 0.3s ease;
    }
    div.stButton > button:hover {
        background-color: #1e39fb;
        color: white;
    }
    div.stButton > button > div {
        font-size: 20px !important;
        font-weight: bold !important;
    }
    </style>
"""
st.markdown(button_style, unsafe_allow_html=True)

if "trendyol_products" not in st.session_state:
    st.session_state.trendyol_products = []
if "amazon_products" not in st.session_state:
    st.session_state.amazon_products = []

col1, col2 = st.columns([1,1])

with col1:
    if st.button("Trendyol Ürünlerini Getir", key="get_trendyol"):
        if not search_word.strip():
            st.warning("Önce arama kelimesi girin.")
        else:
            with st.spinner("Trendyol verisi çekiliyor..."):
                st.session_state.trendyol_products = get_trendyol_products(search_word, selected_sort)

    if st.button("Trendyol Ürünlerini Temizle", key="clear_trendyol"):
        st.session_state.trendyol_products = []

with col2:
    if st.button("Amazon Ürünlerini Getir", key="get_amazon"):
        if not search_word.strip():
            st.warning("Önce arama kelimesi girin.")
        else:
            with st.spinner("Amazon verisi çekiliyor..."):
                st.session_state.amazon_products = get_amazon_products(search_word, selected_sort_amazon)

    if st.button("Amazon Ürünlerini Temizle", key="clear_amazon"):
        st.session_state.amazon_products = []

st.markdown("---")

def render_product_card(p, site_name):
    if site_name == "Trendyol":
        name, price, rating, comment, img_url, product_link = p
    elif site_name == "Amazon":
        name = p.get("name", "Ürün adı yok")
        price = p.get("price", "Fiyat yok")
        rating = p.get("rating", "-")
        comment = p.get("comment", "-")
        product_link = p.get("link", "")
        img_url = p.get("img", "")
    else:
        name = p.get("name", "Ürün adı yok")
        price = p.get("price", "Fiyat yok")
        rating = "-"
        comment = "-"
        img_url = p.get("img", "")
        product_link = p.get("link", "")

    card_html = f"""
    <div style='
        padding:10px;
        border:1px solid #eee;
        border-radius:10px;
        margin-bottom:15px;
        display: flex;
        align-items: center;
        height: 300px;
        overflow: hidden;
        box-sizing: border-box;
    '>
        <a href="{product_link}" target="_blank" rel="noopener noreferrer" style="flex-shrink: 0;">
            <img src="{img_url}" style="width:180px; height:230px; object-fit: cover; border-radius:15px; margin-right:15px;">
        </a>
        <div style="line-height:1.4; word-spacing:0.1em; overflow: hidden;">
            <div style='
                font-size:14px;
                font-weight:bold;
                margin-bottom:8px;
                height: 5.25em;
                overflow: hidden;
                text-overflow: ellipsis;
                display: -webkit-box;
                -webkit-line-clamp: 3;
                -webkit-box-orient: vertical;
            '>{name}</div>
            <div style='color: #04d6f7; font-size:18px; font-weight:bold; margin-bottom:6px;'>Fiyat: {price}</div>
            <div style='color: #ffa000; font-size:14px; margin-bottom:4px;'>Ortalama Puan: {rating}⭐</div>
            <div style='color: #6d6f6f; font-size:13px;'>Yorum Sayısı: {comment}</div>
        </div>
    </div>
    """

    return card_html

# Ürünleri yan yana sütunlarda gösterme
max_show = 10  # ilk 10 ürünü göster

cols = st.columns(2)

with cols[0]:
    st.markdown("<h2 style='text-align:center; color:#f06523;'>Trendyol Ürünleri</h2>", unsafe_allow_html=True)
    if st.session_state.trendyol_products:
        for product in st.session_state.trendyol_products[:max_show]:
            st.markdown(render_product_card(product, "Trendyol"), unsafe_allow_html=True)


with cols[1]:
    st.markdown("<h2 style='text-align:center; color:#ff6600;'>Amazon Ürünleri</h2>", unsafe_allow_html=True)
    if st.session_state.amazon_products:
        for product in st.session_state.amazon_products[:max_show]:
            st.markdown(render_product_card(product, "Amazon"), unsafe_allow_html=True)


