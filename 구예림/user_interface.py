# 사용자 명령어 인터페이스
from telegram import Update
from telegram.ext import Application, MessageHandler, CommandHandler, filters, ContextTypes
import telegram_bot as tb
import asyncio


# 처음 접속 시 안내 메세지
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    pass


# 메시지 수신 핸들러
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    pass


# 알 수 없는 명령어 처리 핸들러
async def unknown_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    pass


# 메인 함수
async def main():
    # 어플리케이션 생성
    application = Application.builder().token(tb.load_telegram()).build()

    # 수신 메세지에 따른 핸들러 추가
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    application.add_handler(MessageHandler(filters.COMMAND, unknown_command))

    # 애플리케이션 초기화 및 실행
    await application.initialize()
    await application.start()
    await application.updater.start_polling()
    print("텔레그램 봇 실행...")

    try:
        while True:
            await asyncio.sleep(1)
    except KeyboardInterrupt:
        print("텔레그램 봇 종료...")
        await application.stop()


# 테스트 메인 함수
if __name__ == "__main__":
    asyncio.run(main())
