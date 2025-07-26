import json
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import auth
from .models import Feedback, Profile, Doctor, Questions, Symptoms, Disease, Test, TestRequest
from .data import symptoms_list
import infermedica_api
from django.shortcuts import get_object_or_404
from django.http import FileResponse, HttpResponse
import google.generativeai as genai
from django.utils.dateparse import parse_datetime
# Create your views here.


genai.configure(api_key="AIzaSyBh9Wfefpi8SqoJmPLnvkofA5Sv0PcmGBg")

def home(request):
	return render(request, 'home.html')


def signup(request):
	if request.method == 'POST':
		if request.POST['pass1'] == request.POST['pass2'] and len(request.POST['pass1']) > 8 :
			try:
				user = User.objects.get(username=request.POST['uname'])
				context = {
					'error': 'Username already taken.'
				}
				return render(request, 'signup.html', context)
			except User.DoesNotExist:
				user = User.objects.create_user(username=request.POST['uname'], password=request.POST['pass1'])
				auth.login(request, user)
				return redirect('login')
		else:
			context = {
				'error': 'Password must match or Length of Password must be greater than 8.'
			}
			return render(request, 'signup.html', context)
	else:
		return render(request, 'signup.html')


def login(request):
	if request.method == 'POST':
		user = auth.authenticate(username=request.POST['uname'], password=request.POST['pass1'])
		if user is not None:
			auth.login(request,user)
			# question = Questions.objects.filter(user_id=request.user.id)
			profile = Profile.objects.filter(user_id=request.user.id)
			if profile:
				return redirect('index')
			else:
				return redirect('add_profile')
		else:
			context = {
				'error': 'Username or password is incorrect.'
			}
			return render(request, 'login.html', context)
	else:
		return render(request, 'login.html')


def logout(request):
	if request.method == 'POST':
		auth.logout(request)
		return redirect('home')


def index(request):
	profile = Profile.objects.filter(user_id = request.user.id)
	context = {
		'profile': profile
	}
	return render(request, 'index.html', context)


def feedback(request):
	if request.method == 'POST':
		feed = request.POST['feed']
		if feed != '':
			feedback = Feedback(feedback = feed, user_id = request.user.id)
			feedback.save()
			return redirect('index')
		else:
			context = {
				'error': "Feedback can't be blank."
			}
			return render(request, 'feedback.html', context)
	return render(request, 'feedback.html')



def add_profile(request):
	if request.method == 'POST':
		profile = Profile(fname = request.POST['fname'], lname = request.POST['lname'],
						  age = request.POST['age'],  contact = request.POST['contact'], gender = request.POST['gender'].capitalize(),
						  email = request.POST['email'], street = request.POST['street'], city = request.POST['city'],
						  state = request.POST['state'], pincode = request.POST['pin'],user_id = request.user.id)
		profile.save()
		return redirect('question')
	return render(request, 'add_profile.html')


def see_profile(request):
	profile = Profile.objects.filter(user_id = request.user.id)
	context = {
		'profile': profile
	}
	return render(request, 'see_profile.html', context)


def doctor(request):
	query = Doctor.objects.all()

	if 'name' in request.GET:
		name = request.GET['name']
		if name:
			query = query.filter(name__icontains=name)

	if 'category' in request.GET:
		category = request.GET['category']
		if category:
			query = query.filter(category__icontains=category)

	if 'address' in request.GET:
		address = request.GET['address']
		if address:
			query = query.filter(address__icontains=address)

	return render(request, 'doctor.html', {'query': query})


def question(request):
	gender = Profile.objects.filter(user_id=request.user.id).filter(gender='Female')
	person = Profile.objects.get(user_id=request.user.id)
	print(person.fname)
	if request.method == 'POST':
		questions = Questions(pregnant = request.POST['pregnant'], weight = request.POST['weight'],
						  cigarettes = request.POST['cig'], injured = request.POST['inj'],
						  cholestrol = request.POST['ch'], hypertension = request.POST['hyp'],
						  user_id = request.user.id)
		questions.save()
		return redirect('index')
	context = {
		'gender': gender,
		'person': person,
	}
	return render(request, 'question.html', context)


