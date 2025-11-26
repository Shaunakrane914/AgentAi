from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from backend.main import app as backend_app
from dotenv import load_dotenv
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/api", backend_app)

# Custom static files handler with no-cache headers
from fastapi import Request
from starlette.staticfiles import StaticFiles
from starlette.responses import Response, RedirectResponse

class NoCacheStaticFiles(StaticFiles):
    async def get_response(self, path: str, scope) -> Response:
        response = await super().get_response(path, scope)
        response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
        response.headers["Pragma"] = "no-cache"
        return response

app.mount("/static", NoCacheStaticFiles(directory="frontend"), name="static")

@app.get("/")
def index():
    response = FileResponse("frontend/index.html")
    response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
    response.headers["Pragma"] = "no-cache"
    return response

@app.get("/dashboard")
def dashboard_page():
    response = FileResponse("frontend/dashboard.html")
    response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
    response.headers["Pragma"] = "no-cache"
    return response

@app.get("/about")
def about_page():
    response = FileResponse("frontend/about.html")
    response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
    response.headers["Pragma"] = "no-cache"
    return response

@app.get("/submit")
def submit_page():
    response = FileResponse("frontend/submit.html")
    response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
    response.headers["Pragma"] = "no-cache"
    return response

# Convenience proxy: allow POST /claims/submit at root to hit mounted backend at /api/claims/submit
@app.post("/claims/submit")
async def proxy_claims_submit():
    # 307 preserves method and body for POST
    return RedirectResponse(url="/api/claims/submit", status_code=307)

# Evidence is generated lazily via backend API mounted at /api.

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
