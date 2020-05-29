import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import rc
rc('font', family='AppleGothic') # 맥 컴퓨터 사용 시

air_2017_df = pd.read_csv('./AIR_HOUR_2017.csv', parse_dates=["측정일시"], dtype={"측정소 코드": str})
air_2018_df = pd.read_csv('./AIR_HOUR_2018.csv', parse_dates=["측정일시"], dtype={"측정소 코드": str})
air_station_df = pd.read_csv('./AIR_STATION.csv', dtype={"측정소 코드": str})

air_2017_len = air_2017_df.shape[0]
air_2018_len = air_2018_df.shape[0]

air_total_df = air_2017_df.append(air_2018_df, ignore_index=True)
air_total_len = air_total_df.shape[0]
assert air_total_len == air2017_len + air2018_len

air_filtered_df = air_filtered_df[(air_total_df["측정항목 코드"] == 8) | (air_total_df["측정항목 코드"] == 9)]
air_filtered_df.reset_index(drop=True, inplace=True)

air_total["측정일시"] = pd.to_datetime(air_total["측정일시"].dt.strftime("%Y-%m-%d"))

finedust_df = air_filtered_df[air_filtered_df["측정항목 코드"] == 8][["측정일시", "평균값", "측정소 코드"]]
ufinedust_df = air_filtered_df[air_filtered_df["측정항목 코드"] == 9][["측정일시", "평균값", "측정소 코드"]]

plt.subplot(2, 1, 1)
for i in range(13):
    target_measurement = finedust_df[finedust_df["측정소 코드"] == str(101+i)]
    target_station = air_station_df[air_station_df["측정소 코드"] == str(101+i)]

    x = target_measurement["측정일시"].drop_duplicates()
    y = target_measurement.groupby(["측정소 코드", "측정일시"]).max()
    plt.plot(x, y, label=target_station["측정소 주소"].values[0])

plt.legend(loc='upper left')
plt.ylim([0.0, 600])

plt.subplot(2, 1, 2)
for i in range(12):
    target_measurement = finedust_df[finedust_df["측정소 코드"] == str(114+i)]
    target_station = air_station_df[air_station_df["측정소 코드"] == str(114+i)]

    x = target_measurement["측정일시"].drop_duplicates()
    y = target_measurement.groupby(["측정소 코드", "측정일시"]).max()
    plt.plot(x, y, label=target_station["측정소 주소"].values[0])

plt.legend(loc='upper left')
plt.ylim([0.0, 600])
plt.show()


x = finedust_df["측정일시"].drop_duplicates()
y = finedust_df.groupby(["측정일시"]).mean()
plt.plot(x, y, label="미세먼지")

x = ufinedust_df["측정일시"].drop_duplicates()
y = ufinedust_df.groupby(["측정일시"]).mean()
plt.plot(x, y, label="미세먼지")

plt.legend(loc='upper left')
plt.ylim([0.0, 500])
plt.show()


fig, ax = plt.subplots()
finedust_df = finedust_df[(finedust["평균값"] > 0) & (finedust["평균값"] < 400)]
finedust_df.boxplot(by="측정소 코드", ax=ax)
plt.show()