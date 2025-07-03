import streamlit as st
from scrape.trendyol_scraper import get_trendyol_products
from scrape.hepsiburada_scraper import get_hepsiburada_products

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

selected_sort = st.selectbox("Trendyol için sıralama seçeneğini seçin:", sort_options, key="sort_trendyol")

st.markdown(
    """
    <p style='text-align:center; font-size:18px;'>
    Aşağıdaki butona basarak Trendyol ve Hepsiburada ürünlerini karşılaştırabilirsiniz.
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
if "hepsiburada_products" not in st.session_state:
    st.session_state.hepsiburada_products = []

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
    if st.button("Hepsiburada Ürünlerini Getir", key="get_hepsiburada"):
        if not search_word.strip():
            st.warning("Önce arama kelimesi girin.")
        else:
            with st.spinner("Hepsiburada verisi çekiliyor..."):
                st.session_state.hepsiburada_products = get_hepsiburada_products(search_word)

    if st.button("Hepsiburada Ürünlerini Temizle", key="clear_hepsiburada"):
        st.session_state.hepsiburada_products = []

st.markdown("---")

# Ürünleri listeleme fonksiyonu (tek ürün için)
def render_product_card(p, site_name):
    if site_name == "Trendyol":
        name, price, rating, comment, img_url, product_link = p
    else:  # Hepsiburada
        name = p.get("name", "Ürün adı yok")
        price = p.get("price", "Fiyat yok")
        rating = "-"
        comment = "-"
        img_url = p.get("img", "")
        product_link = p.get("link", "")

    card_html = f"""
    <div style='padding:10px; border:1px solid #eee; border-radius:10px; margin-bottom:15px; display: flex; align-items: center;'>
        <a href="{product_link}" target="_blank" rel="noopener noreferrer" style="flex-shrink: 0;">
            <img src="{img_url}" style="width:180px; height:180px; object-fit: cover; border-radius:15px; margin-right:15px;">
        </a>
        <div style="line-height:1.3; word-spacing:0.1em;">
            <b style='font-size:14px; display:block; margin-bottom:8px;'>{name}</b>
            <span style='color: #04d6f7; font-size:18px; font-weight:bold; display:block; margin-bottom:6px;'>{price}</span>
            <span style='color: #ffa000; font-size:14px; display:block; margin-bottom:4px;'>Ortalama Puan: {rating}⭐</span>
            <span style='color: #6d6f6f; font-size:13px; display:block;'>Yorum Sayısı: {comment}</span>
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
    st.markdown("<h2 style='text-align:center; color:#ff6600;'>Hepsiburada Ürünleri</h2>", unsafe_allow_html=True)
    if st.session_state.hepsiburada_products:
        for product in st.session_state.hepsiburada_products[:max_show]:
            st.markdown(render_product_card(product, "Hepsiburada"), unsafe_allow_html=True)