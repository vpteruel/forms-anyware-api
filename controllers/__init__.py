from controllers.auth import router as auth_router
from controllers.health import router as health_router
from controllers.users import router as users_router

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
