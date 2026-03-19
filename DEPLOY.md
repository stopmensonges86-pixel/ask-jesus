# Demande a Jesus — Guide de Déploiement

## Backend : Render (gratuit)

1. Va sur https://render.com → "Get Started" → "Dashboard"
2. Clique **"New +"** → **"Web Service"**
3. Connecte ton compte **GitHub** et sélectionne ce repo (tu devras d'abord uploader sur GitHub)
4. Configure :
   - **Name** : `demande-a-jesus`
   - **Region** : Europe (Frankfurt)
   - **Branch** : main
   - **Root Directory** : `backend`
   - **Build Command** : `pip install -r requirements.txt`
   - **Start Command** : `gunicorn main:app --bind 0.0.0.0:$PORT`
5. Clique **"Advanced"** → **"Add Environment Variable"** :
   - `MINIMAX_API_KEY` = `sk-api-sf_z8KMxdzyNqHM42Wx1saZ3yr_lnBO5wTZiA3JRnB-GqarAtlKalEEjbeh0xvg_NNIbVcYFlLpsJXqsImzWXVPCrxOyWjMi0t0lR1Y9qvB1owNlM3gM3CQ`
6. **"Create Web Service"** (gratuit — délai de déploiement ~2-3 min)
7. Une fois déployé, copie l'URL : `https://demande-a-jesus.onrender.com`

## Problème API MiniMax — À corriger AVANT le déploiement

Le format de l'API MiniMax ne fonctionne pas avec `abab6.5-chat`.
Voir : `test_minimax.py` pour les tests.

**Action requise** : Une fois le backend déployé sur Render, ouvre un shell sur Render et teste :
```bash
curl -X POST https://api.minimaxi.chat/v1/chat/completions \
  -H "Authorization: Bearer SK-..." \
  -H "Content-Type: application/json" \
  -d '{"model":"MiniMax-01","messages":[{"role":"user","content":"hi"}],"max_tokens":3}'
```

## Frontend : Netlify (gratuit)

1. Va sur https://app.netlify.com/drop
2. Glisse-dépose le dossier `app/` depuis ce projet
3. Ton site est en ligne ! Copie l'URL Netlify

## Connecter frontend → backend

Dans `app/index.html`, modifie la ligne API endpoint :
```javascript
const API_URL = "https://demande-a-jesus.onrender.com";
```

## Upload vers GitHub (requis pour Render)

1. Crée un repo GitHub : `demande-a-jesus`
2. Upload les dossiers `backend/` et `app/`
3. Connecte le repo à Render
