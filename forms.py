from flask import Flask, request, logging,session
from flask import render_template,redirect,url_for
from wtforms import StringField,Form, TextAreaField,validators,PasswordField
from passlib.hash import sha256_crypt

class RegisterForm(Form):
    name= StringField('Name',[validators.length(min=1, max=50)])
    username= StringField('Username', [validators.length(min=4, max=30)])
    email= StringField('Email', [validators.length(min=6, max=50)])
    password= PasswordField('Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords do not match')
        ])
    confirm = PasswordField('Confirm Password')



    

