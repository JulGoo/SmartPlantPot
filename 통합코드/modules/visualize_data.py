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
    client = InfluxDBClient(host='localhost', port=8086, username='root', password='root', database='spp')
    
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
        "humidity": f"SELECT humidity As value, time FROM Humidity {time_filter} ORDER BY time",
        "soil_moisture": f"SELECT soil_moisture AS value, time FROM Soil_Moisture {time_filter} ORDER BY time"
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
    fig, ax = plt.subplots(4, 1, figsize=(10, 16), sharex=True)

    # 조도
    if "lux" in dataframes and not dataframes["lux"].empty:
        ax[0].plot(pd.to_datetime(dataframes["lux"]["time"]), dataframes["lux"]["value"], label="Lux", color="orange")
        ax[0].set_title("Light Exposure")
        ax[0].set_ylabel("Lux")
        ax[0].legend()

    # 온도
    if "temperature" in dataframes and not dataframes["temperature"].empty:
        ax[1].plot(pd.to_datetime(dataframes["temperature"]["time"]), dataframes["temperature"]["value"], label="Temperature", color="red")
        ax[1].set_title("Temperature")
        ax[1].set_ylabel("°C")
        ax[1].legend()

    # 습도
    if "humidity" in dataframes and not dataframes["humidity"].empty:
        ax[2].plot(pd.to_datetime(dataframes["humidity"]["time"]), dataframes["humidity"]["value"], label="Humidity", color="blue")
        ax[2].set_title("Humidity")
        ax[2].set_ylabel("%")
        ax[2].legend()

    # 토양 습도
    if "soil_moisture" in dataframes and not dataframes["soil_moisture"].empty:
        ax[3].plot(pd.to_datetime(dataframes["soil_moisture"]["time"]), dataframes["soil_moisture"]["value"], label="Soil Moisture", color="green")
        ax[3].set_title("Soil Moisture")
        ax[3].set_ylabel("Moisture Level")
        ax[3].legend()

    # 공통 설정
    ax[3].set_xlabel("Time")
    plt.tight_layout()

    # 테스트용 이미지 저장 코드 추가
    test_image_path = "test_image"
    if not os.path.exists(test_image_path):
        os.makedirs(test_image_path)
    test_file_path = os.path.join(test_image_path, f"visualization_{period}.png")
    plt.savefig(test_file_path)
    print(f"[TEST] Image saved at {test_file_path}")

    # 원래 코드: 메모리로 저장
    buffer = io.BytesIO()
    plt.savefig(buffer, format="png")
    buffer.seek(0)
    plt.close(fig)

    return buffer

def main():
    """메인 함수"""
    print("Select the period for visualization:")  # 사용자 입력
    print("1. Last 7 days (7d)")
    print("2. Last 30 days (30d)")
    print("3. Last 1 year (1y)")
    print("4. All data (all)")
    choice = input("Enter your choice (1/2/3/4): ")  # 테스트용 입력 받기 


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



