# 英日韓每日語言學習 Agent

每天早上 09:00（台灣時間）自動抓取 The Verge、NHK、朝鮮日報最新新聞，整理後推送到 Discord。

## 架構

```
GitHub Actions（每天 09:00 觸發）
    ↓
agent.py 呼叫 Gemini API 搜尋新聞並整理
    ↓
Discord Webhook 推送訊息
```

---

## 設定步驟

### 步驟 1：取得 Gemini API Key（免費）

1. 前往 https://aistudio.google.com/app/apikey
2. 登入 Google 帳號
3. 點「Create API Key」
4. 複製 Key 備用

---

### 步驟 2：建立 Discord Webhook

1. 打開你的 Discord 伺服器
2. 在目標頻道上按右鍵 → **「編輯頻道」**
3. 左側選「**整合**」→「**Webhook**」
4. 點「**新 Webhook**」→ 命名（如：語言學習 Agent）
5. 點「**複製 Webhook 網址**」備用

---

### 步驟 3：建立 GitHub Repository

1. 前往 https://github.com/new
2. Repository 名稱：`language-agent`（或任意名稱）
3. 設為 **Private**
4. 點「Create repository」
5. 把這個資料夾的所有檔案上傳進去：
   - `agent.py`
   - `.github/workflows/daily_agent.yml`
   - `README.md`

---

### 步驟 4：設定 Secrets

1. 在 GitHub repo 頁面，點上方「**Settings**」
2. 左側選「**Secrets and variables**」→「**Actions**」
3. 點「**New repository secret**」，新增以下兩個：

| Name | Value |
|------|-------|
| `GEMINI_API_KEY` | 步驟 1 取得的 Key |
| `DISCORD_WEBHOOK_URL` | 步驟 2 取得的 Webhook 網址 |

---

### 步驟 5：測試

1. 進入 repo 的「**Actions**」頁籤
2. 左側點「每日語言學習 Agent」
3. 右側點「**Run workflow**」→「Run workflow」
4. 等約 30 秒，檢查 Discord 頻道是否收到訊息

---

## 費用

| 項目 | 費用 |
|------|------|
| GitHub Actions | 免費（Public repo 無限；Private repo 每月 2000 分鐘） |
| Gemini API | 免費（每分鐘 15 次、每天 1500 次請求） |
| Discord Webhook | 完全免費 |

每天只跑一次，**完全在免費額度內**。

---

## 自訂調整

- **修改新聞來源**：編輯 `agent.py` 中 `PROMPT` 的來源說明
- **修改發送時間**：編輯 `.github/workflows/daily_agent.yml` 中的 `cron`（UTC 時間）
- **修改語言或格式**：直接修改 `agent.py` 中的 `PROMPT`
