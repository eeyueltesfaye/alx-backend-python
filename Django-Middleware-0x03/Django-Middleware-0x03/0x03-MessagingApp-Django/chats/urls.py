<<<<<<< HEAD
from django.urls import path, include
from rest_framework import routers
from rest_framework_nested import routers as nested_routers
from .views import ConversationViewSet, MessageViewSet
=======
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import ConversationViewSet, MessageViewSet, BookListCreateAPIView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

>>>>>>> 9495c56 (Update messaging_app with filters and views)

router = routers.DefaultRouter()
router.register(r'conversations', ConversationViewSet, basename='conversation')

# Create nested router for messages inside conversations
conversations_router = nested_routers.NestedDefaultRouter(router, r'conversations', lookup='conversation')
conversations_router.register(r'messages', MessageViewSet, basename='conversation-messages')

urlpatterns = [
<<<<<<< HEAD
    path('', include(router.urls)),
    path('', include(conversations_router.urls)),
=======
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  # for login
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # to refresh token
    path('', include('messaging_app.urls')),  # include your app urls here
>>>>>>> 9495c56 (Update messaging_app with filters and views)
]
