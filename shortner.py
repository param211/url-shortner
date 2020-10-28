import uuid
import redis
from fastapi import FastAPI
from pydantic import BaseModel
from starlette.responses import RedirectResponse

# Start app and server
app = FastAPI()
# r = redis.Redis()
r = redis.from_url(os.environ.get("REDIS_URL"))


# Class to store url-name pair
class Item(BaseModel):
    url: str
    custom_target:str = None


# Test the root
@app.get("/")
def read_root():
    return {"message": "Yo Yo Param Singh!"}


# Redirect
@app.get("/{short}")
def redirect_url(short: str):
    for key in r.keys():
        if r.get(key).decode("utf8") == short:
            return {"url": key.decode("utf8")}
            # return RedirectResponse(url=key.decode("utf8"))

    return {"message": "URL does not exist"}


# Define POST
@app.post("/")
def shorten_url(item: Item):

    url = item.url

    if r.get(url) is None:
        new_name = item.custom_target or str(uuid.uuid4())[-6:]
        if r.mset({url: new_name}):
            return {"url": url, "short": r.get(url)}
        else:
            return {"message": "failed"}

    return {"message": "URL already exists", "short": r.get(url)}
