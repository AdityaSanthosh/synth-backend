from fastapi import FastAPI, File, UploadFile
from supabase import create_client, Client
from pydantic import BaseModel
import email
from bs4 import BeautifulSoup

app = FastAPI()

url: str = "https://hrtaeapwsrqccwefrhxl.supabase.co"
key: str = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImhydGFlYXB3c3JxY2N3ZWZyaHhsIiwicm9sZSI6ImFub24iLCJpYXQiOjE2Nzc4NDcyMDEsImV4cCI6MTk5MzQyMzIwMX0.2bETs7c0DhuqWGsBvW8OB89BcT8KJ7mezc_QguPp5iw"
supabase: Client = create_client(url, key)


@app.get("/")
async def root():
    return {"message": "Hello Synth"}


@app.post("/savepage")
async def putData(file: UploadFile = File()):
    raw_string = file.file.read().decode()
    with open("temp.txt","w") as f:
        f.write(raw_string)
    with open("temp.txt","r") as fp:
        message = email.message_from_file(fp)
        for part in message.walk():
            if part.get_content_type() == "text/html":
                with open("page.html","w") as f:
                    f.write(part.get_payload(decode=False))
    with open("page.html") as fp:
        soup = BeautifulSoup(fp, 'lxml')
    p_content = soup.find_all('p')
    print(p_content[20].text)
    # remove unnecessary symbols from text
    return {"file_size": "len(file)"}


@app.get("/search")
async def search(query: str):
    return {"message": f"Hello {query}"}
