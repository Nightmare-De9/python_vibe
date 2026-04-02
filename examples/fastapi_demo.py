"""
fastapi_demo.py — middleware for pretty request logging
needs: pip install fastapi uvicorn python_vibe
run with: uvicorn fastapi_demo:app --reload
"""

import python_vibe
python_vibe.set_theme("midnight")
python_vibe.enable()

import time
import logging

log = logging.getLogger("fastapi_demo")

try:
    from fastapi import FastAPI, Request
    from fastapi.responses import JSONResponse
except ImportError:
    python_vibe.error("needs fastapi: pip install fastapi uvicorn")
    raise SystemExit(1)


app = FastAPI(title="python_vibe demo api", version="0.1.0")


@app.middleware("http")
async def vibe_middleware(request: Request, call_next):
    """log every request with style"""
    start = time.perf_counter()
    response = await call_next(request)
    elapsed = (time.perf_counter() - start) * 1000

    status = response.status_code
    method = request.method
    path = request.url.path

    if status < 300:
        log.info(f"{method} {path} → {status} ({elapsed:.1f}ms)")
    elif status < 400:
        log.warning(f"{method} {path} → {status} ({elapsed:.1f}ms) [redirect]")
    else:
        log.error(f"{method} {path} → {status} ({elapsed:.1f}ms) [error]")

    return response


# sample endpoints

@app.get("/")
async def root():
    return {"message": "python_vibe + fastapi. looking good.", "chai": "☕"}


@app.get("/users")
async def get_users():
    users = [
        {"id": 1, "name": "rahul", "city": "bhopal", "active": True},
        {"id": 2, "name": "priya", "city": "indore", "active": True},
        {"id": 3, "name": "karan", "city": "pune", "active": False},
    ]
    return {"users": users, "total": len(users)}


@app.get("/users/{user_id}")
async def get_user(user_id: int):
    if user_id > 3:
        return JSONResponse(status_code=404, content={"error": "user not found bhai"})
    return {"id": user_id, "name": "rahul", "city": "bhopal"}


@app.post("/vibe")
async def set_vibe(theme: str = "cyber"):
    try:
        python_vibe.set_theme(theme)
        return {"ok": True, "theme": theme, "msg": f"vibing with {theme} now"}
    except ValueError as e:
        return JSONResponse(status_code=400, content={"error": str(e)})


python_vibe.log("fastapi app ready. run with: uvicorn fastapi_demo:app --reload")


