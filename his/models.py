from django.db import models

class Department(models.Model):
    name = models.CharField(max_length=100)

class Doctor(models.Model):
    name = models.CharField(max_length=100)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    email = models.EmailField(blank=True, null=True)

class Patient(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    symptoms = models.TextField()

class Appointment(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    date = models.DateTimeField()

class Image(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='patient_images/')  # 이미지 업로드 경로
    description = models.TextField(null=True, blank=True)  # 이미지 설명

    def __str__(self):
        return f"{self.patient.name}'s Image by {self.doctor.name}"
    
class DicomData(models.Model):
    file = models.CharField(max_length=100)
    patient_id = models.CharField(max_length=50)
    age = models.CharField(max_length=10, blank=True, null=True)
    contrast = models.BooleanField(default=False)
    modality = models.CharField(max_length=20, blank=True, null=True)
    image_preview = models.ImageField(upload_to="dicom_previews/")  # 변환된 이미지 저장

    def __str__(self):
        return f"{self.patient_id} ({self.file})"