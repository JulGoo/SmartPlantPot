# 텔레그램 봇 인터페이스
import telegram
import os
from dotenv import load_dotenv


# 텔레그램 봇 토큰값과 채팅 아이디 가져오기
def load_telegram():
    try:
        load_dotenv("telegram.env")
        token = str(os.getenv("token"))
        chat_id = str(os.getenv("chatID"))
        return token, chat_id
    # 토큰값과 채팅 아이디를 못 가져왔을 때 예외 처리
    except Exception as e:
        print(e)
        return None, None


