# 텔레그램 봇 인터페이스
import telegram
import os
from dotenv import load_dotenv


# 텔레그램 봇 토큰값 가져오기
def load_token():
    try:
        load_dotenv("token.env")
        return str(os.getenv("token"))
    # 토큰값을 못 가져왔을 때 예외 처리
    except Exception as e:
        print(e)
        return None



