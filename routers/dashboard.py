from fastapi import APIRouter

router = APIRouter(
    prefix="/dashboard",
    tags=["dashboard"],
    responses={404: {"description": "Not found"}},
)


@router.get("/")
async def base_dashboard():
    return {"message": "Dashboard Home"}

@router.get("/users")
async def dashboard_users():
    return {"message": "Dashboard Users"}
