from django.urls import path
from .views import (
    CareerApplicationCreate,
    JobListAPIView,
    ContactMessageCreate,
    MOUListAPIView,
    GalleryImageListAPIView,
    ProjectListAPIView,
    CommunityItemListAPIView,
    cpu_inquiry_create,
    cpu_inquiry_admin,
    HackathonRegistrationCreate,
)

urlpatterns = [

    # ===== CAREER =====
    path("jobs/", JobListAPIView.as_view()),
    path("apply/", CareerApplicationCreate.as_view()),
    path("apply/<int:pk>/", CareerApplicationCreate.as_view()),

    # ===== CONTACT =====
    path("contact/", ContactMessageCreate.as_view()),
    path("contact/<int:pk>/", ContactMessageCreate.as_view()),

    # ===== CPU INQUIRY =====
    path("inquiry/", cpu_inquiry_create),              # 🌍 PUBLIC (POST only)
    path("inquiry/admin/", cpu_inquiry_admin),         # 🔒 ADMIN (GET)
    path("inquiry/admin/<int:pk>/", cpu_inquiry_admin),# 🔒 ADMIN (DELETE)

    # ===== HACKATHON =====
    path("hackathon/", HackathonRegistrationCreate.as_view()),
    path("hackathon/<int:pk>/", HackathonRegistrationCreate.as_view()),

    # ===== PUBLIC READ =====
    path("mous/", MOUListAPIView.as_view(), name="mous"),
    path("gallery/", GalleryImageListAPIView.as_view()),
    path("projects/", ProjectListAPIView.as_view()),
    path("giveback/", CommunityItemListAPIView.as_view()),
]
