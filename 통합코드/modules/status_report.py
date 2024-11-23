# 실시간 상태 보고 기능
import telegram
import telegram_bot as tb


# 일반 메세지 전송
async def send_chat(msg, chat_id):
    bot = telegram.Bot(token=tb.load_telegram()[0])
    await bot.sendMessage(chat_id, text=msg, parse_mode="Markdown")


# 사진 전송
async def send_image(chat_id):
    bot = telegram.Bot(token=tb.load_telegram()[0])

    try:
        image_path = "test_image.jpg"
        await bot.send_photo(chat_id, image_path)
    except Exception as e:
        print(e)
        return None
    return True


# 동영상 전송
async def send_video(chat_id):
    bot = telegram.Bot(token=tb.load_telegram()[0])

    # 에러 수정 필요
    # File "/var/lib/engine/tmpfs_numa0/test_video.mp4" of size 14598977 bytes is too big for a photo
    try:
        video_path = "test_video.mp4"
        await bot.send_photo(chat_id, video_path)
    except Exception as e:
        print(e)
        return None
    return True
