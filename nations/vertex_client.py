# nations/vertex_client.py
# Centralizes Vertex AI client initialization and configuration for the nations app.

import json
import os
from google.cloud import aiplatform
from google.oauth2 import service_account
from decouple import config

print("Initializing Vertex AI Client Module...")

# --- Vertex AI Configuration ---
# Load necessary IDs and settings from environment variables.
GCP_PROJECT_ID = config('GCP_PROJECT_ID', default=None)
GCP_REGION = config('GCP_REGION', default='europe-west3') # Adjust if your region differs

# Nation Data Index Endpoint details
VERTEX_INDEX_ENDPOINT_ID = config('VERTEX_INDEX_ENDPOINT_ID', default=None) # Ensure this is set in your .env or Heroku config
VERTEX_DEPLOYED_INDEX_ID = config('VERTEX_DEPLOYED_INDEX_ID', default=None) # Ensure this is set

# Modding Guideline Index Endpoint details
GUIDELINE_VERTEX_INDEX_ENDPOINT_ID = config('GUIDELINE_VERTEX_INDEX_ENDPOINT_ID', default=None) # Ensure this is set
GUIDELINE_VERTEX_DEPLOYED_INDEX_ID = config('GUIDELINE_VERTEX_DEPLOYED_INDEX_ID', default=None) # Ensure this is set


# --- Google Cloud Credentials ---
# Attempt to load service account credentials if provided via environment variable.
GCP_SERVICE_ACCOUNT_JSON_STR = config('GCP_SERVICE_ACCOUNT_KEY_JSON', default=None)
credentials = None
if GCP_SERVICE_ACCOUNT_JSON_STR:
    try:
        key_info = json.loads(GCP_SERVICE_ACCOUNT_JSON_STR)
        credentials = service_account.Credentials.from_service_account_info(key_info)
        print("Vertex Client: Loaded Service Account credentials.")
    except json.JSONDecodeError:
        print("ERROR: Vertex Client: GCP_SERVICE_ACCOUNT_KEY_JSON is invalid JSON.")
    except Exception as cred_err:
        print(f"ERROR: Vertex Client: Loading credentials failed: {cred_err}")
elif not os.environ.get('HEROKU_APP_ID'): # Don't warn if on Heroku (might use default creds)
     print("WARN: Vertex Client: GCP_SERVICE_ACCOUNT_KEY_JSON not found. Trying default application credentials.")


# --- Initialize Vertex AI Client Library ---
# Connects to the Google Cloud project.
try:
    if not GCP_PROJECT_ID:
         print("WARN: Vertex Client: GCP_PROJECT_ID not set. Vertex AI features disabled.")
    else:
        print("Vertex Client: Initializing aiplatform library...")
        aiplatform.init(
            project=GCP_PROJECT_ID,
            location=GCP_REGION,
            credentials=credentials # Uses loaded creds or falls back to default
        )
        print(f"Vertex Client: aiplatform initialized for project {GCP_PROJECT_ID} in {GCP_REGION}.")
except ImportError:
    print("ERROR: Vertex Client: google-cloud-aiplatform library not found. Run pip install google-cloud-aiplatform")
    # Set endpoints to None so checks elsewhere fail gracefully
    vertex_ai_endpoint_nation = None
    guideline_vertex_ai_endpoint = None
except Exception as init_err:
    print(f"ERROR: Vertex Client: initializing aiplatform library: {init_err}")
    vertex_ai_endpoint_nation = None
    guideline_vertex_ai_endpoint = None


# --- Create Matching Engine Endpoint References ---
# These objects are used to query the specific deployed indexes.
vertex_ai_endpoint_nation = None
guideline_vertex_ai_endpoint = None

# Nation Data Index
if GCP_PROJECT_ID: # Only proceed if initialization was attempted
    try:
        if not all([VERTEX_INDEX_ENDPOINT_ID, VERTEX_DEPLOYED_INDEX_ID]):
            print("WARN: Vertex Client: Missing VERTEX_INDEX_ENDPOINT_ID or VERTEX_DEPLOYED_INDEX_ID. Nation RAG disabled.")
        else:
            print(f"Vertex Client: Creating NATION index endpoint reference: {VERTEX_INDEX_ENDPOINT_ID}")
            vertex_ai_endpoint_nation = aiplatform.MatchingEngineIndexEndpoint(
                index_endpoint_name=VERTEX_INDEX_ENDPOINT_ID
            )
            print(f"Vertex Client: NATION endpoint reference created.")
    except NameError: # Handles case where aiplatform failed to import/init
         print("ERROR: Vertex Client: Cannot create NATION endpoint reference - aiplatform library issue.")
    except Exception as e:
        print(f"ERROR: Vertex Client: initializing NATION endpoint ({VERTEX_INDEX_ENDPOINT_ID}): {e}")
        vertex_ai_endpoint_nation = None # Ensure it's None on error

# Modding Guideline Index
if GCP_PROJECT_ID: # Only proceed if initialization was attempted
    try:
        if not all([GUIDELINE_VERTEX_INDEX_ENDPOINT_ID, GUIDELINE_VERTEX_DEPLOYED_INDEX_ID]):
            print("WARN: Vertex Client: Missing GUIDELINE_VERTEX_INDEX_ENDPOINT_ID or GUIDELINE_VERTEX_DEPLOYED_INDEX_ID. Guideline RAG disabled.")
        else:
            print(f"Vertex Client: Creating GUIDELINE index endpoint reference: {GUIDELINE_VERTEX_INDEX_ENDPOINT_ID}")
            guideline_vertex_ai_endpoint = aiplatform.MatchingEngineIndexEndpoint(
                index_endpoint_name=GUIDELINE_VERTEX_INDEX_ENDPOINT_ID
            )
            print(f"Vertex Client: GUIDELINE endpoint reference created.")
    except NameError: # Handles case where aiplatform failed to import/init
         print("ERROR: Vertex Client: Cannot create GUIDELINE endpoint reference - aiplatform library issue.")
    except Exception as e:
        print(f"ERROR: Vertex Client: initializing GUIDELINE endpoint ({GUIDELINE_VERTEX_INDEX_ENDPOINT_ID}): {e}")
        guideline_vertex_ai_endpoint = None # Ensure it's None on error

print("Vertex AI Client Module Initialization Complete.")
