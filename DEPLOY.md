# Deploying the SENTINEL backend (free tier)

Stack: **Render** (free web service) + **Aiven** (free, always-on MySQL).
No credit card required for either.

The code already reads all settings from environment variables, so deployment
is mostly configuration. Tables (`users`, `reports`, `emergencies`,
`emergency_contacts`) are created automatically on first boot.

---

## 1. Create the database on Aiven

1. Sign up at https://aiven.io (GitHub login works).
2. **Create service → MySQL → Free plan**. Pick a cloud/region close to you.
3. Wait until the service status is **Running**.
4. Open the service's **Overview** tab and copy the connection details:
   - Host  -> `DB_HOST`
   - Port  -> `DB_PORT`
   - User  -> `DB_USER`
   - Password -> `DB_PASSWORD`
   - Database name (default `defaultdb`) -> `DB_NAME`
5. Still on Overview, click **CA certificate → Download** (or "Show").
   Copy the entire PEM, including the
   `-----BEGIN CERTIFICATE-----` / `-----END CERTIFICATE-----` lines.
   This becomes `DB_CA_CERT`.

> Aiven requires TLS. `database.py` writes `DB_CA_CERT` to a temp file and uses
> it for both the SQLAlchemy engine and the raw `mysql.connector` pool.

---

## 2. Push the latest code to GitHub

This repo's remote is already `rishwanthkc/sentinel-backend`. From the
`sentinel-backend` folder:

```bash
git add requirements.txt app/main.py app/database.py Procfile render.yaml .env.example DEPLOY.md
git commit -m "Prepare backend for Render + Aiven deployment"
git push origin main
```

(`.env` stays out of git — it is in `.gitignore`.)

---

## 3. Deploy the API on Render

1. Sign up at https://render.com (GitHub login).
2. **New → Web Service → Build and deploy from a Git repository**, pick
   `sentinel-backend`.
3. Render auto-detects Python. Confirm:
   - **Build command:** `pip install -r requirements.txt`
   - **Start command:** `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
   - **Instance type:** Free
4. Add the **Environment Variables** from step 1:
   `DB_HOST`, `DB_PORT`, `DB_USER`, `DB_PASSWORD`, `DB_NAME`, `DB_CA_CERT`.
   For `DB_CA_CERT`, paste the full PEM (multi-line is fine).
5. Click **Create Web Service**. First build takes a few minutes.

> Alternatively, the included `render.yaml` lets you use Render **Blueprints**
> (New → Blueprint) — you still fill in the env vars, which are marked
> `sync: false` so they are never committed.

---

## 4. Verify

When the deploy is live you'll get a URL like
`https://sentinel-backend-xxxx.onrender.com`.

- Open `https://<your-app>.onrender.com/`  -> `{"message":"SENTINEL Backend Running"}`
- Open `https://<your-app>.onrender.com/health` -> `{"status":"ok"}`
- Open `https://<your-app>.onrender.com/docs` -> interactive API docs.

> Free Render services sleep after ~15 min idle; the first request afterwards
> takes ~30-60s to wake. That's expected on the free tier.

---

## 5. Point the apps at the deployed API

**Web app** — `sentinel-web/.env`:

```
VITE_API_BASE_URL=https://<your-app>.onrender.com
```

Then redeploy / restart the web dev server.

**Android app** — `sentinel-android/.../api/RetrofitClient.kt`:

```kotlin
private const val BASE_URL = "https://<your-app>.onrender.com/"
```

(Also update `network_security_config.xml` if it pins cleartext/IP hosts —
HTTPS to a public domain needs no cleartext exception.)

---

## Environment variables reference

| Variable      | Example                          | Notes                          |
|---------------|----------------------------------|--------------------------------|
| `DB_HOST`     | `mysql-xxx.aivencloud.com`       | Aiven host                     |
| `DB_PORT`     | `12345`                          | Aiven port (not 3306)          |
| `DB_USER`     | `avnadmin`                       | Aiven user                     |
| `DB_PASSWORD` | `***`                            | Aiven password                 |
| `DB_NAME`     | `defaultdb`                      | Aiven database name            |
| `DB_CA_CERT`  | `-----BEGIN CERTIFICATE-----...` | Aiven CA cert (full PEM)       |
