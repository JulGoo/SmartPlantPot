# 실시간 상태 보고 기능
import telegram
import telegram_bot as tb


# 일반 메세지 전송
async def send_chat(msg, chat_id):
    bot = telegram.Bot(token=tb.load_telegram()[0])
    await bot.sendMessage(chat_id, text=msg, parse_mode="Markdown")


# 식물 상태 분석 - 사진 전송
async def send_image(chat_id):
    bot = telegram.Bot(token=tb.load_telegram()[0])

    try:
        image_path = "test_image.jpg"
        ###### 최근에 찍은 식물 사진 불러오기 ####
        ########## def visualize_and_save_image()  :param period: '7d', '30d', '1y', or 'all' ##########################
        ################################### def visualize_and_save_image(dataframes, period) ###########################
        await bot.send_photo(chat_id, image_path)
    except Exception as e:
        print(e)
        return None
    return True


# 동영상 전송
async def send_video(chat_id):
    bot = telegram.Bot(token=tb.load_telegram()[0])

    try:
        video_path = "test_video.mp4"
        ################################ def create_video_from_photos() ################################################
        await bot.send_video(chat_id, video_path)
    except Exception as e:
        print(e)
        return None
    return True
