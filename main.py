import datetime
import json

from fastapi import FastAPI, File, UploadFile
from supabase import create_client, Client
import re
import email
from bs4 import BeautifulSoup

app = FastAPI()

url: str = "https://hrtaeapwsrqccwefrhxl.supabase.co"
key: str = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImhydGFlYXB3c3JxY2N3ZWZyaHhsIiwicm9sZSI6ImFub24iLCJpYXQiOjE2Nzc4NDcyMDEsImV4cCI6MTk5MzQyMzIwMX0.2bETs7c0DhuqWGsBvW8OB89BcT8KJ7mezc_QguPp5iw"
supabase: Client = create_client(url, key)


class DatetimeEncoder(json.JSONEncoder):
    def default(self, obj):
        try:
            return super().default(obj)
        except TypeError:
            return str(obj)


@app.get("/")
async def root():
    return {"message": "Hello Synth"}


@app.post("/savepage")
async def putData(file: UploadFile = File()):
    raw_string = file.file.read().decode()
    with open("temp.txt", "w") as f:
        f.write(raw_string)
    with open("temp.txt", "r") as fp:
        message = email.message_from_file(fp)
        for part in message.walk():
            if part.get_content_type() == "text/html":
                soup = BeautifulSoup(part.get_payload(decode=False), 'lxml')
                page = soup.find_all(text=True)
    page1 = [s.replace(r"=", '') for s in page]
    my_array = [re.sub(r'[^,"()\'A-Za-z0-9:. _-]+', '', s) for s in page1]
    my_array = [s.strip() for s in my_array if s]
    data, count = supabase.table('pageContent').insert(
        {"user_id": 1, "page-content": my_array, "created_at": json.dumps(datetime.datetime.now(), cls=DatetimeEncoder)
            , "tab_id": "1"}).execute()
    return {"file_size": "len(file)"}


@app.get("/search")
async def search(query: str):
    query = query.strip()
    data, count = supabase.rpc('searchtext', {'my_substring': query}).execute()
    results = data[1][:5]
    kid = 1
    response = []
    for resp in results:
        response.append({'id': kid, 'match': resp.get('matched_element')})
        kid += 1
    return response
