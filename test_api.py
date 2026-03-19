import urllib.request, json, urllib.error

api_key = 'sk-api-sf_z8KMxdzyNqHM42Wx1saZ3yr_lnBO5wTZiA3JRnB-GqarAtlKalEEjbeh0xvg_NNIbVcYFlLpsJXqsImzWXVPCrxOyWjMi0t0lR1Y9qvB1owNlM3gM3CQ'
url = 'https://api.minimaxi.chat/v1/chat/completions'

models = ['MiniMax-01', 'minimax-01', 'MiniMax-M2', 'abab5.5-chat', 'abab6-chat', 'abab6.5', 'gpt-4o-mini', 'gpt-4o', 'chat-4o']

for model in models:
    data = {'model': model, 'messages': [{'role': 'user', 'content': 'hi'}], 'max_tokens': 5}
    body = json.dumps(data).encode('utf-8')
    req = urllib.request.Request(url, data=body, headers={
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {api_key}'
    }, method='POST')
    try:
        with urllib.request.urlopen(req, timeout=5) as resp:
            r = json.loads(resp.read())
            print(f'OK {model}:', r['choices'][0]['message']['content'])
    except urllib.error.HTTPError as e:
        print(f'ERR {model}:', e.code, e.read().decode()[:80])
