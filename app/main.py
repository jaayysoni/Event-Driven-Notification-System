from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from app.routes import welcome

app = FastAPI(title="Event-Driven Notification System")

# Include routes
app.include_router(welcome.router)

@app.get("/", response_class=HTMLResponse)
async def root():
    return "<h1>Notification System Running 🚀</h1>"
