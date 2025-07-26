from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField



# Create your models here.

class Feedback(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	feedback = models.TextField()

	def __str__(self):
		return self.user.username

class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    fname = models.CharField(max_length=20)
    lname = models.CharField(max_length=20)
    age = models.IntegerField()
    contact = models.BigIntegerField()  # Use BigIntegerField
    gender = models.CharField(max_length=10)
    email = models.CharField(max_length=50)
    street = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    state = models.CharField(max_length=200)
    pincode = models.BigIntegerField()  # Use BigIntegerField
    
    def __str__(self):
        return self.fname


class Doctor(models.Model):
    name = models.CharField(max_length=50)
    category = models.CharField(max_length=200)
    contact = models.CharField(max_length=15)  # Use CharField instead of IntegerField
    address = models.TextField()

    def __str__(self):
        return self.name


class Questions(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	pregnant = models.CharField(max_length=50, blank=True)
	weight = models.CharField(max_length=50)
	cigarettes = models.CharField(max_length=50)
	injured = models.CharField(max_length=50)
	cholestrol = models.CharField(max_length=50)
	hypertension = models.CharField(max_length=50)

	def __str__(self):
		return self.user.username


class Symptoms(models.Model):
	symptom_id = models.CharField(max_length=15)
	symptom_name = models.CharField(max_length=200)

	def __str__(self):
		return self.symptom_name

class Disease(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	ids_of_selected_symptoms = ArrayField(ArrayField(models.CharField(max_length=100)))
	name_of_selected_symptoms = ArrayField(ArrayField(models.CharField(max_length=500)))
	result_of_predicted_disease = models.CharField(max_length=500)

	def __str__(self):
		return self.user.username

class Test(models.Model):
    name = models.CharField(max_length=200, unique=True)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    sample_required = models.CharField(max_length=100, choices=[
        ('Blood', 'Blood'),
        ('Urine', 'Urine'),
        ('Saliva', 'Saliva'),
        ('Stool', 'Stool'),
        ('Other', 'Other')
    ])
    processing_time = models.IntegerField(help_text="Time in hours",null=True, blank=True)
    normal_range = models.CharField(max_length=100, blank=True, null=True)
    
    def __str__(self):
        return self.name
	
class TestRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    request_date = models.DateTimeField()  # Allow user input for request date
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)  # Auto-sets when created
    status = models.CharField(max_length=50, choices=[
        ('Pending', 'Pending'),
        ('In Progress', 'In Progress'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled')
    ], default='Pending')
    result = models.FileField(upload_to='test_results/', blank=True, null=True)  # Store PDF files

    def __str__(self):
        return f"{self.user.username} - {self.test.name}"
