from fastapi import FastAPI
from controllers import auth, health, users

app = FastAPI(title="Forms Anyware API")

# Include routers
app.include_router(auth)
app.include_router(health)
app.include_router(users)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000)