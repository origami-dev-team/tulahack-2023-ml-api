import firebase_admin
from fastapi import HTTPException, UploadFile
from firebase_admin import firestore_async
from firebase_admin import storage
from google.cloud.firestore_v1.async_document import AsyncDocumentReference
from google.cloud.firestore_v1.async_collection import AsyncCollectionReference
from typing import List
from utils.types import DICT
from constants import BUCKET_NAME
from utils import parse_filename

# Main rules of this Firestore wrapper:
#   * This one receives ONLY dicts
#   * This one returns ONLY dicts

class Firestore:
    def __new__(cls):
        if not hasattr(cls, "instance"):
            cred = firebase_admin.credentials.Certificate("secrets/firebase.json")
            app = firebase_admin.initialize_app(cred, {
                "storageBucket": f"gs://{BUCKET_NAME}"
            })
            cls.firestore = firestore_async.client()  # type: ignore
            cls.bucket = storage.bucket(app=app, name=BUCKET_NAME)
            cls.instance = super(Firestore, cls).__new__(cls)
        return cls.instance

    async def create(self, collection: str, data: DICT, unique: bool = False) -> DICT:
        ref = self.__get_doc_ref(data["id"], collection)
        if unique:
            doc = await ref.get()
            if doc.exists:
                raise HTTPException(status_code=400, detail=f"{collection} already exists!")
        await ref.set(data)
        return await self.__get_doc_safely(ref)

    async def get_one(self, id: str, collection: str) -> DICT:
        ref = self.__get_doc_ref(id, collection)
        return await self.__get_doc_safely(ref)

    async def get_all(self, collection: str) -> List[DICT]:
        docs = self.__get_collection_ref(collection).stream()  # type: ignore
        docs_dicts = []
        async for doc in docs:
            dict = doc.to_dict()
            docs_dicts.append(dict)
        return docs_dicts

    async def update(self, id: str, collection: str, data: DICT) -> DICT:
        ref = self.__get_doc_ref(id, collection)
        await self.__get_doc_safely(ref)
        await ref.update(data)
        return await self.__get_doc_safely(ref)

    async def delete_one(self, id: str, collection: str) -> DICT:
        ref = self.__get_doc_ref(id, collection)
        doc = await self.__get_doc_safely(ref)
        await ref.delete()
        return doc

    async def delete_all(self, collection: str, batch_size: int = 5):
        docs = self.__get_collection_ref(collection).limit(batch_size).stream()
        deleted = []

        async for doc in docs:  # type: ignore
            await doc.reference.delete()
            deleted.append(doc.to_dict())

        if len(deleted) >= batch_size:
            return self.delete_all(collection, batch_size)
        return deleted
        
    async def upload_file(self, file: UploadFile, folder: str, id: str, from_string: bool = False) -> str:
        name, ext = parse_filename(str(file.filename))
        blob  = firestore.bucket.blob(f"{folder}/{name}-{id}.{ext}")
        if from_string:
            blob.upload_from_string(file.file)
        else:
            blob.upload_from_file(file.file)
        return blob.public_url

    async def __get_doc_safely(self, ref: AsyncDocumentReference) -> DICT:
        doc = await ref.get()
        if not doc.exists:
            raise HTTPException(status_code=404, detail=f"Item doesn't exists")
        return doc.to_dict()  # type: ignore

    def __get_doc_ref(self, id: str, collection: str) -> AsyncDocumentReference:
        ref = self.__get_collection_ref(collection).document(id)
        return ref

    def __get_collection_ref(self, collection: str) -> AsyncCollectionReference:
        ref = self.firestore.collection(collection)
        return ref


firestore = Firestore()
