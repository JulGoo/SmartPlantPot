# 사용자 명령어 인터페이스
from telegram import Update, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, MessageHandler, CommandHandler, filters, ContextTypes
import status_report as sr
import telegram_bot as tb
import asyncio


# 처음 접속 시 안내 메세지
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = ("안녕하세요!\n"
           "똑똑한 식물 관리 플랫폼\n"
           "\"Smart Plant Pot\" 입니다!\n"
           "\n"
           "다음 번호를 선택해주세요.")

    # GUI 버튼으로 선택지 구성
    keyboard = [
        [
            InlineKeyboardButton("1. 도움말", callback_data="help"),
            InlineKeyboardButton("2. 식물설정", callback_data="plant_setting"),
        ],
        [
            InlineKeyboardButton("3. 식물상태분석", callback_data="plant_analysis"),
            InlineKeyboardButton("4. 타임랩스받기", callback_data="get_timelapse"),
        ],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # 메세지 전송
    await update.message.reply_text(
        msg,
        reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    )


# 메시지 수신 핸들러
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    chat_id = update.message.chat_id
    msg = f"'{user_message}' 는 없는 선택지입니다. 다시 입력해주세요."

    # 메시지에 따라 행동 정의
    if ("1" in user_message) or ("도움말" in user_message):
        msg = ("명령어 도움말 입니다.\n"
               "1. 도움말\n"
               "2. 식물설정\n"
               "3. 식물상태분석\n"
               "4. 타임랩스")
    elif ("2" in user_message) or ("식물설정" in user_message):
        msg = ("식물을 선택해주세요.\n"
               "1. 바나나\n"
               "2. 망고")
    elif ("3" in user_message) or ("식물상태분석" in user_message):
        result = await sr.send_image(chat_id)
        if result is None:
            msg = "사진 파일이 없습니다."
        else:
            msg = "식물 상태 분석 결과 입니다."
    elif ("4" in user_message) or ("타임랩스받기" in user_message):
        result = await sr.send_video(chat_id)
        if result is None:
            msg = "타임랩스 영상이 없습니다."
        else:
            msg = "현재까지 촬영된 타임랩스 영상 입니다."

    await update.message.reply_text(msg)


# 알 수 없는 명령어 처리 핸들러
async def unknown_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("잘못된 명령어입니다. 다시 입력해주세요.")


# 메인 함수
async def main():
    # 어플리케이션 생성
    application = Application.builder().token(tb.load_telegram()[0]).build()

    # 수신 메세지에 따른 핸들러 추가
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    application.add_handler(MessageHandler(filters.COMMAND, unknown_command))

    # 애플리케이션 초기화 및 실행
    await application.initialize()
    await application.start()
    # 대기 상태(메세지 수신 상태 확인)
    await application.updater.start_polling()
    print("텔레그램 봇 실행...")

    try:
        while True:
            # 1초 간격으로 대기 상태 유지
            await asyncio.sleep(1)
    except KeyboardInterrupt:
        print("텔레그램 봇 종료...")
        await application.stop()


# 테스트 메인 함수
if __name__ == "__main__":
    asyncio.run(main())
