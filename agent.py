import os
import json
import urllib.request
import urllib.error
from datetime import datetime

GEMINI_API_KEY = os.environ["GEMINI_API_KEY"]
DISCORD_WEBHOOK_URL = os.environ["DISCORD_WEBHOOK_URL"]

# 使用穩定版本的模型名稱
GEMINI_URL = (
    "https://generativelanguage.googleapis.com/v1beta/models/"
    "gemini-2.5-flash:generateContent?key=" + GEMINI_API_KEY
)

today = datetime.now().strftime("%Y年%m月%d日")
weekdays = ["一","二","三","四","五","六","日"]
weekday = weekdays[datetime.now().weekday()]


PROMPT = f"""今天是 {today}（星期{weekday}）。

你是每日語言學習 Agent。請幫我從以下來源各搜尋一則今日最新科技或時事新聞：
- 英語：The Verge (theverge.com)
- 日語：NHK Web (www3.nhk.or.jp)
- 韓語：朝鮮日報 (chosun.com)

請嚴格按照以下格式輸出，不要任何額外說明或 markdown 符號以外的內容：

📅 **{today}（週{weekday}）每日語言學習**
━━━━━━━━━━━━━━━━━━━━

🇺🇸 **【英語 EN】The Verge**
**標題：** （新聞標題）
**摘要：** （2句中文摘要）
**朗讀句：** （一句英文原句，適合朗讀）
**單字：** `word1` / `word2`

🇯🇵 **【日語 JA】NHK Web**
**標題：** （新聞標題）
**摘要：** （2句中文摘要）
**朗讀句：** （一句日文原句，適合朗讀）
**單字：** `単語1` / `単語2`

🇰🇷 **【韓語 KO】朝鮮日報**
**標題：** （新聞標題）
**摘要：** （2句中文摘要）
**朗讀句：** （一句韓文原句，適合朗讀）
**單字：** `단어1` / `단어2`

━━━━━━━━━━━━━━━━━━━━
✅ **今日學習目標**
> ☐ 讀完三篇，說出各篇主題
> ☐ 抄下 6 個單字至 Notion
> ☐ 大聲朗讀三句重點句 × 3 遍

_由語言學習 Agent 自動生成_"""


def call_gemini(prompt: str) -> str:
    payload = json.dumps({
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"temperature": 0.7, "maxOutputTokens": 1200}
    }).encode("utf-8")

    req = urllib.request.Request(
        GEMINI_URL,
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST"
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8")
        raise RuntimeError(f"Gemini API 錯誤 {e.code}: {body}") from e

    return data["candidates"][0]["content"]["parts"][0]["text"]


def send_to_discord(message: str) -> None:
    chunks = [message[i:i+1990] for i in range(0, len(message), 1990)]
    for chunk in chunks:
        payload = json.dumps({"content": chunk}).encode("utf-8")
        req = urllib.request.Request(
            DISCORD_WEBHOOK_URL,
            data=payload,
            headers={"Content-Type": "application/json"},
            method="POST"
        )
        try:
            with urllib.request.urlopen(req, timeout=10) as resp:
                status = resp.getcode()
        except urllib.error.HTTPError as e:
            body = e.read().decode("utf-8")
            raise RuntimeError(f"Discord Webhook 錯誤 {e.code}: {body}") from e

        if status not in (200, 204):
            raise RuntimeError(f"Discord webhook returned {status}")


def main():
    print(f"[{datetime.now().isoformat()}] Agent 啟動...")
    print("使用模型：gemini-1.5-flash-latest")
    print("呼叫 Gemini API 搜尋新聞...")
    message = call_gemini(PROMPT)
    print("新聞內容已產生，傳送至 Discord...")
    send_to_discord(message)
    print("✅ 完成！")


if __name__ == "__main__":
    main()
