from flask import Flask, render_template, Markup, request, redirect, session, abort, url_for, flash
from flask_session import Session
from functools import wraps

import requests
import json

# Firebase Imports
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore


# Initialize the firebase app

try:
    app = firebase_admin.get_app()
except ValueError as e:
    # Use a service account
    cred = credentials.Certificate("uwi-shuttle-user-id-firebase-adminsdk-gv3ie-6d3bef9f35.json")
    firebase_admin.initialize_app(cred)

db = firestore.client()

routes_ref = db.collection('ROUTES')
routes_list = routes_ref.get()
x = ""

for doc in routes_list:
    print("x")