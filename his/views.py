from django.shortcuts import render
from .models import Doctor, Appointment, Patient, Department
import matplotlib
import base64
from io import BytesIO
import os
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
matplotlib.use('Agg') 

def home(request):
    return render(request, 'his/index.html')

def about(request):
    patients = Patient.objects.prefetch_related('appointment_set__doctor')
    return render(request, 'his/about.html', {'patients': patients})

def doctor(request):
    query = request.GET.get('id', None)  # 검색할 Patient ID
    png_result = None

    if query:
        png_file = os.path.join(DICOM_DIR, f"{query}.png")  # PNG 파일 경로 생성

        if os.path.exists(png_file):
            try:
                # PNG 파일 렌더링
                buffer = render_png_as_dicom_style(png_file)
                if buffer:
                    import base64
                    png_result = {
                        "image_preview": base64.b64encode(buffer.getvalue()).decode('utf-8'),
                        "file_name": query,
                    }
                else:
                    png_result = {"error": "Failed to render PNG file."}
            except Exception as e:
                png_result = {"error": f"Failed to process PNG file: {e}"}
        else:
            png_result = {"error": "No matching PNG file found for the given ID."}

    return render(request, 'his/doctor.html', {'png_result': png_result})

def book_appointment(request):
    if request.method == "POST":
        patient_name = request.POST.get('patient_name', '')
        phone = request.POST.get('phone', '')
        symptoms = request.POST.get('symptoms', '')
        doctor_name = request.POST.get('doctor_name', '')
        date = request.POST.get('date', '')

        department, _ = Department.objects.get_or_create(name="General")
        doctor, _ = Doctor.objects.get_or_create(name=doctor_name, defaults={'department': department, 'email': ''})
        patient = Patient.objects.create(name=patient_name, phone=phone, symptoms=symptoms)
        appointment = Appointment.objects.create(patient=patient, doctor=doctor, date=date)

        return render(request, 'his/success.html', {'appointment': appointment})

    return render(request, 'his/book_appointment.html')

def search_images(request):
    query = request.GET.get('doctor_name', None)  # 검색할 의사 이름
    images = []
    if query:
        images = Image.objects.filter(doctor__name__icontains=query)  # 부분 검색
    return render(request, 'his/search_images.html', {'images': images, 'query': query})


# DICOM 디렉토리 설정
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DICOM_DIR = os.path.join(BASE_DIR, "media", "dicom_files")

def render_png_as_dicom_style(png_file_path):
    """
    PNG 이미지를 DICOM 스타일로 렌더링하기 위한 함수.
    """
    try:
        # PNG 파일 읽기
        image = Image.open(png_file_path).convert('L')  # Grayscale로 변환
        image_array = np.array(image)

        # Matplotlib로 렌더링
        buffer = BytesIO()
        plt.imshow(image_array, cmap='gray')  # Grayscale
        plt.axis('off')
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        plt.close()

        return buffer
    except Exception as e:
        print(f"Error rendering PNG: {e}")
        return None

def doctor(request):
    query = request.GET.get('id', None)  # 검색할 Patient ID
    png_result = None

    if query:
        # PNG 파일 경로 생성
        png_file = os.path.join(DICOM_DIR, f"{query}.png")

        if os.path.exists(png_file):
            try:
                # PNG 파일 렌더링
                buffer = render_png_as_dicom_style(png_file)
                if buffer:
                    png_result = {
                        "image_preview": base64.b64encode(buffer.getvalue()).decode('utf-8'),
                        "file_name": query,
                    }
                else:
                    png_result = {"error": "Failed to render PNG file."}
            except Exception as e:
                png_result = {"error": f"Failed to process PNG file: {e}"}
        else:
            png_result = {"error": "No matching PNG file found for the given ID."}

    return render(request, 'his/doctor.html', {'png_result': png_result})