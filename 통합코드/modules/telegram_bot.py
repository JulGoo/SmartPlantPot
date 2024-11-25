# 텔레그램 봇
import os
import glob
import asyncio
import telegram

import os
from dotenv import load_dotenv
from visualize_data import fetch_data_from_influxdb, visualize_and_save_image
from resnet50_model import model_predict
from timelapse import create_video_from_photos


# 텔레그램 봇 토큰값과 채팅 아이디 가져오기
def load_telegram():
    try:
        load_dotenv("../telegram.env")
        token = str(os.getenv("token"))
        chat_id = str(os.getenv("chatID"))

        # 토큰과 채팅 ID가 제대로 로드되었는지 확인
        if not token or not chat_id:
            raise ValueError("telegram_bot.py: 토큰 또는 채팅 ID가 누락되었습니다.")

        return token, chat_id
    except Exception as e:
        print(f"telegram_bot.py: 텔레그램 연동 에러: {e}")
        return None, None


# 일반 메세지 전송
async def send_chat(msg, chat_id):
    bot = telegram.Bot(token=load_telegram()[0])
    await bot.sendMessage(chat_id, text=msg, parse_mode="Markdown")


# 식물 상태 분석 - 사진 전송
async def send_image(chat_id):
    bot = telegram.Bot(token=load_telegram()[0])

    try:
        # 최근 식물 이미지 전송
        image_dir = "../plant_images"
        image_files = glob.glob(os.path.join(image_dir, "*.jpg"))

        if not image_files:
            print(f"telegram_bot.py: 이미지가 존재하지 않습니다.{image_dir}")
            return False
        
        latest_file = max(image_files, key=os.path.getctime)

        await bot.send_photo(chat_id, photo=open(latest_file, 'rb'), captuion="🌱 식물의 최근 모습")


        # 시각화 이미지 전송
        periods = ["7d", "30d", "1y"]
        period_names = {"7d": "지난 일주일", "30d": "지난 한 달", "1y": "지난 일 년"}

        for period in periods:
            # 데이터프레임 생성
            dataframes = fetch_data_from_influxdb(period)

            # 시각화 및 이미지 생성
            image_buffer = visualize_and_save_image(dataframes, period)

            # 텔레그램 메시지와 이미지 전송
            caption = f"📊 {period_names[period]}간의 기록.."

            await bot.send_photo(chat_id, photo=image_buffer, caption=caption)

        # 식물 상태 전송
        result = model_predict(latest_file)
        status = "🤗 식물이 건강해요!!" if result else "😥 식물이 아픈 거 같아요.."

        await bot.sendMessage(chat_id, text=status)
        await asyncio.sleep(2)
        return True
    except Exception as e:
        print(e)
        return None


# 타임랩스 조회 - 동영상 전송
async def send_video(chat_id):
    # request = request(read_timeout=60, connect_timeout=60)
    bot = telegram.Bot(token=load_telegram()[0])

    try:
        video_path = create_video_from_photos(video_lenth=10)

        await bot.send_video(chat_id, video_path)
        await asyncio.sleep(2)
        return True
    except Exception as e:
        print("Video Exception : ")
        print(e)
        return None

