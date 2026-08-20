# Superstore Sales & Profit Analysis

Analisis performa penjualan dan profitabilitas retail Superstore periode 2014-2017 untuk mengidentifikasi kategori produk, wilayah, segmen pelanggan, serta efektivitas kebijakan diskon terhadap margin profit perusahaan.

---

## 📌 Key Business Questions Answered

1. **Sub-kategori produk mana yang paling untung vs paling rugi?**
   - *Copiers*, *Phones*, dan *Accessories* menyumbang profit tertinggi.
   - *Tables* (-$17.725), *Bookcases*, dan *Supplies* mengalami kerugian signifikan meskipun volume sales tinggi.
2. **Apakah diskon berpengaruh terhadap profit?**
   - Ya, terdapat korelasi negatif (-0.22). Diskon di atas **20%** secara konsisten mengikis margin dan menyebabkan transaksi merugi.
3. **Bagaimana tren penjualan dari waktu ke waktu (bulanan)?**
   - Terlihat pola musiman (*seasonality*) dengan lonjakan sales & profit yang sangat tinggi menjelang akhir tahun (Kuartal 4: November & Desember).
4. **Wilayah (region) mana yang performanya paling baik?**
   - **West** dan **East** merupakan kontributor profit terbesar, sedangkan **Central** memiliki profit margin paling rendah akibat diskon agresif.
5. **Siapa 10 customer dengan kontribusi profit tertinggi?**
   - Pelanggan seperti *Tamara Chand*, *Raymond Buch*, dan *Sanjit Chand* memberikan akumulasi profit terbesar (> $3.800 - $8.900 per customer).

---

## 🛠️ Project Architecture & Tech Stack

- **Data Processing & EDA:** Python (`pandas`, `matplotlib`, `seaborn`)
- **SQL Database & Querying:** SQLite (`sqlite3`) & `sql/queries.sql`
- **Interactive Dashboard:** `Streamlit` & `Plotly Express`
- **Environment & Package Management:** `requirements.txt` with pinned versions
- **Deployment Ready:** Streamlit Community Cloud configuration (`.streamlit/config.toml`)

---

## 📁 Final Folder Structure

```text
superstore-project/
├── .streamlit/
│   └── config.toml          # Custom dark theme configuration for Streamlit Cloud
├── data/
│   └── Sample_-_Superstore.csv # Raw Kaggle Superstore dataset (9,994 records)
├── sql/
│   ├── superstore.db        # SQLite database (ISO YYYY-MM-DD date formatted)
│   ├── build_database.py    # Python ETL script to generate superstore.db
│   └── queries.sql          # Pure SQL queries answering the 5 key business questions
├── notebook/
│   └── superstore_analysis.ipynb # Jupyter notebook with EDA & sqlite3 integration
├── images/                  # Static charts exported from EDA notebook
│   ├── discount_vs_profit.png
│   ├── monthly_trend.png
│   ├── profit_per_region.png
│   └── profit_per_subcategory.png
├── app.py                   # Streamlit Interactive Dashboard app
├── requirements.txt         # Production-ready Python dependencies
├── .gitignore               # Standard Python gitignore (ensuring superstore.db is tracked)
└── README.md                # Project documentation
```

---

## 📊 Streamlit Interactive Dashboard

Dashboard interaktif dibangun menggunakan **Streamlit** dan **Plotly**, terhubung langsung ke SQLite database (`sql/superstore.db`).

### Fitur Dashboard:
- **KPI Cards Top Bar:** Total Sales, Total Profit, Profit Margin %, Total Orders, dan Rata-rata Diskon.
- **Dynamic Sidebar Filters:** Filter Rentang Tanggal, Region, Kategori Produk, dan Segmen Konsumen.
- **4 Visual Utama:**
  1. *Horizontal Bar Chart:* Profitability per Sub-Kategori (Highlight merah khusus sub-kategori rugi).
  2. *Dual Line Chart:* Tren perkembangan Sales & Profit Bulanan (2014-2017).
  3. *Bar Chart:* Perbandingan Profitabilitas antar Region.
  4. *Interactive Scatter Plot:* Dampak Diskon (%) terhadap Profit per Kategori dengan titik impas.

---

## 🚀 How to Run Locally

1. **Clone repository ini:**
   ```bash
   git clone https://github.com/USERNAME/superstore-project.git
   cd superstore-project
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **(Opsional) Re-build SQLite Database:**
   ```bash
   python sql/build_database.py
   ```

4. **Jalankan Dashboard Streamlit:**
   ```bash
   streamlit run app.py
   ```

5. **Akses Jupyter Notebook:**
   ```bash
   jupyter notebook notebook/superstore_analysis.ipynb
   ```

---

## ☁️ Deployment to Streamlit Community Cloud

Project ini sudah siap untuk di-deploy ke Streamlit Community Cloud:
1. Push repository ke GitHub.
2. Login ke [share.streamlit.io](https://share.streamlit.io/).
3. Pilih repository `superstore-project`, set main file path ke `app.py`.
4. Klik **Deploy**!
