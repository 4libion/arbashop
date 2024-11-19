from django.contrib import admin
from .models import User, Customer, Farmer, Admin

admin.site.register(User)
admin.site.register(Customer)
admin.site.register(Farmer)
admin.site.register(Admin)