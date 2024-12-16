
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse, RedirectResponse
from urllib.parse import unquote
from main import decrease_url, expand_url, login, users

app = FastAPI()

@app.get("/decrease_url/{user_id}")
async def decr_get(user_id: int, long_url: str):
    long_url = unquote(long_url)
    if login(user_id):
        result = decrease_url(user_id, long_url)
        if result:
            return JSONResponse(content={"response": 201, "short_url": result}, status_code=201)
        else:
            raise HTTPException(status_code=400, detail="Failed to shorten URL")
    else:
        raise HTTPException(status_code=401, detail="Unauthorized")

@app.post("/decrease_url/{user_id}")
async def decr_post(user_id: int, request: Request):
    data = await request.json()
    long_url = data.get("long_url")
    if not long_url:
        raise HTTPException(status_code=400, detail="Missing long_url in request")
    if login(user_id):
        result = decrease_url(user_id, long_url)
        if result:
            return JSONResponse(content={"response": 201, "short_url": result}, status_code=201)
        else:
            raise HTTPException(status_code=400, detail="Failed to shorten URL")
    else:
        raise HTTPException(status_code=401, detail="Unauthorized")

@app.get("/expand_url/{user_id}")
async def expn(user_id: int, short_url: str):
    if login(user_id):
        result = expand_url(user_id, short_url)
        if result:
            return RedirectResponse(url=result, status_code=302)
        else:
            raise HTTPException(status_code=400, detail="Missing long_url")
    else:
        raise HTTPException(status_code=404, detail="URL not found")

@app.get("/users")
async def get_all_users():
    return users
