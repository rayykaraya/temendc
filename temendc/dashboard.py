import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from pathlib import Path

# ========== KONFIGURASI ========== 
sns.set(style='dark')
st.set_page_config(page_title="Analisis E-Commerce Public Dataset", layout="wide")

# ========== NAVIGASI ==========
st.sidebar.markdown("## Navigasi")
menu = st.sidebar.radio("Pilih Halaman:", ["Halaman Utama", "Analisis Data"])

# ========== PATH DATA ==========
dataset_paths = {
    "Category Reviews": Path("temendc/category_reviews.csv"),
    "Ordered Products": Path("temendc/ordered_products_by_customers.csv")
}

# Memuat dataset jika tersedia
datasets = {}
for name, path in dataset_paths.items():
    if path.is_file():
        datasets[name] = pd.read_csv(path)
    else:
        st.sidebar.warning(f"⚠️ File {name} tidak ditemukan!")

# ========== HALAMAN UTAMA ==========
if menu == "Halaman Utama":
    st.markdown("""
        <h1 style='text-align: center;'>Analisis E-Commerce Public Dataset</h1>
        <h3 style='text-align: center;'>Berikut adalah dataset yang digunakan pada Analisis Data kali ini</h3>
        """, unsafe_allow_html=True)
    
    selected_dataset = st.selectbox("Pilih Dataset:", list(dataset_paths.keys()))

    if selected_dataset in datasets:
        st.write(f"### Dataframe yang Dipilih: {selected_dataset}")
        st.dataframe(datasets[selected_dataset])
    else:
        st.error("❌ Dataset belum tersedia. Pastikan file sudah ada di repository atau unggah dataset.")

# ========== ANALISIS DATA ==========
elif menu == "Analisis Data":
    st.markdown("""<h1 style='text-align: center;'>📊 Analisis Data</h1>""", unsafe_allow_html=True)

    # Pastikan kedua dataset tersedia sebelum analisis
    if "Ordered Products" in datasets and "Category Reviews" in datasets:
        
        # ========== PERTANYAAN 1 ==========
        st.write("### PERTANYAAN 1: Produk dengan volume pembelian tertinggi")
        ordered_products_df = datasets["Ordered Products"]

        # Pastikan kolom yang dibutuhkan ada
        if "product_category_name" in ordered_products_df.columns and "order_id" in ordered_products_df.columns:
            ordered_products_df["product_category_name"] = ordered_products_df["product_category_name"].astype(str)

            top_10_products = (
                ordered_products_df
                .groupby("product_category_name", as_index=False)
                .agg({"order_id": "nunique"})
                .nlargest(10, "order_id")
            )

            fig, ax = plt.subplots(figsize=(10, 6))
            ax.barh(top_10_products["product_category_name"], top_10_products["order_id"], color="skyblue")
            ax.set_title("Top 10 Best Selling Products", fontsize=14)
            ax.set_xlabel('Total Sales')
            ax.set_ylabel('Product Category Name')
            ax.invert_yaxis()
            st.pyplot(fig)

            st.write("### Best Selling Product:")
            st.dataframe(top_10_products)
        else:
            st.error("❌ Kolom yang dibutuhkan tidak ditemukan dalam dataset!")

        # ========== PERTANYAAN 2 ==========
        st.write("### PERTANYAAN 2: Kategori produk dengan rating tertinggi dan terendah")
        category_reviews_df = datasets["Category Reviews"]

        if "review_score" in category_reviews_df.columns and "product_category_name_english" in category_reviews_df.columns:
            category_reviews_sorted = category_reviews_df.sort_values(by="review_score", ascending=False)

            # Salin data sebelum menambahkan kolom baru
            top_10_products_by_review = category_reviews_sorted.head(10).copy()
            top_10_lowest_rating_products = category_reviews_sorted.tail(10).copy()

            top_10_products_by_review["Kategori"] = "Top 10"
            top_10_lowest_rating_products["Kategori"] = "Lowest 10"
            combined_data = pd.concat([top_10_products_by_review, top_10_lowest_rating_products])

            fig, ax = plt.subplots(figsize=(18, 6))
            sns.scatterplot(
                x=combined_data["product_category_name_english"],
                y=combined_data["review_score"],
                hue=combined_data["Kategori"],
                palette={"Top 10": "green", "Lowest 10": "red"},
                s=100,
                ax=ax
            )

            plt.xticks(rotation=45)
            plt.title("Scatter Plot: Produk dengan Review Tertinggi & Terendah", fontsize=14)
            plt.xlabel("Kategori Produk", fontsize=12)
            plt.ylabel("Skor Review", fontsize=12)
            plt.legend(title="Kategori", loc="upper right")
            st.pyplot(fig)

            st.write("### Top Rated Product:")
            st.dataframe(top_10_products_by_review)

            st.write("### Lowest Rated Product:")
            st.dataframe(top_10_lowest_rating_products)
        else:
            st.error("❌ Kolom yang dibutuhkan tidak ditemukan dalam dataset!")

    else:
        st.error("⚠️ Data belum dimuat. Pastikan file tersedia atau unggah file CSV.")
