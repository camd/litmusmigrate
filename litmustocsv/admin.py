from models import Branches, Products
from django.contrib import admin

class BranchInline(admin.TabularInline):
    model = Branches
    fields = ['name']

class PickerAdmin(admin.ModelAdmin):
	fields = ['name']
	inlines = [BranchInline]

    
admin.site.register(Products, PickerAdmin)
admin.site.register(Branches)

