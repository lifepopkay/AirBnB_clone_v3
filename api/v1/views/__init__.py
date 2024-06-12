#!/usr/bin/python3
"""Initialize files"""
from api.v1.views.places_amenities import *
from api.v1.views.users import *
from api.v1.views.places_reviews import *
from api.v1.views.places import *
from api.v1.views.cities import *
from api.v1.views.amenities import *
from api.v1.views.states import *
from api.v1.views.index import *
from flask import Blueprint

app_views = Blueprint('/api/vi', __name__,  url_prefix="/api/v1")
