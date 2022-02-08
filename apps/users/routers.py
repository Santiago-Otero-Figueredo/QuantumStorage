
from rest_framework.routers import SimpleRouter
from apps.users.viewsets import UserViewSet

routes = SimpleRouter()

# USER
routes.register(r'user', UserViewSet, basename='user')


urlpatterns = [
    *routes.urls
]
