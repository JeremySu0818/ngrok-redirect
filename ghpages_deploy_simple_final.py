# -*- coding: utf-8 -*-
"""
簡易自動部署腳本 - 加入 origin 遠端設定

此版本會：
1. 啟動本地伺服器 (若存在 index.js)
2. 關閉舊有 ngrok 進程
3. 啟動 ngrok 並取得公網網址
4. 生成或更新 index.html
5. 設定遠端 origin（若不存在）
6. 提交並推送 index.html 到 main 分支

使用前請確認：
- 已安裝 Node.js、ngrok、Git，且已設定好 git user.name & user.email
- GitHub Pages 設定為 main 分支根目錄 (/)
- 修改下方參數：REPO_DIR、NGROK_PATH、LOCAL_PORT、GIT_URL
"""

import os
import subprocess
import time
import json

# ===== 參數設定 =====
NGROK_PATH = "ngrok"  # ngrok 執行檔路徑
LOCAL_PORT = 3000     # 本地伺服器埠號
REPO_DIR = r"C:\星泓 原D槽\星泓 檔案\星泓 電腦\程式\網頁\專案\xzquotes"  # 專案本機目錄
GIT_URL   = "https://github.com/JeremySu0818/ngrok-redirect.git"           # 遠端儲存庫 URL
HTML_FILE = "index.html"  # 跳轉頁檔名

# 切換到專案目錄
os.chdir(REPO_DIR)

# 步驟1：啟動本地伺服器(若有 index.js)
if os.path.exists("index.js"):
    print("步驟1：啟動本地伺服器 index.js…")
    subprocess.Popen(["node", "index.js"], cwd=REPO_DIR)
    time.sleep(3)
else:
    print("警告：未找到 index.js，跳過本地伺服器啟動")

# 步驟2：關閉舊有 ngrok 進程
print("步驟2：關閉所有現有 ngrok 進程…")
subprocess.run(["taskkill", "/F", "/IM", "ngrok.exe"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

# 步驟3：啟動 ngrok 並取得網址
print("步驟3：啟動 ngrok…")
subprocess.Popen([NGROK_PATH, "http", str(LOCAL_PORT)], cwd=REPO_DIR, stdout=subprocess.DEVNULL)
time.sleep(3)
res = subprocess.check_output(["curl", "-s", "http://127.0.0.1:4040/api/tunnels"])
url = json.loads(res)['tunnels'][0]['public_url']
print(f"✔ ngrok 公網網址：{url}")

# 步驟4：生成或更新 index.html
print("步驟4：生成或更新 index.html…")
html = f"<html><head><meta http-equiv=\"refresh\" content=\"0; url={url}\"><script>location.href='{url}'</script></head><body>Redirecting…</body></html>"
with open(HTML_FILE, "w", encoding="utf-8") as f:
    f.write(html)

# 步驟5：設定遠端 origin
print("步驟5：設定遠端 origin…")
# 若 origin 不存在則添加
remotes = subprocess.check_output(["git", "remote"], text=True)
if "origin" not in remotes.split():
    subprocess.run(["git", "remote", "add", "origin", GIT_URL], check=True)

# 步驟6：提交並推送 index.html
print("步驟6：提交並推送 index.html…")
subprocess.run(["git", "add", HTML_FILE], check=True)
subprocess.run(["git", "commit", "-m", "deploy: 更新跳轉頁面"], check=True)
subprocess.run(["git", "push", "-u", "origin", "main"], check=True)

print("✅ 部署完成！訪問：https://jeremysu0818.github.io/ngrok-redirect/ 即可跳轉到最新 ngrok 網址")