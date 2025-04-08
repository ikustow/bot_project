import firebase_admin
from firebase_admin import credentials, firestore, storage, auth
import os

from .config import FIREBASE_CREDENTIALS

cred = credentials.Certificate(FIREBASE_CREDENTIALS)
firebase_admin.initialize_app(cred, {
    'storageBucket': 'ai-store-audit.firebasestorage.app'
})

db = firestore.client()
bucket = storage.bucket()

def check_user_exists(user_id: int) -> bool:
    print(f"Checking user existence for ID: {str(user_id)}")
    users = db.collection("users").where("user_id", "==", str(user_id)).limit(1).stream()
    return any(True for _ in users)

def get_user_tasks(user_id: int):
    tasks = db.collection("tasks").where("user_id", "==", str(user_id)).stream()
    return [task.to_dict() | {"id": task.id} for task in tasks]

def get_task_requirements(task_id: str) -> str:
    doc = db.collection("tasks").document(task_id).get()
    return doc.to_dict().get("requirements", "")

def upload_image(file_path: str, filename: str) -> str:
    blob = bucket.blob(f"uploads/{filename}")
    blob.upload_from_filename(file_path)
    blob.make_public()
    return blob.public_url
