from django.urls import include, path
from rest_framework import routers
from rest_framework_nested.routers import NestedDefaultRouter

from .views import ConversationViewSet, MessageViewSet

router = routers.DefaultRouter()
router.register(r'conversations', ConversationViewSet, basename='conversations')

nested_router = NestedDefaultRouter(router, r'conversations', lookup='conversation')
nested_router.register(r'messages', MessageViewSet, basename='messages')


urlpatterns = [
    path('', include(router.urls)),
    path('', include(nested_router.urls)),
]
