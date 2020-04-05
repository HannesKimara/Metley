from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from rest_framework.permissions import (
    IsAuthenticated, IsAuthenticatedOrReadOnly
)

from authapi.models import User
from ..models import Examination as Exam, Clinic, Symptom
from ..serializers import ExaminationSerializer, ExamViewSerializer

class ExamView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        all_exams = Exam.objects.filter(user=request.user).all()
        serializer = ExamViewSerializer(all_exams, many=True)
        return Response(
            {
                "total": len(all_exams),
                "results": serializer.data
            }
        )

    def post(self, request):
        serializer = ExaminationSerializer(data=request.data)

        if serializer.is_valid():
            exam_clinic = Clinic.objects.filter(public_id=serializer.data['clinic_id']).first()
            exam_doctor = User.objects.filter(public_id=serializer.data['doctor_id']).first()
            
            if all([exam_clinic, exam_doctor]):
                new_exam = Exam(
                    status="OG",
                    patient_note=serializer.data['patient_note'],
                    user=request.user,
                    doctor=exam_doctor,
                    clinic=exam_clinic
                )
                new_exam.save_exam()
                exam_symptoms = Symptom.create_symptoms(serializer.data['symptoms'], key="symptom")
                new_exam.symptoms.set(exam_symptoms)
                new_exam.save()

                return Response(
                    {
                        "success": True,
                        "data": serializer.data
                    }
                )
            else:
                return Response(
                    {
                        "error": True,
                        "message": "Clinic and Doctor selected non-existent"
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )