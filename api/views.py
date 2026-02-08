from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser, AllowAny
from django.conf import settings
from django.shortcuts import get_object_or_404
from .utils.google_sheets import save_team_to_sheet
from django.utils import timezone
import requests

from .models import (
    CareerApplication,
    ContactMessage,
    MOU,
    GalleryImage,
    Project,
    CommunityItem,
    CpuInquiry,
    HackathonTeam,
    Job,
)
from .serializers import (
    CareerApplicationSerializer,
    ContactMessageSerializer,
    MOUSerializer,
    GalleryImageSerializer,
    ProjectSerializer,
    CommunityItemSerializer,
    CpuInquirySerializer,
    HackathonTeamSerializer,
    HackathonRegistrationSerializer,
    JobSerializer,
)

# ---------------- TELEGRAM ---------------- #

def send_telegram(bot_token, chat_id, text):
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    resp = requests.post(
        url,
        data={"chat_id": chat_id, "text": text},
        timeout=5
    )
    print("TELEGRAM:", resp.status_code, resp.text)


# ================= CAREER ================= #

class JobListAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        today = timezone.now().date()
        jobs = Job.objects.filter(
            is_active=True,
            application_start_date__lte=today,
            application_end_date__gte=today
        )
        serializer = JobSerializer(jobs, many=True)
        return Response(serializer.data)
    
class CareerApplicationCreate(APIView):

    def get_permissions(self):
        if self.request.method == "POST":
            return [AllowAny()]      # 🌍 public submit
        return [IsAdminUser()]      # 🔒 admin only

    def get(self, request):
        qs = CareerApplication.objects.all().order_by("-applied_at")
        serializer = CareerApplicationSerializer(qs, many=True)
        return Response(serializer.data)

    def post(self, request):
        job_id = request.data.get("job")

        if not job_id:
            return Response(
                {"job": "Job selection is required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # 🔒 Validate job existence
        job = get_object_or_404(Job, id=job_id)

        today = timezone.now().date()

        # 🔒 Validate job application window
        if not job.is_active:
            return Response(
                {"job": "This job is no longer active"},
                status=status.HTTP_400_BAD_REQUEST
            )

        if not (job.application_start_date <= today <= job.application_end_date):
            return Response(
                {"job": "Applications for this job are closed"},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = CareerApplicationSerializer(data=request.data)
        if serializer.is_valid():
            obj = serializer.save()

            resume_url = ""
            if obj.resume:
                resume_url = request.build_absolute_uri(
                    settings.MEDIA_URL + obj.resume.name
                )

            send_telegram(
                settings.TELEGRAM_CAREER_BOT_TOKEN,
                settings.TELEGRAM_CAREER_CHAT_ID,
                f"Career Application\n\n"
                f"Job: {obj.job.title}\n"
                f"Name: {obj.full_name}\n"
                f"Email: {obj.email}\n"
                f"Phone: {obj.phone}\n"
                f"College: {obj.college}\n"
                f"CGPA: {obj.cgpa}\n"
                f"Year: {obj.year_of_passing}\n"
                f"Experience: {obj.experience}\n"
                f"Skills: {obj.skills}\n\n"
                f"Resume:\n{resume_url}"
            )

            return Response(
                {"message": "Application submitted successfully"},
                status=status.HTTP_201_CREATED,
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        obj = get_object_or_404(CareerApplication, pk=pk)
        obj.delete()
        return Response(
            {"message": "Deleted"},
            status=status.HTTP_204_NO_CONTENT
        )

# ================= CONTACT ================= #

class ContactMessageCreate(APIView):

    def get_permissions(self):
        if self.request.method == "POST":
            return [AllowAny()]
        return [IsAdminUser()]

    def get(self, request):
        qs = ContactMessage.objects.all().order_by("-created_at")
        serializer = ContactMessageSerializer(qs, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ContactMessageSerializer(data=request.data)
        if serializer.is_valid():
            obj = serializer.save()

            send_telegram(
                settings.TELEGRAM_CONTACT_BOT_TOKEN,
                settings.TELEGRAM_CONTACT_CHAT_ID,
                f"Contact Message\n\n"
                f"Name: {obj.name}\n"
                f"Email: {obj.email}\n"
                f"Phone: {obj.phone}\n"
                f"Subject: {obj.subject}\n"
                f"Message: {obj.message}"
            )

            return Response({"message": "Contact saved"}, status=201)

        return Response(serializer.errors, status=400)

    def delete(self, request, pk):
        obj = get_object_or_404(ContactMessage, pk=pk)
        obj.delete()
        return Response({"message": "Deleted"}, status=204)


# ================= CPU ================= #

@api_view(["POST"])
@permission_classes([AllowAny])
def cpu_inquiry_create(request):
    serializer = CpuInquirySerializer(data=request.data)
    if serializer.is_valid():
        obj = serializer.save()

        send_telegram(
            settings.TELEGRAM_CPU_BOT_TOKEN,
            settings.TELEGRAM_CPU_CHAT_ID,
            f"CPU Inquiry\n\n"
            f"Name: {obj.full_name}\n"
            f"Email: {obj.email}\n"
            f"Phone: {obj.phone}\n"
            f"CPU: {obj.cpu_model}\n"
            f"Quantity: {obj.quantity}\n"
            f"RAM: {obj.ram}\n"
            f"Storage: {obj.storage}\n"
            f"Message: {obj.message}"
        )

        return Response({"message": "Inquiry submitted"}, status=201)

    return Response(serializer.errors, status=400)


@api_view(["GET", "DELETE"])
@permission_classes([IsAdminUser])
def cpu_inquiry_admin(request, pk=None):
    if request.method == "GET":
        qs = CpuInquiry.objects.all().order_by("-created_at")
        serializer = CpuInquirySerializer(qs, many=True)
        return Response(serializer.data)

    if request.method == "DELETE":
        obj = get_object_or_404(CpuInquiry, pk=pk)
        obj.delete()
        return Response({"message": "Deleted"}, status=204)


# ================= PUBLIC READ ================= #

class MOUListAPIView(ListAPIView):
    serializer_class = MOUSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        return MOU.objects.filter(is_active=True)


class GalleryImageListAPIView(ListAPIView):
    serializer_class = GalleryImageSerializer
    permission_classes = [AllowAny]
    queryset = GalleryImage.objects.all().order_by("-created_at")

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["request"] = self.request
        return context


class ProjectListAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        qs = Project.objects.all()
        serializer = ProjectSerializer(qs, many=True)
        return Response(serializer.data)


class CommunityItemListAPIView(ListAPIView):
    serializer_class = CommunityItemSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        return CommunityItem.objects.filter(section="giveback").order_by("-created_at")


# ================= HACKATHON ================= #

class HackathonRegistrationCreate(APIView):

    def get_permissions(self):
        if self.request.method == "POST":
            return [AllowAny()]
        return [IsAdminUser()]

    def get(self, request):
        teams = HackathonTeam.objects.all().order_by("-created_at")
        serializer = HackathonTeamSerializer(teams, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = HackathonRegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # 1️⃣ Save to DB (TEAM + PARTICIPANTS)
        team = serializer.save()

        leader = team.participants.filter(role="LEADER").first()
        members = team.participants.filter(role="MEMBER")

        # 2️⃣ GOOGLE SHEETS (FAIL-SAFE)
        try:
            participants = []
            if leader:
                participants.append(leader)
            participants.extend(list(members))

            save_team_to_sheet(team, participants)

        except Exception as sheet_err:
            # IMPORTANT: never block registration
            print("Google Sheets error:", sheet_err)

        # 3️⃣ TELEGRAM MESSAGE
        members_text = ""
        for i, m in enumerate(members, 1):
            members_text += (
                f"\nMember {i}:\n"
                f"Name: {m.full_name}\n"
                f"Email: {m.email}\n"
                f"Phone: {m.phone}\n"
                f"Branch: {m.branch}\n"
                f"Section: {m.section}\n"
                f"Year: {m.year}\n"
            )

        message = (
            f"Hackathon Registration\n\n"
            f"Team Name: {team.team_name}\n"
            f"Total Participants: {team.total_participants}\n\n"
        )

        if leader:
            message += (
                f"Leader:\n"
                f"Name: {leader.full_name}\n"
                f"Email: {leader.email}\n"
                f"Phone: {leader.phone}\n"
                f"Branch: {leader.branch}\n"
                f"Section: {leader.section}\n"
                f"Year: {leader.year}\n"
            )

        message += members_text

        send_telegram(
            settings.TELEGRAM_HACKATHON_TOKEN,
            settings.TELEGRAM_HACKATHON_ID,
            message
        )

        return Response(
            {
                "message": "Hackathon registration successful",
                "team_id": team.id
            },
            status=status.HTTP_201_CREATED
        )

    def delete(self, request, pk):
        team = get_object_or_404(HackathonTeam, pk=pk)
        team.delete()
        return Response({"message": "Deleted"}, status=204)
