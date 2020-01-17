from django.shortcuts import render, redirect
from ca.models import * 
from auths.models import CA_Detail
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse


@login_required
def contactUs(request):
	if request.method == 'POST':
		COMPLAINT_CATEGORY_CHOICES = {
		('General', 'General'),
		('Technical', 'Technical'),
		('Competition', 'Competition'),
		('Festival', 'Festival'),
		('Payment', 'Payment'),
		}
		complaint_category_list = [x[0] for x in COMPLAINT_CATEGORY_CHOICES]
		data = {}
		if request.POST['complaint_category'] == '':
			 data['complaint_category_stat'] = "Complaint category empty"
		if request.POST['complaint_category'] not in complaint_category_list:
			 data['complaint_category_stat'] = "INVALID COMPLAINT CATEGORY"

		if request.POST['complaint_text'] == '':
			 data['complaint_text_stat'] = "Complaint text empty"

		if data.get('category') or data.get('desc'):
			data['stat'] = "FAILURE"
			return JsonResponse(data)
		else :
			complaint_text = request.POST['complaint_text']
			complaint_category = request.POST['complaint_category']
			Complaints.objects.create(user=request.user, complaint_text=complaint_text, 
				complaint_category=complaint_category)
			data['stat'] = "SUCCESS"

		return JsonResponse(data)
	else:
		ca_dets = request.user.ca_details
		if ca_dets.ca_profile_complete and not ca_dets.ca_approval :
			return redirect('ca:pending')
		elif not ca_dets.ca_profile_complete :
			return redirect('ca:questionnare')
		else :
			prevQueries = Complaints.objects.filter(user=request.user).order_by('-pk')

			context = {
			'prevQueries': prevQueries,
			'more_active': True,
			}

			return render(request, 'ca/contacts.html', context)


@login_required
def submitIdea(request):
	if request.method == 'POST':
			data = {}
			if request.POST['idea_category'] == '':
				 data['category'] = "Category Empty"

			if request.POST['idea_desc'] == '':
				 data['desc'] = "Desc Empty"

			if data.get('category') or data.get('desc'):
				data['stat'] = "Failure"
				return JsonResponse(data)
			else :
				idea = request.POST['idea_desc']
				idea_category = request.POST['idea_category']
				Idea.objects.create(user=request.user, idea=idea, idea_category=idea_category)
				data['stat'] = "Success"

			return JsonResponse(data)
	else:
		ca_dets = request.user.ca_details
		if ca_dets.ca_profile_complete and not ca_dets.ca_approval :
			return redirect('ca:pending')
		elif not ca_dets.ca_profile_complete :
			return redirect('ca:questionnare')
		else :
			ideaQueries = Idea.objects.filter(user=request.user).order_by('-pk')

			context = {
				'ideaQueries': ideaQueries,
				'idea_active': True,
			}

			return render(request, 'ca/idea.html', context)

@login_required
def faqs(request):
	if request.method == 'POST':
		faq_category = request.POST['faq_category']
		faqs = FAQ.objects.filter(faq_category=faq_category)

		context = {
		'faqs':faqs,
		}

		return render(request, 'ca/faq_response.html', context)

	else:
		ca_dets = request.user.ca_details
		if ca_dets.ca_profile_complete and not ca_dets.ca_approval :
			return redirect('ca:pending')
		elif not ca_dets.ca_profile_complete :
			return redirect('ca:questionnare')
		else :
			return render(request, 'ca/faq.html', {'more_active': True})


@login_required
def venue(request):
	ca_dets = request.user.ca_details
	if ca_dets.ca_profile_complete and not ca_dets.ca_approval :
		return redirect('ca:pending')
	elif not ca_dets.ca_profile_complete :
		return redirect('ca:questionnare')
	else :
		venues = Venue.objects.filter(user=request.user).order_by('-pk')
		name_pattern = "A-Za-z ";
		team_name_pattern = "A-Za-z0-9, ";
		phone_pattern = "0-9";

		context = {
		'venues': venues,
		'name_pattern':name_pattern,
		'team_name_pattern':team_name_pattern,
		'phone_pattern':phone_pattern,
		'more_active': True,
		}

		return render(request, 'ca/venue.html', context)



@login_required
def questionnare(request):
	if request.method == 'POST':
		alt_contact = request.POST['alt_contact']
		acad = request.POST['acad']
		college_name = request.POST['college_name']
		city = request.POST['city']
		mailing_address = request.POST['mailing_address']
		fb = request.POST['fb']
		por = request.POST['por']
		referral_code = request.POST['referral']

		print(alt_contact, acad,"$$$$$$$$$$$$$$$$$$$$")

		CA_Questionnaire.objects.create(user = request.user, alt_contact=alt_contact, acad=acad,
			college_name=college_name, city=city, mailing_address=mailing_address, fb=fb, por=por,
			referral_code=referral_code)

		ca_det_user = CA_Detail.objects.get(user=request.user)
		ca_det_user.ca_profile_complete = True
		ca_det_user.save()
		return redirect('ca:pending')
	else :
		ca_dets = request.user.ca_details
		if ca_dets.ca_profile_complete and ca_dets.ca_approval :
			return redirect('ca:home')
		elif ca_dets.ca_profile_complete and not ca_dets.ca_approval :
			return redirect('ca:questionnare')
		else :
			context = {
				'email': request.user.email,
				'phone_no': request.user.profile.phone,
				'college': request.user.profile.college,
			}
			return render(request, 'ca/questionnare.html', context)


@login_required
def home(request):
	ca_dets = request.user.ca_details
	if ca_dets.ca_profile_complete and not ca_dets.ca_approval :
		return redirect('ca:pending')
	elif not ca_dets.ca_profile_complete :
		return redirect('ca:questionnare')
	else :
		return render(request, 'ca/home.html', { 'home_active': True })


@login_required
def guidelines(request):
	ca_dets = request.user.ca_details
	if ca_dets.ca_profile_complete and not ca_dets.ca_approval :
		return redirect('ca:pending')
	elif not ca_dets.ca_profile_complete :
		return redirect('ca:questionnare')
	else :
		return render(request, 'ca/guidelines.html', { 'guidelines_active': True })


@login_required
def pending(request):
	ca_dets = request.user.ca_details
	if ca_dets.ca_profile_complete and ca_dets.ca_approval :
		return redirect('ca:home')
	elif not ca_dets.ca_profile_complete :
		return redirect('ca:questionnare')
	else :
		return render(request, 'ca/pending.html')


@login_required
def hospitality(request):
	ca_dets = request.user.ca_details
	if ca_dets.ca_profile_complete and not ca_dets.ca_approval :
		return redirect('ca:pending')
	elif not ca_dets.ca_profile_complete :
		return redirect('ca:questionnare')
	else :
		return render(request, 'ca/hospitality.html', {'more_active': True})


@login_required
def poc(request):
	ca_dets = request.user.ca_details
	if ca_dets.ca_profile_complete and not ca_dets.ca_approval :
		return redirect('ca:pending')
	elif not ca_dets.ca_profile_complete :
		return redirect('ca:questionnare')
	else :
		return render(request, 'ca/poc.html', {'more_active': True})

@login_required
def standings(request):
	ca_dets = request.user.ca_details
	if ca_dets.ca_profile_complete and not ca_dets.ca_approval :
		return redirect('ca:pending')
	elif not ca_dets.ca_profile_complete :
		return redirect('ca:questionnare')
	else :
		return render(request, 'ca/standings.html', {'more_active': True})