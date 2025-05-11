


import os
import json
import firebase_admin
from firebase_admin import credentials, storage
from supabase import create_client, Client

# --- Configuração Firebase ---
#firebase_cred_path = "firebaseSupabase.json"
firebase_bucket_name = "eduardo-d28ce.appspot.com"
firebase_file_path = "Mauro/logsFirebase.txt"

firebase_json = os.getenv("FIREBASE_CREDENTIALS")
cred_dict = json.loads(firebase_json)
cred = credentials.Certificate(cred_dict)

#cred = credentials.Certificate(firebase_cred_path)

if not firebase_admin._apps:
    firebase_admin.initialize_app(cred, {'storageBucket': firebase_bucket_name})

bucket = storage.bucket()
blob = bucket.blob(firebase_file_path)
conteudo = blob.download_as_text()

# --- Parse do conteúdo (exemplo: csv simples) ---
linhas = conteudo.strip().split("\n")

# --- Configuração Supabase ---
url = "https://fmogfljxpdqrjgbskwrp.supabase.co"
chave = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImZtb2dmbGp4cGRxcmpnYnNrd3JwIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDU2NzI1NTAsImV4cCI6MjA2MTI0ODU1MH0.M8JKRz1TYzbq5U22R_riCWDykYWtHjkYHVsm4LW5UJc"
supabase: Client = create_client(url, chave)

# --- Atualização por campo identificador (ex: 'id' ou 'placa') ---
for linha in linhas:
    try:
        campos = linha.strip().split(",")

        if len(campos) < 3:
            print(f"Linha incompleta: {linha}")
            continue

        data_hora = campos[0]
        com_produto = campos[1]
        sem_produto = campos[2]

        # Verifica se já existe uma linha com a mesma data_hora
        existe = supabase.table("Placas").select("data_hora").eq("data_hora", data_hora).execute()

        if not existe.data:  # Se lista estiver vazia, não existe ainda
            supabase.table("Placas").insert({
                "data_hora": data_hora,
                "placa_com_produto_v": com_produto,
                "placa_sem_produto_v": sem_produto
            }).execute()
        else:
            print(f"Registro já existe para data_hora: {data_hora}")

        #supabase.table("Placas").upsert({
        #    "data_hora": data_hora,
        #    "placa_com_produto_v": com_produto,
        #    "placa_sem_produto_v": sem_produto
        #}, on_conflict="data_hora").execute()
    except Exception as e:
        print(f"Erro ao inserir linha: {linha}\n{e}")

