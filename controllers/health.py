from fastapi import APIRouter

router = APIRouter(
    prefix="",
    tags=["health"],
)

@router.get("/")
def root() -> dict[str, str]:
    return {"message": "Hello world!"}

@router.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}

@router.get("/healthz")
def healthz() -> dict[str, str]:
    return {"status": "ok"}
