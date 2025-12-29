from js import Response, fetch, Headers
import json

async def on_fetch(request, env):
    # POST 요청인 경우에만 처리
    if request.method == "POST":
        try:
            # 텔레그램에서 보낸 데이터 읽기
            body = await request.json()
            message = body.get("message", {})
            chat_id = message.get("chat", {}).get("id")
            text = message.get("text", "")

            # 사용자가 /run 명령어를 보냈을 때
            if text == "/run":
                # 1. GitHub API 호출 설정
                github_url = f"https://api.github.com/repos/{env.GITHUB_USER}/{env.GITHUB_REPO}/dispatches"
                github_headers = {
                    "Authorization": f"Bearer {env.GITHUB_TOKEN}",
                    "Accept": "application/vnd.github.v3+json",
                    "User-Agent": "Cloudflare-Worker-Python"
                }
                github_payload = json.dumps({"event_type": "telegram_trigger"})

                # 2. GitHub에 신호 보내기
                gh_res = await fetch(github_url, method="POST", headers=github_headers, body=github_payload)

                if gh_res.ok:
                    # 3. 성공 시 텔레그램으로 답장 보내기
                    tg_url = f"https://api.telegram.org/bot{env.TELEGRAM_TOKEN}/sendMessage"
                    tg_payload = json.dumps({
                        "chat_id": chat_id,
                        "text": "🐍 (Python Worker) 요청을 확인했습니다! GitHub Actions를 실행합니다."
                    })
                    await fetch(tg_url, method="POST", headers={"Content-Type": "application/json"}, body=tg_payload)

            return Response.new("OK")
        except Exception as e:
            return Response.new(f"Error: {str(e)}")

    return Response.new("Python Worker is running!")
