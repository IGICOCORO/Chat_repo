from .models import *
from django import forms

class ConnexionForm(forms.Form):
	username = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Username ','class':'form-control'}))
	password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Password ', 'type':'password','class':'form-control'}))

class MessageForm(forms.ModelForm):
	file = forms.FileField(
		widget=forms.FileInput(
			attrs={
				'placeholder':'profile picture ',
				'class':'form-control',
				'style':"display: none;",
				'id': 'file_input'
			})
		)
	message = forms.CharField(
		widget=forms.TextInput(
			attrs={
				'placeholder':'Leave a message',
				'class':'MuiInputBase-input MuiInput-input',
			}
		)
	)
	class Meta:
		model = Message
		fields = ('content','file')

class RegisterForm(forms.Form):
	username = forms.CharField( widget=forms.TextInput(attrs={'placeholder':'Username ','class':'form-control'}), label='Username')
	firstname = forms.CharField( widget=forms.TextInput(attrs={'placeholder':'Firstname ','class':'form-control'}), label='Firstname')
	lastname = forms.CharField( widget=forms.TextInput(attrs={'placeholder':'Lastname ','class':'form-control'}), label='Lastname')
	password = forms.CharField( widget=forms.PasswordInput(attrs={'placeholder':'Password ','class':'form-control'}), label='Password')
	password2 = forms.CharField( widget=forms.PasswordInput(attrs={'placeholder':'Confirm password ','class':'form-control'}), label='Confirm password')
	picture = forms.ImageField( widget=forms.FileInput(attrs={'placeholder':'profile picture ','class':'form-control'}), label='Profile Picture')
	
	def clean_password2(self, *arg,**kwargs):
		try:
			password = self.cleaned_data.get("password")
			password2 = self.cleaned_data.get("password2")
			print(password, password2)
			if(password == password2):
				return password
			else :
				raise forms.ValidationError("confirmation password must same as password")
		except Exception as e:
			raise forms.ValidationError("confirmation password must same as password")