from fastapi import FastAPI
from supabase import create_client, Client
from pydantic import BaseModel

app = FastAPI()

url: str = "https://hrtaeapwsrqccwefrhxl.supabase.co"
key: str = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImhydGFlYXB3c3JxY2N3ZWZyaHhsIiwicm9sZSI6ImFub24iLCJpYXQiOjE2Nzc4NDcyMDEsImV4cCI6MTk5MzQyMzIwMX0.2bETs7c0DhuqWGsBvW8OB89BcT8KJ7mezc_QguPp5iw"
supabase: Client = create_client(url, key)


# class PageData(BaseModel):
#     user_id: str
#     webpage: str
#     page_content:

@app.get("/")
async def root():
    return {"message": "Hello Synth"}


# @app.post("/insert")
# async def putData()


@app.get("/search")
async def search(query: str):
    return {"message": f"Hello {query}"}
