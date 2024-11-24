import pandas as pd
from influxdb import InfluxDBClient
import matplotlib.pyplot as plt
import io
import os

def fetch_data_from_influxdb(period: str):
    """
    InfluxDB에서 사용자 지정 기간의 데이터를 불러옴
    :param period: '7d', '30d', '1y', or 'all'
    :return: 데이터프레임 딕셔너리
    """
    client = InfluxDBClient(host='', username='', password='', database='')

    # 기간별 쿼리 조건
    if period == "7d":
        time_filter = "WHERE time > now() - 7d"
    elif period == "30d":
        time_filter = "WHERE time > now() - 30d"
    elif period == "1y":
        time_filter = "WHERE time > now() - 365d"    # influxDB에서 1y를 인식하지 못함 -> 365d
    elif period == "all":
        time_filter = ""
    else:
        raise ValueError("Invalid period. Use '7d', '30d', '1y', or 'all'.")

    queries = {
        "lux": f"SELECT lux AS value, time FROM Light_Exposure {time_filter} ORDER BY time",
        "temperature": f"SELECT temperature As value, time FROM Temperature {time_filter} ORDER BY time",
        "humidity": f"SELECT humidity As value, time FROM Humidity {time_filter} ORDER BY time"
    }

    dataframes = {}
    for key, query in queries.items():
        try:
            result = client.query(query)
            points = list(result.get_points())
            dataframes[key] = pd.DataFrame(points)
        except Exception as e:
            print(f"Error fetching {key} data: {e}")

    client.close()
    return dataframes

def visualize_and_save_image(dataframes, period):
    """
    데이터 시각화 및 이미지로 저장
    :param dataframes: 데이터프레임 딕셔너리
    :param period: 사용자 지정 기간
    :return: 이미지 파일 버퍼
    """
    fig, ax = plt.subplots(3, 1, figsize=(10, 12), sharex=True)

    # 조도
    if "lux" in dataframes and not dataframes["lux"].empty:
        ax[0].plot(pd.to_datetime(dataframes["lux"]["time"]), dataframes["lux"]["드

    period_map = {
        "1": "7d",
        "2": "30d",
        "3": "1y",
        "4": "all"
    }

    period = period_map.get(choice)
    if not period:
        print("Invalid choice. Exiting.")
        return

    dataframes = fetch_data_from_influxdb(period)
    if not dataframes:
        print("No data fetched from InfluxDB.")
        return

    image = visualize_and_save_image(dataframes, period)
    print(f"Visualization completed for period: {period}.")
    return image

if __name__ == "__main__":
    image = main()
