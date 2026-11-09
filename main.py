import discord
import random
import asyncio
import os
from flask import Flask
from threading import Thread

# ==========================================
# Render가 봇을 재우지 않게 만드는 가짜 웹사이트
app = Flask('')

@app.route('/')
def home():
    return "봇 살아있음 ㅋㅋ"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()
# ==========================================

# 토큰은 깃허브에 올리면 밴 당하니까 Render 환경변수에서 가져옴
TOKEN = os.getenv("DISCORD_TOKEN")

# 트리거 명령어
START_TRIGGER = "!장애타"
STOP_TRIGGER = "!STOP"
SETTINGS_TRIGGER = "!설정"
SPEED_TRIGGER = "!스피드"
SPACE_TRIGGER = "!띄어쓰기"
NORMAL_TRIGGER = "!일반쓰기"
HELP_TRIGGER = "!기능"

# 단어 리스트
raw_words = "니애미,창년,개보지,말보지,저능아,열등종자,개새끼,니애미,창년,고아,시발,시발련,고아련,종자,장애,랑애,농아,븅신,병신,씨발,애미,애비,죽은,새끼,머저리,창녀,청년,느금마,느그애비,느그애미,니애비,씹보지,말랑보지,말보지,창년보지,죽은보지,헐렁보지,보지,자폐아,거지,좆거지,개거지,장애보지,개벌래보지"
words_list = raw_words.split(',')

# 4묶음으로 나누기
chunk_size = 10
chunks = [words_list[i:i + chunk_size] for i in range(0, len(words_list), chunk_size)]

def make_spam_message():
    c1 = random.choice(chunks[0]) if len(chunks) > 0 else ""
    c2 = random.choice(chunks[1]) if len(chunks) > 1 else ""
    c3 = random.choice(chunks[2]) if len(chunks) > 2 else ""
    c4 = random.choice(chunks[3]) if len(chunks) > 3 else ""
    
    if spam_mode == "space":
        combined = f"{c1}{c2}{c3}{c4}"
        return " ".join(combined)
    else:
        return f"{c1}{c2}{c3}{c4}"

client = discord.Client()
is_spamming = False
spam_delay = 1.0 
spam_mode = "normal" 

@client.event
async def on_ready():
    print(f"✅ 로그인 완료: {client.user}")

@client.event
async def on_message(message):
    global is_spamming, spam_delay, spam_mode
    
    if message.author.id != client.user.id:
        return

    if message.content == STOP_TRIGGER:
        if is_spamming:
            is_spamming = False
            await message.channel.send("STOP")
        return

    if message.content == HELP_TRIGGER:
        help_text = (
            "**[ 도배봇 기능 목록 ]**\n"
            f"`{START_TRIGGER}` : 도배 시작\n"
            f"`{STOP_TRIGGER}` : 도배 중지\n"
            f"`{SETTINGS_TRIGGER}` : 현재 속도 확인\n"
            f"`{SPEED_TRIGGER} [숫자]` : 속도 변경 (예: {SPEED_TRIGGER} 1.3)\n"
            f"`{SPACE_TRIGGER}` : 띄어쓰기 모드 (글자마다 띄어쓰기)\n"
            f"`{NORMAL_TRIGGER}` : 일반쓰기 모드 (글자 붙여서 쓰기 / 기본값)"
        )
        await message.channel.send(help_text)
        return

    if message.content == SPACE_TRIGGER:
        spam_mode = "space"
        await message.channel.send("띄어쓰기 모드로 변경됨.")
        return

    if message.content == NORMAL_TRIGGER:
        spam_mode = "normal"
        await message.channel.send("일반쓰기 모드로 변경됨.")
        return

    if message.content == SETTINGS_TRIGGER:
        await message.channel.send(f"현재 도배 속도: {spam_delay}초")
        return

    if message.content.startswith(SPEED_TRIGGER):
        parts = message.content.split(" ")
        if len(parts) == 2:
            try:
                new_delay = float(parts[1])
                if new_delay < 0.001:
                    new_delay = 0.001
                elif new_delay > 100.0:
                    new_delay = 100.0
                
                spam_delay = new_delay
                await message.channel.send(f"속도 변경됨: {spam_delay}초마다 전송")
            except ValueError:
                await message.channel.send("숫자만 입력해라")
        return

    if message.content == START_TRIGGER:
        if is_spamming:
            return 
        
        is_spamming = True
        
        while is_spamming:
            try:
                msg = make_spam_message()
                await message.channel.send(msg)
                await asyncio.sleep(spam_delay) 
            except discord.errors.HTTPException as e:
                if e.status == 429:
                    retry_after = e.response.headers.get('Retry-After', 2)
                    await asyncio.sleep(float(retry_after))
                else:
                    await asyncio.sleep(1)
            except Exception:
                await asyncio.sleep(1)

if __name__ == "__main__":
    keep_alive()
    client.run(TOKEN)
