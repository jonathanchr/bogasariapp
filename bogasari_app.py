import streamlit as st
import pandas as pd
import datetime
import openpyxl
from PIL import Image
from io import BytesIO
import plotly_express as px
import plotly.graph_objects as go
import requests

st.set_page_config(page_title="Bogasari App", layout="wide")
st.markdown('<style>div.block-container{padding-top:1rem;}</style>', unsafe_allow_html=True)

# Unduh gambar dari URL
image_url = 'https://storage.googleapis.com/bogasari-app.appspot.com/logo_bogasari.jpg'
response = requests.get(image_url)

# Periksa apakah unduhan berhasil
if response.status_code == 200:
    # Tampilkan gambar di Streamlit
    st.write('Succeed')
else:
    st.write('Failed to download image')


# IMAGE & TITLE
col1, _, col2 = st.columns([0.45, 0.4, 0.15])
with col1:
    html_title = """
        <style>
            .title-test {
                font-weight:bold;
                padding:5px;
                border-radius:6px;
                text-align:left;
            }
            .subtitle-test{
                font-weight:bold;
                padding:5px;
                border-radius:6px;
                text-align:left;
                margin-top: -10px;
            }
        </style>
        <h2 class="title-test">CP PREMIUM</h2>
        <h3 class="title-test">ANALISA PERFORMANCE OUTLET</h3>
    """
    st.markdown(html_title, unsafe_allow_html=True)
with col2:
    image = st.image('https://storage.googleapis.com/bogasari-app.appspot.com/logo_bogasari.jpg')

# DATETIME
col3, _ = st.columns([0.1, 0.45])
with col3:
    box_date = str(datetime.datetime.now().strftime("%d %B %Y"))
    st.write(f"Date:  \n {box_date}")

# READING DATA
df = pd.read_excel(
    io="https://storage.googleapis.com/bogasari-app.appspot.com/FullOutlet.xlsx",
    engine="openpyxl",
    sheet_name="Data1",
    usecols="A:G",
    nrows=4000)

df_ach = pd.read_excel(
    io="https://storage.googleapis.com/bogasari-app.appspot.com/FullOutlet.xlsx",  # file name
    engine="openpyxl",  # library
    sheet_name="Achievement",
    usecols="A:G",  # which columns you want to use
    nrows=4000,  # how many rows are included in your selection
)
df_grw = pd.read_excel(
    io="https://storage.googleapis.com/bogasari-app.appspot.com/FullOutlet.xlsx",  # file name
    engine="openpyxl",  # library
    sheet_name="Growth",
    usecols="A:G",  # which columns you want to use
    nrows=4000,  # how many rows are included in your selection
)
merged_df = pd.concat([pd.DataFrame(df), pd.DataFrame(df_ach), pd.DataFrame(df_grw)], ignore_index=True)
# st.dataframe(merged_df)


# MENU SIDEBAR
st.sidebar.header("Choose Here: ")
account = st.sidebar.multiselect(
    "Select Outlet:",
    options=merged_df["Account"].unique()
)
tahun = st.sidebar.multiselect(
    "Select Year:",
    options=df["Year"].unique()
)
bulan = st.sidebar.multiselect(
    "Select Month:",
    options=merged_df["Month"].unique(),
    default=merged_df["Month"].unique()
)
filters = st.sidebar.multiselect(
    "Select Filters:",
    options=merged_df["Filter"].unique(),
    default=merged_df["Filter"].unique()
)
itemss = st.sidebar.multiselect(
    "Select Items:",
    options=merged_df["Item"].unique(),
    default=merged_df["Item"].unique()
)
df_selection = merged_df.query(
    "Account == @account & Year == @tahun & Month == @bulan & Filter == @filters & Item == @itemss"
)

# GRAFIK 1 [BARCHART : ]
filter_2023 = df[df["Year"] == 2023].groupby(by=["Filter"]).sum()[["Qty(Box)"]].sort_values(by="Qty(Box)")

col4, col5 = st.columns([0.45, 0.45])
with col4:
    fig1 = px.bar(filter_2023,
                  x=filter_2023.index,
                  y="Qty(Box)",
                  color=filter_2023.index,
                  title="Total Pencapaian Sales Volume 2023",
                  template="gridon")
    fig1.update_layout(xaxis_title="Marketing Plan")
    st.plotly_chart(fig1, use_container_width=True)

view2, view3 = st.columns([0.45, 0.45])
with view2:
    expander = st.expander("Rincian Data")
    expander.write(filter_2023)

# GRAFIK 2 [BARCHART : ]
filter_monthOf2023 = df[df["Year"] == 2023].groupby(by=["Filter", "Month"]).sum()[["Qty(Box)"]].reset_index()
month_order = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

with col5:
    fig2 = px.bar(filter_monthOf2023,
                  x="Month",
                  y="Qty(Box)",
                  color="Filter",
                  title="MONTHLY TREND Total Pencapaian Sales Volume 2023",
                  template="gridon",
                  barmode="group",
                  category_orders={"Month": month_order})
    fig2.update_traces(text=filter_monthOf2023["Qty(Box)"].round(2), textposition='outside')
    st.plotly_chart(fig2, use_container_width=True)

with view3:
    expander = st.expander("Rincian Data")
    expander.write(filter_monthOf2023)
st.divider()

