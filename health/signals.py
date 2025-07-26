# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from django.core.mail import EmailMessage
# from django.conf import settings
# from .models import TestRequest, Profile

# @receiver(post_save, sender=TestRequest)
# def send_result_email(sender, instance, **kwargs):
#     """Send email when test request is marked as Completed and result is uploaded."""
    
#     # Fetch the email from Profile
#     try:
#         profile = Profile.objects.get(user=instance.user)
#         email_to = profile.email  # Use Profile email
#     except Profile.DoesNotExist:
#         print(f"❌ No Profile found for user: {instance.user}")
#         return  # Stop execution

#     if instance.status == "Completed" and instance.result:
#         print(f"✅ Email should be sent to: {email_to}")  # Debugging print
        
#         subject = "Your Test Result is Ready!"
#         body = f"""
#         Hello {instance.user.username},

#         Your test result is now available. You can download it from the link below:

#         http://localhost:8000/{settings.MEDIA_URL}{instance.result}

#         Thank you!
#         """
#         email = EmailMessage(subject, body, settings.DEFAULT_FROM_EMAIL, [email_to])
#         email.send(fail_silently=False)  # Set to False for debugging


from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import EmailMessage
from django.conf import settings
from .models import TestRequest, Profile

@receiver(post_save, sender=TestRequest)
def send_result_email(sender, instance, **kwargs):
    """Send email when test request is marked as Completed and result is uploaded."""
    if instance.status == "Completed" and instance.result:
        user = instance.user
        profile = Profile.objects.filter(user=user).first()  # Fetch profile safely
        email_to = profile.email
        subject = "Your Test Result is Ready!"
        body = f"""
        <html>
        <head></head>
        <body>
            <p>Hello <strong>{profile.fname} {profile.lname}</strong>,</p>

            <p>We are pleased to inform you that your test results are now available.</p>
            <p>Please find the details of your test below:</p>

            <h3>🔬 Test Details</h3>
            <ul>
                <li><strong>Test Name:</strong> {instance.test.name}</li>
                <li><strong>Description:</strong> {instance.test.description if instance.test.description else "N/A"}</li>
                <li><strong>Sample Type:</strong> {instance.test.sample_required}</li>
                <li><strong>Processing Time:</strong> {instance.test.processing_time} hours</li>
                <li><strong>Normal Range:</strong> {instance.test.normal_range if instance.test.normal_range else "N/A"}</li>
            </ul>

            <h3>👤 Your Details</h3>
            <ul>
                <li><strong>Name:</strong> {profile.fname} {profile.lname}</li>
                <li><strong>Email:</strong> {profile.email}</li>
                <li><strong>Contact:</strong> {profile.contact if profile else "Not Available"}</li>
                <li><strong>Address:</strong> {f"{profile.street}, {profile.city}, {profile.state}, {profile.pincode}" if profile else "Not Available"}</li>
            </ul>

            <h3>📄 Download Your Test Result:</h3>
            <p>You can download your test result from the following link:</p>
            <p><a href="http://localhost:8000/{settings.MEDIA_URL}{instance.result}">Download Result</a></p>

            <p>Thank you for choosing our services.</p>
            <p>If you have any questions, feel free to contact us.</p>

            <p>Best Regards,</p>
            <p>🏥 <strong>Medilab Team</strong></p>
        </body>
        </html>
        """

        email = EmailMessage(
            "Your Test Results are Ready", 
            body, 
            settings.DEFAULT_FROM_EMAIL, 
            [profile.email]
        )
        email.content_subtype = "html"  # ✅ Set the email format to HTML
        email.send(fail_silently=False)