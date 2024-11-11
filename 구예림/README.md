# 텔레그램 봇 연동
## 텔레그램에서 봇 생성(BotFather 사용)
### 이름: SmartPlantPot44_bot

## 라이브러리 설치
```
pip install python-telegram-bot --upgrade
```

# dotenv를 활용한 Token 및 ChatID 가져오기
## 단일 사용자로 가정 후 테스트
토큰값을 넣어 채팅 아이디를 확인
```
https://api.telegram.org/bot[Token]/getUpdates
```
<br>

* 프로젝트 디렉토리에 `.env` 파일을 생성한 후, 봇의 **토큰 값**과 **채팅 아이디**를 추가
* **.gitignore**에 **.env**파일 추가 (**비공개 처리**)

## `python-dotenv` 설치
`.env` 파일의 값을 파이썬 코드에서 읽어오기 위해 `python-dotenv` 라이브러리를 설치
```
pip install python-dotenv
```




