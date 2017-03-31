from django.shortcuts import render, redirect, HttpResponse
from .models import User, Quote, Favorite
from django.contrib import messages
from django.core.mail import send_mail
# Create your views here.
def index(request):
	return render(request,'black_belt/index.html')

def quotes(request):
	if 'loggedIn' not in request.session:
		messages.warning(request, 'You must be logged in')
		return redirect('/')

	user = User.userManager.filter(id=request.session['user_id'])
	favorites = Favorite.objects.filter(user_id=user[0])
	context = {
		'quotes': Quote.objects.exclude(favorite__user_id_id=user[0]),
		'favorites': favorites
	}
	return render(request,'black_belt/quotes.html',context)

def addFavorite(request,quoteid):
	user = User.userManager.filter(id=request.session['user_id'])
	quote = Quote.objects.filter(id=quoteid)
	try:
		f = Favorite(quote_id=quote[0],user_id=user[0])
		f.save()
		messages.success(request, 'Favorite Successfully Saved')
		return redirect('/quotes')
	except Exception as e:
		messages.warning(request, e)
		return redirect('/quotes')

def destroyFavorite(request,favoriteid):
	user = User.userManager.filter(id=request.session['user_id'])
	f = Favorite.objects.get(id=favoriteid)

	try:
		f.delete()
		messages.success(request, 'Favorite Successfully Deleted')
		return redirect('/quotes')
	except Exception as e:
		messages.warning(request, e)
		return redirect('/quotes')

def create(request):
	user = User.userManager.filter(id=request.session['user_id'])
	#with more time we can create a custom quote manager and validate in model, fat models are more better
	errors = 0
	if len(request.POST['quoted_by']) <3:
		messages.warning(request,'Quoted by field must be at least 3 characters in length')
		errors = errors + 1
	if len(request.POST['quote_message']) <10:
		messages.warning(request,'Quote message must be at least 10 characters in length')
		errors = errors + 1

	if errors >0:
		return redirect('/quotes')

	q = Quote(quoted_by=request.POST['quoted_by'],message=request.POST['quote_message'],submitted_by=user[0])

	try:
		q.save()
		messages.success(request, 'Quote Successfully Saved')
		return redirect('/quotes')
	except Exception as e:
		messages.warning(request, e)
		return redirect('/quotes')

def user (request,userid):
	if 'loggedIn' not in request.session:
		messages.warning(request, 'You must be logged in')
		return redirect('/')

	user = User.userManager.filter(id=userid)
	quotes = Quote.objects.filter(submitted_by=user)
	print (user[0].first_name)
	context = {
		'user': user[0],
		'posts': quotes,
		'count': len(quotes)
	}
	return render(request,'black_belt/user_profile.html',context);
def register(request):
	

	# step one lets try to validate that email and register the user
	if User.userManager.filter(email=request.POST['email']):
		messages.warning(request, "Oops, looks like you are already registered, try logging in!")
		return redirect('/')
	try:
		User.userManager.register(request.POST['email'],request.POST['password'],request.POST['password2'],request.POST['first_name'],request.POST['last_name'],request.POST['date_of_birth'])
		try:
			success = User.userManager.login(request.POST['email'],request.POST['password'])
			if success == False:
				messages.warning(request,"Incorrect Login")
				return redirect('/')
			else:
				user = User.userManager.filter(email=request.POST['email'])
				request.session['user_id'] = user[0].id
				request.session['first_name'] = user[0].first_name
				request.session['loggedIn'] = True
				send_mail('Welcome to Quotes!', 'Welcome to the dojo quoting exam app.', 'mw@worldsourcetech.com', [user[0].email], fail_silently=True)
				messages.success(request, "User Registered and Successfully Logged In")
				return redirect('/quotes')
		except Exception as e:
			messages.warning(request, e)
			return redirect('/')
	except Exception as e:
		print e
		if e == "password error":
			messages.warning(request,'Password must be at least 8 characters long')
		else:
			messages.warning(request, e)
		return redirect('/')


def login(request):
	errors =0
	if len(request.POST['email'])<1:
		messages.warning(request,"Email field required")
		errors + 1

	if len(request.POST['password'])<1:
		messages.warning(request,"Password field required")
		errors + 1

	if errors >0:
		return redirect('/')

	try:
		success = User.userManager.login(request.POST['email'],request.POST['password'])
		if success == False:
			messages.warning(request,"Incorrect Login")
			return redirect('/')
		else:
			user = User.userManager.filter(email=request.POST['email'])
			request.session['user_id'] = user[0].id
			request.session['first_name'] = user[0].first_name
			request.session['loggedIn'] = True
			messages.success(request, "User Successfully Logged In")
			return redirect('/quotes')
	except Exception as e:
		messages.warning(request, e)
		return redirect('/')

def success(request):
	return render(request,'black_belt/quotes.html')

def logout(request):
	del request.session['loggedIn']
	del request.session['first_name']
	del request.session['user_id']
	messages.success(request, "User Successfully Logged Out")
	return redirect('/')