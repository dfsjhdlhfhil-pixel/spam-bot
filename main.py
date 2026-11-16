import discord
import random
import asyncio
import os
import threading
import time
from flask import Flask

# ==========================================
# Render가 봇을 재우지 않게 만드는 가짜 웹사이트
# ==========================================
app = Flask('')

@app.route('/')
def home():
    return "봇 살아있음 ㅋㅋ"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = threading.Thread(target=run)
    t.daemon = True
    t.start()

# ==========================================
# ★ 렌더 환경변수에서 토큰 불러오기 ★
# ==========================================
TOKEN = os.getenv("DISCORD_TOKEN") 

if not TOKEN:
    print("❌ 렌더 환경변수(Environment)에 DISCORD_TOKEN 값을 넣어주세요.")
    exit(1)

# ★ 니 부계 디스코드 ID ★
OWNER_ID = 123456789012345678 # 니 부계 ID로 수정해라! (따옴표 X)

# 명령어
START_TRIGGER = "!장애타"
STOP_TRIGGER = "!STOP"
SETTINGS_TRIGGER = "!설정"
SPEED_TRIGGER = "!스피드"
SPACE_TRIGGER = "!띄어쓰기"
NORMAL_TRIGGER = "!일반쓰기"
HELP_TRIGGER = "!기능"
SPAM_TRIGGER = "!spam"
MENTION_TRIGGER = "!갠디" # DM으로 보내는 명령어
DOBAE_TRIGGER = "!도배"   # 채널에 보내는 명령어

# 일반 도배용 단어장
raw_words = "니애미,창년,개보지,말보지,저능아,열등종자,개새끼,고아,시발,시발련,고아련,종자,장애,랑애,농아,븅신,병신,씨발,애미,애비,죽은,새끼,머저리,창녀,청년,느금마,느그애비,느그애미,니애비,씹보지,말랑보지,말보지,창년보지,죽은보지,헐렁보지,보지,자폐아,거지,좆거지,개거지,장애보지,개벌래보지"
words = raw_words.split(',')

# 멘션 테러용 랜덤 숫자/문자열
random_nums = [
    "100", "9339", "34554", "4313", "6436", "2521", "1343", "14111", "4059", "2849", "324", "38204", "14323", "1357", "168", "447", "4754", "INF", "2314", "6352", "5152", "5736", "9474", "0424", "7346", "1453", "15462", "5231", "5155",
    "4143", "4314", "135", "635", "5513", "45734", "65E8", "47WQ4", "", "5WQ", "GRSA", "GS", "YHRD", "FEA", "TE", "THRW", "RGATBE", "grW", "GR", "rg", "grrg", "arg", "arghr", "reER", "ESAH", "TAE", "HAFD"
]

# 공통 텍스트 양식
terror_text = "현월 업인데 너컷이야 병신새끼야 현월라인을 찬양해라 너병신 갠디 태러 당하네? 병신새끼네? 너컷이네병신아? {num}"

