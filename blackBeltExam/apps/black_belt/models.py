from __future__ import unicode_literals
from django.db import models
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.contrib import messages
import bcrypt 
# Create your models here.
class UserManager(models.Manager):
	def register(self,email,password,password2,first_name,last_name,dob):	
		try: 
			validate_email( email )
		except ValidationError as e:
			print e
			return False
		if len(password) < 8:			
			raise NameError('Password Must be 8 characters')
			return False
		if password !=password2:
			raise NameError('Passwords must match ')
			return False
		if len(first_name) <2:
			raise NameError('First name has to be at least 2 characters')
			return False
		if len(last_name) <2:
			return NameError('Last name has to be at least 2 characters')

		try:
			hashed = bcrypt.hashpw(password.encode(),bcrypt.gensalt())
			newUser = User(first_name=first_name,last_name=last_name,password=hashed,email=email,birth_date=dob)
			newUser.save()
			return True
		except ValidationError as e:
			print e
			return False

	def login(self,email,password):
		#firs check if user exists
		user = User.userManager.filter(email=email)
		print user[0].id
		#also hash the password
		userPassword = user[0].password.encode()
		if bcrypt.hashpw(password.encode(), userPassword) == userPassword:
			userInfo = {
			'first_name':user[0].first_name,
			'user_id':user[0].id,
			'loggedIn': True
			}
			return userInfo
		else:
			return False
		# 	hashed == userPassword
		# 	#and their password matches
		# 	request.session['loggedIn'] = True
		# 	#log them in and save pertinent data to session
		# 	reqeust.session['user_id'] =  user[0].id
		# 	request.session['first_name'] = user[0].first_name
		# 	return True
		# except Exception as e:
		# 	print e
		# 	return False
class User(models.Model):
	first_name = models.CharField(max_length=255)
	last_name = models.CharField(max_length=255)
	password = models.CharField(max_length=255)
	email = models.CharField(max_length=255)
	birth_date = models.DateField(null=True, blank=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	userManager = UserManager()

class Quote(models.Model):
	quoted_by =models.CharField(max_length=255)
	message =models.TextField(max_length=1000)
	submitted_by = models.ForeignKey(User)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

class Favorite(models.Model):
	quote_id = models.ForeignKey(Quote)
	user_id = models.ForeignKey(User)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)



