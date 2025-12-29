from workers import Response
import json

async def fetch(request, env, ctx):
    # 텔레그램은 POST 방식으로 데이터를 보냅니다.
    if request.method == "POST":
        try:
            payload = await request.json()
            chat_id = payload['message']['chat']['id']
            text = payload['message'].get('text', '')

            # 응답 메시지 작성
            reply = f"Python Worker에서 보냄: {text}"
            
            # 텔레그램 API 호출 (환경변수 env.TELEGRAM_TOKEN 사용)
            url = f"https://api.telegram.org/bot{env.TELEGRAM_TOKEN}/sendMessage"
            
            # Cloudflare의 내장 fetch 사용
            await fetch(url, method="POST", headers={"Content-Type": "application/json"}, 
                        body=json.dumps({"chat_id": chat_id, "text": reply}))
            
        except Exception as e:
            return Response.json({"error": str(e)}, status=500)

    return Response.json({"status": "ok"})