col6, col7 = st.columns([0.45, 0.45])
with col6:
    # ARCHIEVEMENT
    jumlah_stt_2023 = df[(df['Filter'] == 'STT') & (df['Year'] == 2023)]['Qty(Box)'].sum()
    jumlah_target_2023 = df[(df['Filter'] == 'Target') & (df['Year'] == 2023)]['Qty(Box)'].sum()
    archive = round(jumlah_stt_2023 / jumlah_target_2023, 3)
    st.subheader(":book: ACHIEVEMENT 2023")
    st.subheader(archive)
with col7:
    # GROWTH
    quantity_stt_2021 = df[(df['Filter'] == 'STT') & (df['Year'] == 2021)]['Qty(Box)'].values[0]
    quantity_stt_2022 = df[(df['Filter'] == 'STT') & (df['Year'] == 2022)]['Qty(Box)'].values[0]
    quantity_stt_2023 = df[(df['Filter'] == 'STT') & (df['Year'] == 2023)]['Qty(Box)'].values[0]
    growth_percentage2221 = ((quantity_stt_2022 - quantity_stt_2021) / quantity_stt_2021) * 100
    growth_percentage2322 = ((quantity_stt_2023 - quantity_stt_2022) / quantity_stt_2022) * 100
    st.subheader(f"Growth 2022/2021: {growth_percentage2221: .2f}%")
    st.subheader(f"Growth 2023/2022: {growth_percentage2322: .2f}%")
st.divider()

st.header(f'Analisa Performance Outlet {tahun}')
st.header(f'Outlet : {account}')

# GRAFIK 3 [BARCHART : ]
item_filterandyear = df_selection.groupby(['Year', 'Filter', 'Item'])["Qty(Box)"].sum().reset_index(name='Count')

col8, col9 = st.columns([0.45, 0.45])
with col8:
    fig3 = px.bar(
        item_filterandyear,
        x='Year',
        y='Count',
        color='Item',
        facet_col='Filter',
        labels={'Count': 'Quantity'},
        title='TREND Sales Volume Per Produk',
        barmode="group"
    )
    st.plotly_chart(fig3, use_container_width=True)

view4, view5 = st.columns([0.45, 0.45])
with view4:
    expander = st.expander("Rincian Data")
    expander.write(item_filterandyear)

# GRAFIK 4 [BARCHART : ]
outlet_peritem = df_selection.groupby(['Account', 'Item'])['Qty(Box)'].sum().reset_index()
with col9:
    fig4 = px.bar(outlet_peritem,
                  x='Account',
                  y='Qty(Box)',
                  color='Item',
                  title='Sales Volume Per Produk Per Outlet',
                  template='gridon',
                  barmode='group'
                  )
    fig4.update_layout(xaxis_title='Outlet')
    st.plotly_chart(fig4, use_container_width=True)
with view5:
    expander = st.expander("Rincian Data")
    expander.write(outlet_peritem)

# GRAFIK 5 [BARCHART : ]
filter_month = df_selection.groupby(by=["Filter", "Month"]).sum()[["Qty(Box)"]].reset_index()
month_order = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
item_order = ['TSB', 'TKB', 'TCK']
col10, col11 = st.columns([0.45, 0.45])
with col10:
    fig5 = px.bar(filter_month,
                  x="Month",
                  y="Qty(Box)",
                  color="Filter",
                  title='MONTHLY Sales Achievement',
                  template="gridon",
                  barmode="group",
                  category_orders={"Month": month_order})
    # fig2.update_traces(text=filter_monthOf2023["Qty(Box)"].round(2), textposition='outside')
    st.plotly_chart(fig5, use_container_width=True)

filter_perYear = df.groupby(by=["Year", "Filter"]).sum()[["Qty(Box)"]].reset_index()
view6, view7 = st.columns([0.45, 0.45])
with view6:
    expander = st.expander("Rincian Trend Penjualan Pertahun")
    expander.write(filter_perYear)

# GRAFIK 6 [BARCHART : ]
item_perMonth = df_selection.groupby(by=["Item", "Month"]).sum()[["Qty(Box)"]].reset_index()
month_order = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

with col11:
    fig6 = px.bar(item_perMonth,
                  x="Month",
                  y="Qty(Box)",
                  color="Item",
                  title='MONTHLY TREND Sales Volume Per Product',
                  labels={"Qty(Box)": "Quantity"},
                  category_orders={"Month": month_order},
                  template="gridon",
                  barmode="group")
    st.plotly_chart(fig6, use_container_width=True)

item_perYear = df.groupby(by=["Year", "Item"]).sum()[["Qty(Box)"]].reset_index()
with view7:
    expander = st.expander("Rincian Trend Penjualan Pertahun")
    expander.write(item_perYear)

# GRAFIK 7 [PIECHART : KOMPOSISI OUTLET PER TAHUN]
col12, col13 = st.columns((2))
outlet_order = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26]
with col12:
    fig9 = px.pie(
        df_selection,
        names='Account',
        values='Qty(Box)',
        labels={'Qty(Box)', 'Quantity'},
        title='Komposisi Outlet Per Tahun',
        category_orders={'Account': outlet_order})
    st.plotly_chart(fig9, use_container_width=True)

# GRAFIK 8 [PIECHART : KOMPOSISI ]
with col13:
    fig10 = px.pie(
        df_selection,
        names='Item',
        values='Qty(Box)',
        labels={'Qty(Box)', 'Quantity'},
        title='Komposisi Produk Per Tahun')
    st.plotly_chart(fig10, use_container_width=True)

# HIDE STREAMLIT STYLE
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)
