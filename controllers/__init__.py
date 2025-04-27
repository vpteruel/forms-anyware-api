from routers.auth import router as auth_router
from routers.health import router as health_router
from routers.users import router as users_router

# Expose routers directly
auth = auth_router
health = health_router
users = users_router

# If you want to use the dictionary approach later
router_modules = {
    "auth": auth_router,
    "health": health_router,
    "users": users_router,
}