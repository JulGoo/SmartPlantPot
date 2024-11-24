# 텔레그램 봇
import asyncio

import telegram

import os
from dotenv import load_dotenv


# 텔레그램 봇 토큰값과 채팅 아이디 가져오기
def load_telegram():
    try:
        load_dotenv("telegram.env")
        token = str(os.getenv("token"))
        chat_id = str(os.getenv("chatID"))

        # 토큰과 채팅 ID가 제대로 로드되었는지 확인
        if not token or not chat_id:
            raise ValueError("토큰 또는 채팅 ID가 누락되었습니다.")

        return token, chat_id
    except Exception as e:
        print(f"Error loading telegram configuration: {e}")
        return None, None


# 일반 메세지 전송
async def send_chat(msg, chat_id):
    bot = telegram.Bot(token=load_telegram()[0])
    await bot.sendMessage(chat_id, text=msg, parse_mode="Markdown")


# 식물 상태 분석 - 사진 전송
async def send_image(chat_id):
    bot = telegram.Bot(token=load_telegram()[0])

    try:
        image_path = "test_image.jpg"
        ###### 최근에 찍은 식물 사진 불러오기 ####
        ########## def visualize_and_save_image()  :param period: '7d', '30d', '1y', or 'all' ##########################
        ################################### def visualize_and_save_image(dataframes, period) ###########################
        await bot.send_photo(chat_id, image_path)
        return True
    except Exception as e:
        print(e)
        return None


# 타임랩스 조회 - 동영상 전송
async def send_video(chat_id):
    # request = request(read_timeout=60, connect_timeout=60)
    bot = telegram.Bot(token=load_telegram()[0])

    try:
        video_path = "test_video.mp4"
        ################################ def create_video_from_photos() ################################################
        await bot.send_video(chat_id, video_path)
        await asyncio.sleep(2)
        return True
    except Exception as e:
        print("Video Exception : ")
        print(e)
        return None

