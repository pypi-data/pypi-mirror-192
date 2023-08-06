import requests
import openai
import time
import uuid
import os

token = "v2.public.Q2lRMlpHUTRPV015WXkwNFl6QTBMVFZrTUdVdE9HWTNPQzFsTTJFMlptWmxOelZpTlRVU0IySmxiR2xsWm5NYUN6QnNlVVJST0ZKdVEwZFdJaVEzTURrek16RTJNQzB5WW1JeExUUTVNVEV0T0RSa1lTMDNORGc0TkdOaFpETTROalV5SkRJeU4yRXpNelUyTFdRMU5EY3ROR05rWVMxaFptRTBMVGd3TnpFNE5qVmlOelEwTmc9PZMliagwkWrAKPiUuygx7vk8Y6vxt8W7pjqkl9sfqCYBkRyU_Dqw_rK_vTwXpSpom0R3LG7zp_YqYPCpx66hig4.R0FFaUJtTnZibTFoYmhLV0IzWXlMbkIxWW14cFl5NVJNbVI2VTFOMFRsbHJVblZrTVd4U1dqQndSVmt3WkRSVFZYaEVWRmRWTTJWVVZUUlNNRlpSVVRGamVsRnVUbWhSVjJodVVtdGtjRmRWZEV0U1JuQnlWMnRTYms1V2JEWlRiWEJOVmtkb2NWUlZVbEprUlRWWVZWaGtZVlY2UVRCWGJYQnFUa1Y0V0ZaWWNGcFdSbkIwVjIweFZrMHdOVmhUVkVaUFZXMDVTMUpYWkd0aFZuQllaVWhDWVZZeGNEWlRWM0JYWTJzeGNFNVlaR3RXTUhCNldWWmtUbVJYVWxaT1NIQk5WbXMxZVZReGFHNWxiRXBYVm01R1VtRnJjRlZVYkdSelYwVXhjbU5GTlZCV1ZHZDVWbXRrTkUweVVrZFRibWhVWWtVd2QxWlhlRzlUTVVvMlZteENZVmRIZURSVVZVVTVVR0Y1VldGQmVqUkJWekZxZEdSd2JIUkJjWGRuWjBkSFFVaE9TMjVmYzBSTGJ6ZzFhRUZETTNWalpUbENkR3d4YjBoR01uTnBWRmRZVjBSVVdtRmxYM2R2ZEhkVFoyczNRbFZSWm5Oek9EQm1RakJEVG1kSkxsSXdSa1poVlVwMFZHNWFhV0pVUm05WmJXaE1UV3RHZFZkWWJFMWlhMGw0VjFjeE5HTkdiRFZPVmtwT1lsWkpNbFpVUm10bGJVNXpVbGhzVldKck5XaFVWbVEwVlRGc1ZWTnRSbFpTYmtKSVZrY3dOVlpHV2xsaFJWWldaV3RKTUZVeFpFcGxWa3B6VjJ4T1RsSnNjRkZXYTFKRFVqSlNXRkpZYkZCV01taFRWbXBLYjJSV1ZsaGtSM1JwWWtVMVdGbHJWazlXYlVwVllrVldWbUZyU2toVk1uaHpWbXhLZEU5WFJrNVNhM0JLVmpKd1EyTXhaSE5TYmtwVllUTkNUMVpxUWxwTmJGVjRZVVprYUdKRk5VaFdNalZEVjIxRmVWVnVjRnBXTTFFd1drWmFTMlJGTVZoaFJrNVRZVEZXTTFacVFsTlJNVmw1VkZob1UySnNTbFJaYlhoM1ZERmFjbGR1WkZSU2JGWTBWbTF6TldGV1NuUmxTSEJhVFVaVk1WWnJaRXRTTWs1SllVWmtVMVp1UW5sV1ZsSkhVakpTV0ZOclZsTmlSMmh2VkZSS2EwNVdXbGhOVkU1UFZtMVNTRlV5ZUZkVmJVcDBWVzVPVjJKVVJUQlpWVnBoVm0xR1NHTkdSbGRpUlZwNFdUQldSbVZWTkhwalIyeFBVakExVWxsdE1WZGtSbEpJV2tod1YxSkhVak5hUkVKTFlqRlZkMk5HYUZkV1JYQktWbXhvUWsxV1VYaGlSRVpQWVd4S01Wa3haSEprTVVaWVUycENUbUV6VVhsWmFrcDJUa2RLUmxWdWFGWmlWbHB5Vm14YVQxRXlVWGhhUnpWclVtcHJkMWRZY0VOVFJteDBZVWhPWVZWNlFqQlpWRTVXWlcxS1JtRjZVbXhXUlRWUlYyNXdRbVJXVm5GUmEyUlRZbFZhVjFVeU5WTldWMHB6WTBoQ1dtSkdTa2haYWtaelpFWndTVmRzVGs1aGVsWkxWbFJKTVZsV2JGZFRhMmhRVTBkak9RPT0"
openai.api_key = "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"


def __flag__():
    return requests.post("https://chat-api.beliefs.repl.co/api/flag").json()["flags"]


def __ai_train__(q: str):
    if q != None:
        completions = openai.Completion.create(
            engine="text-davinci-003",
            prompt=q,
            max_tokens=1024,
            n=1,
            stop=None,
            temperature=0.5,
        )

        return {
            "error": False,
            "message": completions.choices[0].text.strip(),
            "cid": uuid.uuid4(),
        }


class client:
    def __init__(this, debug):
        this.debug = debug
        this.api = {
            "flag": "https://chat-api.beliefs.repl.co/api/flag",
            "get_flags": "https://chat-api.beliefs.repl.co/api/user/flags",
            "ask": "https://chat-api.beliefs.repl.co/api/ask",
            "train": "https://chat-api.beliefs.repl.co/api/train",
            "pre-trained": "https://chat-bot-server-LZlub.lzulb.repl.co/get-resp",
        }
        this.session = requests.Session()

    def train(this, question: str, answer=None, phrase=None, ai=None):
        if this.debug == True:
            print(f"[DEBUG] Timestamp: {time.time()}\n[DEBUG] Function Called: train\n")
            time.sleep(1.5)
            os.system("clear")

        if ai == True:
            return this.session.put(
                this.api["train"],
                json={
                    "q": question,
                    "answer": __ai_train__(question),
                    "phrase": phrase,
                },
            ).json()
          
        return this.session.put(
            this.api["train"], json={"q": question, "answer": answer, "phrase": phrase}
        ).json()

    def ask(this, question: str, ai: None):
        if this.debug == True:
            print(f"[DEBUG] Timestamp: {time.time()}\n[DEBUG] Function Called: ask\n")
            time.sleep(1.5)
            os.system("clear")
          
        if ai == True:
            return __ai_train__(question)

        return this.session.post(
            this.api["ask"], json={"q": question, "ts": time.time()}
        ).json()