# def api_function(array):
# 	api = infermedica_api.configure(app_id='548236', app_key='mjncNunUBo089bkBKLSJ') # Your app_id and app_key (from infermedica)
# 	request = infermedica_api.Diagnosis(sex='male', age=35)
# 	for i in array:
# 		request.add_symptom(i, 'present')
# 	request = api.diagnosis(request)

# 	result = request.conditions[0]['name']
# 	return result

def ai_predict_disease(symptoms):
    """ Uses Google Gemini AI to predict disease based on symptoms. """
    model = genai.GenerativeModel("gemini-pro")  # Use appropriate Gemini model
    prompt = f"I have the following symptoms: {', '.join(symptoms)}. What could be the possible disease? Give a single disease."
    
    try:
        response = model.generate_content(prompt)
        result = response.text.strip()
        return result
    except Exception as e:
        return f"Error in AI prediction: {str(e)}"




# def check_disease(request):
# 	pro = Profile.objects.get(user_id = request.user.id)
# 	# symptoms_from_database = Symptoms.objects.all()
# 	result = ''
# 	symptoms_names = []
# 	if request.method == 'POST':
# 		symptoms_ids = request.POST.getlist('disease')
# 		result = api_function(symptoms_ids)
# 		print(result)
# 		print(symptoms_ids)
# 		symptoms_names = []
# 		for id in symptoms_ids:
# 			if id in symptoms_list:
# 				symptom_name = symptoms_list[id]
# 				symptoms_names.append(symptom_name)
# 		print(symptoms_names)
# 		disease = Disease(ids_of_selected_symptoms=symptoms_ids, name_of_selected_symptoms=symptoms_names,
# 						  result_of_predicted_disease=result, user_id = request.user.id)
# 		disease.save()
# 	context = {
# 		'result': result,
# 		'user': pro,
# 		'symptoms': symptoms_names
# 	}
# 	return render(request, 'check_disease.html', context)


def check_disease(request):
    pro = Profile.objects.get(user_id=request.user.id)
    result = ''
    symptoms_names = []

    if request.method == 'POST':
        symptoms_ids = request.POST.getlist('disease')

        # Convert symptom IDs to actual names
        for id in symptoms_ids:
            if id in symptoms_list:
                symptoms_names.append(symptoms_list[id])

        # Call AI model for disease prediction
        result = ai_predict_disease(symptoms_names)
	
        # Save the prediction in the database
        disease = Disease(
            ids_of_selected_symptoms=[symptoms_ids],
            name_of_selected_symptoms=[symptoms_names],
            result_of_predicted_disease=result,
            user_id=request.user.id
        )
        print(disease)  # Ensure consistent spaces

        disease.save()


    context = {
        'result': result,
        'user': pro,
        'symptoms': symptoms_names
    }
    return render(request, 'check_disease.html', context)



def test_form(request):
    tests = Test.objects.all()
    return render(request, 'test_form.html', {'tests': tests})


def submit_test_request(request):
    if request.method == 'POST':
        test_id = request.POST.get('test')  # Get test ID from form
        request_date = request.POST.get('request_date')  # Get request date from form

        if not request_date:
            # Handle case where request_date is missing (optional)
            return render(request, 'test_form.html', {'error': 'Request date is required'})

        test = get_object_or_404(Test, id=test_id)  # Ensure test exists

        # Convert string input to a datetime object
        parsed_request_date = parse_datetime(request_date)
        if not parsed_request_date:
            return render(request, 'test_form.html', {'error': 'Invalid date format'})

        # Create TestRequest
        test_request = TestRequest.objects.create(
            user=request.user,
            test=test,
            request_date=parsed_request_date,  # Use user-inputted date
            status='Pending'  # Default status
        )
        
        return redirect('test_requests')  # Redirect to user's test requests
    
    return redirect('test_form')  # If GET request, redirect to form page

def test_requests(request):
    user_requests = TestRequest.objects.filter(user=request.user).order_by('request_date')  # Ascending order
    return render(request, 'test_requests.html', {'test_requests': user_requests})


def download_result(request, test_request_id):
    test_request = get_object_or_404(TestRequest, id=test_request_id)
    
    if not test_request.result:
        return HttpResponse("No result available", status=404)
    
    response = FileResponse(test_request.result.open('rb'), as_attachment=True)
    return response