class SpamClient(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.is_spamming = False
        self.spam_content = ""
        self.spam_delay = 1.0 
        self.spam_mode = "normal"

    def make_spam_message(self):
        c1 = random.choice(words)
        c2 = random.choice(words)
        c3 = random.choice(words)
        c4 = random.choice(words)
        
        if self.spam_mode == "space":
            combined = f"{c1}{c2}{c3}{c4}"
            return " ".join(combined)
        else:
            return f"{c1}{c2}{c3}{c4}"

    async def on_ready(self):
        print(f"✅ 로그인 완료: {self.user}")

    async def on_message(self, message):
        if message.author.id != self.user.id and message.author.id != OWNER_ID:
            return

        # 1. 전체 중지 (!STOP)
        if message.content == STOP_TRIGGER:
            if self.is_spamming:
                self.is_spamming = False
                await message.channel.send("STOP")
            return

        # 2. 기능 목록
        if message.content == HELP_TRIGGER:
            help_text = (
                "**[ 도배봇 기능 목록 ]**\n"
                f"`{START_TRIGGER}` : 일반 도배 시작\n"
                f"`{STOP_TRIGGER}` : 도배 중지\n"
                f"`{SETTINGS_TRIGGER}` : 현재 속도 확인\n"
                f"`{SPEED_TRIGGER} [숫자]` : 속도 변경 (예: !스피드 1.3)\n"
                f"`{SPACE_TRIGGER}` : 띄어쓰기 모드\n"
                f"`{NORMAL_TRIGGER}` : 일반쓰기 모드\n"
                f"`{SPAM_TRIGGER} [문장]` : 입력한 문장 반복 도배\n"
                f"`{MENTION_TRIGGER} @유저` : 해당 유저의 DM으로 지랄 도배\n"
                f"`{DOBAE_TRIGGER} @유저` : 현재 채널에 지랄 도배"
            )
            await message.channel.send(help_text)
            return

        # 3. 띄어쓰기 모드
        if message.content == SPACE_TRIGGER:
            self.spam_mode = "space"
            await message.channel.send("띄어쓰기 모드로 변경됨.")
            return

        # 4. 일반쓰기 모드
        if message.content == NORMAL_TRIGGER:
            self.spam_mode = "normal"
            await message.channel.send("일반쓰기 모드로 변경됨.")
            return

        # 5. 속도 확인
        if message.content == SETTINGS_TRIGGER:
            await message.channel.send(f"현재 도배 속도: {self.spam_delay}초")
            return

        # 6. 속도 변경
        if message.content.startswith(SPEED_TRIGGER):
            parts = message.content.split(" ")
            if len(parts) == 2:
                try:
                    new_delay = float(parts[1])
                    if new_delay < 0.001:
                        new_delay = 0.001
                    elif new_delay > 100.0:
                        new_delay = 100.0
                    
                    self.spam_delay = new_delay
                    await message.channel.send(f"속도 변경됨: {self.spam_delay}초마다 전송")
                except ValueError:
                    await message.channel.send("숫자만 입력해라")
            return

        # 7. 커스텀 텍스트 도배 (!spam)
        if message.content.startswith(SPAM_TRIGGER):
            text_to_spam = message.content[len(SPAM_TRIGGER):].strip()
            if not text_to_spam:
                return
            if self.is_spamming:
                return
            
            self.is_spamming = True
            self.spam_content = text_to_spam
            
            while self.is_spamming:
                try:
                    await message.channel.send(self.spam_content)
                    wait_time = max(0.1, self.spam_delay - 0.2)
                    await asyncio.sleep(wait_time) 
                except discord.errors.HTTPException as e:
                    if e.status == 429:
                        retry_after = e.response.headers.get('Retry-After', 2)
                        await asyncio.sleep(float(retry_after) + 0.5)
                    else:
                        await asyncio.sleep(1)
                except Exception:
                    await asyncio.sleep(1)
            return

        # 8. 채널 도배 (!도배 @유저) - 명령어 친 채널에 도배
        if message.content.startswith(DOBAE_TRIGGER):
            if self.is_spamming:
                return
            
            if not message.mentions:
                return
            
            target_user = message.mentions[0]
            if target_user.id == self.user.id or target_user.id == OWNER_ID:
                return

            self.is_spamming = True
            
            while self.is_spamming:
                try:
                    num = random.choice(random_nums)
                    msg = f"{target_user.mention} " + terror_text.format(num=num)
                    await message.channel.send(msg) # 내가 명령어 친 채널로 전송
                    wait_time = max(0.1, self.spam_delay - 0.2)
                    await asyncio.sleep(wait_time) 
                except discord.errors.HTTPException as e:
                    if e.status == 429:
                        retry_after = e.response.headers.get('Retry-After', 2)
                        await asyncio.sleep(float(retry_after) + 0.5)
                    else:
                        await asyncio.sleep(1)
                except Exception:
                    await asyncio.sleep(1)
            return

        # 9. 개인 디엠 도배 (!갠디 @유저) - 대상 유저의 DM으로 전송
        if message.content.startswith(MENTION_TRIGGER):
            if self.is_spamming:
                return
            
            if not message.mentions:
                return
            
            target_user = message.mentions[0]
            if target_user.id == self.user.id or target_user.id == OWNER_ID:
                return 

            self.is_spamming = True
            
            # 상대방과의 DM 채널 열기
            try:
                dm_channel = await target_user.create_dm()
            except Exception:
                await message.channel.send("DM을 보낼 수 없습니다. (상대방이 DM을 막았거나 친구가 아님)")
                self.is_spamming = False
                return

            while self.is_spamming:
                try:
                    num = random.choice(random_nums)
                    msg = terror_text.format(num=num)
                    await dm_channel.send(msg) # 상대방 DM으로 전송
                    wait_time = max(0.1, self.spam_delay - 0.2)
                    await asyncio.sleep(wait_time) 
                except discord.errors.HTTPException as e:
                    if e.status == 429:
                        retry_after = e.response.headers.get('Retry-After', 2)
                        await asyncio.sleep(float(retry_after) + 0.5)
                    else:
                        await asyncio.sleep(1)
                except Exception:
                    await asyncio.sleep(1)
            return

        # 10. 일반 도배 시작 (!장애타)
        if message.content == START_TRIGGER:
            if self.is_spamming:
                return 
            
            self.is_spamming = True
            
            while self.is_spamming:
                try:
                    msg = self.make_spam_message()
                    await message.channel.send(msg)
                    wait_time = max(0.1, self.spam_delay - 0.2)
                    await asyncio.sleep(wait_time) 
                except discord.errors.HTTPException as e:
                    if e.status == 429:
                        retry_after = e.response.headers.get('Retry-After', 2)
                        await asyncio.sleep(float(retry_after) + 0.5)
                    else:
                        await asyncio.sleep(1)
                except Exception:
                    await asyncio.sleep(1)

# ==========================================
# 봇 실행
# ==========================================
def run_bot(token):
    client = SpamClient()
    client.run(token)

keep_alive()
run_bot(TOKEN)
