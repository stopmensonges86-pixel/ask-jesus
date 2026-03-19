import urllib.request, json, urllib.error, sys

api_key = sys.argv[1] if len(sys.argv) > 1 else 'sk-api-sf_z8KMxdzyNqHM42Wx1saZ3yr_lnBO5wTZiA3JRnB-GqarAtlKalEEjbeh0xvg_NNIbVcYFlLpsJXqsImzWXVPCrxOyWjMi0t0lR1Y9qvB1owNlM3gM3CQ'
url = 'https://api.minimaxi.chat/v1/chat/completions'

# Try various formats
tests = [
    # (model, extra_headers, extra_data)
    ('abab6.5-chat', {}, {}),
    ('abab6.5-chat', {'Content-Type': 'application/json'}, {'model': 'abab6.5-chat', 'messages': [{'role': 'user', 'content': 'hi'}], 'max_tokens': 3}),
    ('MiniMax-01', {'Content-Type': 'application/json'}, {'model': 'MiniMax-01', 'messages': [{'role': 'user', 'content': 'hi'}], 'max_tokens': 3}),
    ('abab6.5', {'Content-Type': 'application/json'}, {'model': 'abab6.5', 'messages': [{'role': 'user', 'content': 'hi'}], 'max_tokens': 3}),
    ('minimax/abab6.5-chat', {'Content-Type': 'application/json'}, {'model': 'minimax/abab6.5-chat', 'messages': [{'role': 'user', 'content': 'hi'}], 'max_tokens': 3}),
]

for name, extra_headers, data in tests:
    full_headers = {'Authorization': f'Bearer {api_key}'}
    full_headers.update(extra_headers)
    body = json.dumps(data).encode('utf-8')
    req = urllib.request.Request(url, data=body, headers=full_headers, method='POST')
    try:
        with urllib.request.urlopen(req, timeout=8) as resp:
            r = json.loads(resp.read())
            print(f'✅ OK model={name}:', r['choices'][0]['message']['content'])
    except urllib.error.HTTPError as e:
        err = e.read().decode()[:100]
        print(f'❌ ERR model={name}: {e.code} {err}')
