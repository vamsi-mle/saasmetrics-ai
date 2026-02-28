# saasmetrics.ai  |  Complete Setup Guide
# From zero to running — exact commands for your machine
# SDK confirmed: gcloud 541.0.0  |  bq 2.1.24
# ════════════════════════════════════════════════════════════

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
BEFORE YOU START — confirm you have these
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  gcloud --version    ← should show 541.0.0
  python --version    ← need 3.10+
  node --version      ← need 18+  (only for running gen scripts)

  If any are missing: install before proceeding.


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
STEP 1 — GCP Project
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  # Authenticate (opens browser)
  gcloud auth login

  # Create project (ID must be globally unique)
  gcloud projects create saasmetrics-demo-$(date +%s) --name="saasmetrics demo"

  # List your projects to get the exact ID
  gcloud projects list

  # Set as active — replace with your actual project ID
  gcloud config set project YOUR_PROJECT_ID

  # Confirm
  gcloud config get-value project


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
STEP 2 — Enable Billing + APIs
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  # Link billing via console (required for BQ + GCS)
  # Go to: https://console.cloud.google.com/billing
  # Click "Link a billing account" → select account → link to YOUR_PROJECT_ID

  # Enable required APIs
  gcloud services enable \
    bigquery.googleapis.com \
    bigquerystorage.googleapis.com \
    storage.googleapis.com \
    aiplatform.googleapis.com \
    --project=saasmetricsai-demo


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
STEP 3 — BigQuery Dataset + Tables
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  # Create dataset
  bq mk \
    --dataset \
    --location=US \
    --description="saasmetrics.ai demo" \
    YOUR_PROJECT_ID:saasmetricsai-demo

  # Load all tables (run from project root)
  bq query \
    --project_id=saasmetricsai-demo \
    --use_legacy_sql=false \
    < files/bq_setup.sql

  # Verify — should show 5 tables
  CLOUDSDK_PYTHON=python bq ls saasmetricsai-demo:saasmetrics

  # Quick sanity check
  CLOUDSDK_PYTHON=python bq query \
    --project_id=saasmetricsai-demo \
    --use_legacy_sql=false \
    "SELECT name, status, arr_usd FROM \`saasmetricsai-demo.saasmetrics.customers\` ORDER BY arr_usd DESC LIMIT 5"


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
STEP 4 — GCS Bucket (for file uploads)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  # Create bucket (name must be globally unique — use project ID as suffix)
  gcloud storage buckets create \
    gs://saasmetrics-uploads-saasmetricsai-demo \
    --location=US \
    --project=saasmetricsai-demo

  # Verify
  gcloud storage buckets describe gs://saasmetrics-uploads-saasmetricsai-demo

  # Your bucket name = saasmetrics-uploads-YOUR_PROJECT_ID
  # Write this down — goes in .env as GCS_BUCKET = saasmetrics-uploads-saasmetricsai-demo


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
STEP 5 — Service Account
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  # Create service account
  gcloud iam service-accounts create saasmetrics-backend \
    --display-name="saasmetrics Backend SA" \
    --project=YOUR_PROJECT_ID

  # Grant BigQuery permissions
  gcloud projects add-iam-policy-binding YOUR_PROJECT_ID \
    --member="serviceAccount:saasmetrics-backend@YOUR_PROJECT_ID.iam.gserviceaccount.com" \
    --role="roles/bigquery.dataViewer"

  gcloud projects add-iam-policy-binding YOUR_PROJECT_ID \
    --member="serviceAccount:saasmetrics-backend@YOUR_PROJECT_ID.iam.gserviceaccount.com" \
    --role="roles/bigquery.jobUser"

  # Grant GCS permissions (for file uploads)
  gcloud storage buckets add-iam-policy-binding \
    gs://saasmetrics-uploads-YOUR_PROJECT_ID \
    --member="serviceAccount:saasmetrics-backend@YOUR_PROJECT_ID.iam.gserviceaccount.com" \
    --role="roles/storage.objectAdmin"

  # Download key (KEEP SAFE — never commit to git)
  gcloud iam service-accounts keys create \
    service-account-key.json \
    --iam-account=saasmetrics-backend@YOUR_PROJECT_ID.iam.gserviceaccount.com

  # Protect it
  echo "service-account-key.json" >> .gitignore
  echo ".env" >> .gitignore


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
STEP 6 — Gemini API Key
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  Go to: https://aistudio.google.com/app/apikey
  Click: "Create API key in existing project"
  Select: YOUR_PROJECT_ID
  Copy the key.


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
STEP 7 — Configure .env
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  cp .env.template .env

  # Open .env and fill in:
  #   GEMINI_API_KEY=paste_your_key_here
  #   GCP_PROJECT=YOUR_PROJECT_ID
  #   GCS_BUCKET=saasmetrics-uploads-YOUR_PROJECT_ID

  # Set GCP credentials to use service account
  export GOOGLE_APPLICATION_CREDENTIALS="$(pwd)/service-account-key.json"

  # Add to shell profile so it persists across terminal sessions
  echo "export GOOGLE_APPLICATION_CREDENTIALS=\"$(pwd)/service-account-key.json\"" >> ~/.zshrc
  # or ~/.bashrc if using bash


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
STEP 8 — Install Python Dependencies
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  # Create virtual environment (recommended)
  python -m venv venv
  source venv/bin/activate        # Mac/Linux
  # venv\Scripts\activate          # Windows

  pip install -r requirements.txt

  # Verify key packages
  python -c "
  import google.generativeai
  import google.cloud.bigquery
  import google.cloud.storage
  import fastapi, streamlit, sseclient
  print('All dependencies OK')
  "


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
STEP 9 — Generate Mock Upload Files
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  python gen_mock_uploads.py

  # Creates mock_uploads/ with 3 files:
  #   Competitor_WinLoss_Q4FY2024.xlsx
  #   CS_QBR_Notes_Q3FY2024.pdf
  #   FY2025_GTM_Budget_Plan.docx


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
STEP 10 — Run the App
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  # Terminal 1 — load env + start backend
  source .env 2>/dev/null || export $(grep -v '^#' .env | xargs)
  uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload

  # Confirm backend is up (new terminal or second tab)
  curl http://localhost:8000/health
  # Should return: {"status":"ok","gemini":true,"bigquery":true,"gcs":true,...}

  # Terminal 2 — start frontend
  source venv/bin/activate
  streamlit run frontend/app.py

  # Open: http://localhost:8501


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
PRE-DEMO CHECKLIST
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Run through this 30 minutes before the demo:

  [ ] curl http://localhost:8000/health
      → gemini: true, bigquery: true, gcs: true

  [ ] Open http://localhost:8501
      → App loads, green dots in sidebar for Gemini + BigQuery + GCS

  [ ] Ask: "What is our current ARR?"
      → Should return $2.22M with [BigQuery: revenue_monthly] citation

  [ ] Ask: "What is the RIIP promotion?"
      → Should cite [Word: §4.1] and describe regulated industry discount

  [ ] Upload mock_uploads/Competitor_WinLoss_Q4FY2024.xlsx
      → "Indexed and ready" confirmation, appears in sidebar

  [ ] Ask: "Which competitors are we losing to most?"
      → Should cite [Uploaded: Competitor_WinLoss_Q4FY2024.xlsx]

  [ ] Toggle "Show SQL queries" ON
      → Verify SQL appears under BQ answers

  [ ] Toggle "Show routing decisions" ON
      → Verify routing panel appears with source selection logic

  All green? You're ready.


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
TROUBLESHOOTING
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

"Could not determine credentials"
→ export GOOGLE_APPLICATION_CREDENTIALS="$(pwd)/service-account-key.json"

"bigquery: false in /health"
→ Check GCP_PROJECT in .env matches your actual project ID
→ Verify service account has roles/bigquery.dataViewer + roles/bigquery.jobUser

"gcs: false in /health"
→ Check GCS_BUCKET in .env matches the bucket you created
→ Verify service account has roles/storage.objectAdmin on that bucket

"gemini: false in /health"
→ Check GEMINI_API_KEY in .env is not empty
→ Test: python -c "import google.generativeai as g; g.configure(api_key='YOUR_KEY'); print(g.GenerativeModel('gemini-1.5-flash').generate_content('hi').text)"

"Module not found" errors
→ source venv/bin/activate
→ pip install -r requirements.txt

Streamlit shows "Backend not running"
→ Check Terminal 1 — uvicorn must be running on port 8000
→ Check for import errors in uvicorn output

Upload fails with "GCS error"
→ Uploads will fall back to local storage automatically
→ Files go to uploads_store/ and still work for the demo
