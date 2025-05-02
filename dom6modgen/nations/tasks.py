# nations/tasks.py
from celery import shared_task
from .models import Nation, NationGenerationStatus
import google.generativeai as genai
from google.cloud import aiplatform
from decouple import config
import time

from .views import (
    vertex_ai_endpoint_nation,
    guideline_vertex_ai_endpoint,
    VERTEX_DEPLOYED_INDEX_ID,
    GUIDELINE_VERTEX_DEPLOYED_INDEX_ID,
    GCP_PROJECT_ID, # Needed if re-initializing clients here
    GCP_REGION      # Needed if re-initializing clients here
)



@shared_task(bind=True) # bind=True gives access to self
def generate_nation_dm_task(self, nation_id):
    """
    Celery task to generate Dominions 6 mod code for a Nation asynchronously.
    """
    task_id = self.request.id
    print(f"Starting task {task_id} for Nation ID: {nation_id}")
    nation = None
    try:
        nation = Nation.objects.get(pk=nation_id)
        nation.generation_status = NationGenerationStatus.GENERATING
        nation.generation_task_id = task_id
        nation.generated_dm_code = None # Clear previous results
        nation.generation_error = None
        nation.save(update_fields=['generation_status', 'generation_task_id', 'generated_dm_code', 'generation_error'])
    except Nation.DoesNotExist:
        print(f"Error: Nation with ID {nation_id} not found.")
        # Cannot update status if nation doesn't exist, task fails here.
        return # Or raise an exception

    generated_code = "# Generation failed or prerequisites missing."
    error_message = None
    prompt_used = ""
    nation_context_str = "Nation RAG system inactive or failed."
    guideline_context_str = "Guideline RAG system inactive or failed."

    try:
        # --- RAG Retrieval Logic (Copied & Adapted from view) ---
        rag_context_for_prompt = ""
        query_embedding = None
        can_query_nation = bool(vertex_ai_endpoint_nation)
        can_query_guideline = bool(guideline_vertex_ai_endpoint)

        if can_query_nation or can_query_guideline:
            try:
                print(f"[Task {task_id}] Generating query embedding...")
                query_text = f"{nation.name} {nation.description}"
                query_embedding_response = genai.embed_content(
                    model="models/embedding-001", # Or text-embedding-004 etc.
                    content=query_text,
                    task_type="RETRIEVAL_QUERY"
                )
                query_embedding = query_embedding_response['embedding']
                print(f"[Task {task_id}] Query embedding generated.")
            except Exception as embed_e:
                print(f"[Task {task_id}] Error generating query embedding: {embed_e}")
                error_message = f"Failed to generate query embedding: {embed_e}"
                can_query_nation = False
                can_query_guideline = False
                query_embedding = None

        # Query Nation Index
        if can_query_nation and query_embedding:
            try:
                print(f"[Task {task_id}] Querying NATION Index...")
                NUM_NEIGHBORS = 5
                nation_response = vertex_ai_endpoint_nation.find_neighbors(
                    queries=[query_embedding],
                    deployed_index_id=VERTEX_DEPLOYED_INDEX_ID,
                    num_neighbors=NUM_NEIGHBORS
                )
                retrieved_docs_info_nation = []
                if nation_response and nation_response[0]:
                    print(f"[Task {task_id}] Received {len(nation_response[0])} neighbors from NATION Index.")
                    for neighbor in nation_response[0]:
                        retrieved_docs_info_nation.append(f"Nation ID: {neighbor.id} (Dist: {neighbor.distance:.4f})")
                    nation_context_str = "\n".join(retrieved_docs_info_nation)
                else:
                     nation_context_str = "No relevant neighbors found in NATION Index."
            except Exception as nation_rag_e:
                print(f"[Task {task_id}] Error during NATION Index RAG retrieval: {nation_rag_e}")
                nation_context_str = f"Error during NATION Index retrieval: {nation_rag_e}"
                if not error_message: error_message = "Failed to retrieve context from Nation Index."
        elif not can_query_nation:
             nation_context_str = "NATION Index endpoint not initialized or embedding failed."

        # Query Guideline Index
        if can_query_guideline and query_embedding:
            try:
                print(f"[Task {task_id}] Querying GUIDELINE Index...")
                NUM_NEIGHBORS_GUIDELINE = 3
                guideline_response = guideline_vertex_ai_endpoint.find_neighbors(
                    queries=[query_embedding],
                    deployed_index_id=GUIDELINE_VERTEX_DEPLOYED_INDEX_ID,
                    num_neighbors=NUM_NEIGHBORS_GUIDELINE
                )
                retrieved_docs_info_guideline = []
                if guideline_response and guideline_response[0]:
                    print(f"[Task {task_id}] Received {len(guideline_response[0])} neighbors from GUIDELINE Index.")
                    for neighbor in guideline_response[0]:
                        retrieved_docs_info_guideline.append(f"Guideline ID: {neighbor.id} (Dist: {neighbor.distance:.4f})")
                    guideline_context_str = "\n".join(retrieved_docs_info_guideline)
                else:
                     guideline_context_str = "No relevant neighbors found in GUIDELINE Index."
            except Exception as guideline_rag_e:
                print(f"[Task {task_id}] Error during GUIDELINE Index RAG retrieval: {guideline_rag_e}")
                guideline_context_str = f"Error during GUIDELINE Index retrieval: {guideline_rag_e}"
                if not error_message: error_message = "Failed to retrieve context from Guideline Index."
        elif not can_query_guideline:
             guideline_context_str = "GUIDELINE Index endpoint not initialized or embedding failed."

        # Combine Contexts
        rag_context_for_prompt = f"Retrieved Relevant Context (Context lookup pending):\n\n--- Nation Data Context ---\n{nation_context_str}\n\n--- Modding Guideline Context ---\n{guideline_context_str}\n\n"
        # --- End RAG Retrieval ---

        # --- Gemini Generation Logic (Copied & Adapted from view) ---
        loaded_api_key = config('GEMINI_API_KEY', default=None)
        if not loaded_api_key:
            raise ValueError("Gemini API Key not found in environment variables.")

        # Use the desired model here (e.g., 1.5 Pro)
        generation_model = genai.GenerativeModel('gemini-2.5-flash-preview-04-17') 

        prompt = f"""You are an expert Dominions 6 modder creating a new nation mod file (.dm format)."""