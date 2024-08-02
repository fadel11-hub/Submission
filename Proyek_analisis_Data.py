import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
sns.set(style='dark')


def data_musim_penyewaan(df):
    # berapa total sepeda yang disewa pada saat musim yang berbeda dengan tahun yang berbeda
    season_year = df.groupby(by=['year', 'season']).agg({
        'total_count': 'sum'
    })

    season_year = season_year.reset_index()

    return season_year


def trend_banyak_hari(df):
    # bagaimana trend penyewaaan sepeda ketika hari biasa, tanggal merah dan hari kerja
    trend_hari = df.groupby(by=['weekday', 'workingday', 'holiday']).agg({
        'total_count': 'sum',
    }).reset_index()

    return trend_hari


def trend_banyak_tahun(df):
    trend_tahun = df.groupby(by='dteday').agg({
        'total_count': 'sum'
    }).reset_index()

    return trend_tahun


# Membaca data
days_data = pd.read_csv("days_data.csv")

datetime_columns = ['dteday']
days_data.sort_values(by='dteday', inplace=True)
days_data.reset_index(inplace=True)

for column in datetime_columns:
    days_data[column] = pd.to_datetime(days_data[column])


# Membuat Komponen Filter
min_date = days_data['dteday'].min()
max_date = days_data['dteday'].max()


with st.sidebar:
    # Menambahkan logo perusahaan
    st.image("https://github.com/dicodingacademy/assets/raw/main/logo.png")

    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu', min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

main_df = days_data[(days_data["dteday"] >= str(start_date)) &
                    (days_data["dteday"] <= str(end_date))]

season_bike_sharing = data_musim_penyewaan(main_df)
trend_many_days = trend_banyak_hari(main_df)
trend_many_year = trend_banyak_tahun(main_df)


st.title('Predicting Bike sharing demand')
with st.container():
    Total_seasons = season_bike_sharing.total_count.sum()
    st.metric('Total dalam satu musim ', value=Total_seasons)

    fig, ax = plt.subplots()
    # plt.figure(figsize=(10, 6))
    sns.barplot(x=days_data['season'], y=days_data['total_count'],
                hue=days_data['year'], errorbar=None)
    plt.xlabel('Season')
    plt.ylabel(None)
    plt.title('Total Count by Season')
    st.pyplot(fig)

st.subheader("Waktu kendaraan paling banyak")

# col1, col2, col3 = st.columns(3)

# with col1:
#     workingdays_receny = trend_many_days['workingday'].sum()
#     st.metric("workingdays Recency (days)", value=workingdays_receny)

# with col2:
#     holidays_receny = trend_many_days['holiday'].sum()
#     st.metric("holidays Recency (days)", value=holidays_receny)

# with col3:
#     weekday_receny = trend_many_days['weekday'].sum()
#     st.metric("weekday Recency (days)", value=weekday_receny)

fig, axes = plt.subplots(nrows=3, ncols=1, figsize=(35, 15))

# Plot for working days
sns.barplot(x=days_data['workingday'], y=days_data['total_count'],
            palette=['#FF0000', '#90CAF9'], ax=axes[0])
axes[0].set_xlabel('Working day', fontsize=20)
axes[0].set_ylabel(None)
axes[0].set_title('Jumlah pengguna sepeda pada hari kerja',
                  loc='center', fontsize=30)
axes[0].tick_params(axis='y', labelsize=35)
axes[0].tick_params(axis='x', labelsize=30)

# Plot for holidays
sns.barplot(x=days_data['holiday'], y=days_data['total_count'],
            palette=['#FF0000', '#90CAF9'], ax=axes[1])
axes[1].set_xlabel('Holiday', fontsize=20)
axes[1].set_ylabel(None)
axes[1].set_title(
    'Jumlah pengguna sepeda pada hari libur/ holiday', loc='center', fontsize=30)
axes[1].tick_params(axis='y', labelsize=35)
axes[1].tick_params(axis='x', labelsize=30)

# Plot for weekdays
sns.barplot(x=days_data['total_count'], y=days_data['weekday'],
            palette=['#FF0000', '#90CAF9'], ax=axes[2])
axes[2].set_xlabel('Weekdays', fontsize=20)
axes[2].set_ylabel(None)
axes[2].set_title(
    'Jumlah pengguna sepeda pada hari kerja/weekdays', loc='center', fontsize=30)
axes[2].tick_params(axis='y', labelsize=35)
axes[2].tick_params(axis='x', labelsize=30)
st.pyplot(fig)


st.subheader('Trend sepeda sepanjang 2011 - 2012')
# with st.container():
Total_year = trend_many_year.total_count.sum()
st.metric('Total dalam 2011 - 2012 ', value=Total_year)

# plt.figure(figsize=(10, 6))
# sns.lineplot(x= days_data['dteday'], y= days_data['total_count'], color='#90CAF9', linestyle='-', linewidth=2, marker='o', markersize=6)
# plt.xlabel('Year',fontsize=30)
# plt.ylabel('Total Count')
# plt.title('Total Count by date',fontsize=50)
# plt.grid(True, linestyle='--', alpha=0.8)
# st.pyplot(fig)

fig, ax = plt.subplots(figsize=(16, 8))
ax.plot(
    days_data["dteday"],
    days_data["total_count"],
    marker='o',
    linewidth=2,
    color="#90CAF9"
)
ax.set_xlabel("Date", fontsize=20)
ax.set_ylabel(None)
ax.set_title("Bikeshare Rides Over Time", fontsize=30)
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15)
st.pyplot(fig)

with st.container():
    fig, ax = plt.subplots(figsize=(16, 10))
    sns.lineplot(x=days_data['month'], y=days_data['total_count'], hue=days_data['year'],
                 color='#3498db', linestyle='-', linewidth=2, marker='o', markersize=6, ax=ax)
    ax.set_xlabel('month', fontsize=20)
    ax.set_ylabel(None)
    ax.set_title('Total Count by month', fontsize=30)
    ax.grid(True, linestyle='--', alpha=0.8)
    st.pyplot(fig)

st.caption('Copyright (c) Fadel 2024')
