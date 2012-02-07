from models import Branch, Product, Testcase, Testgroup, Subgroup
from django.contrib import admin

class BranchInline(admin.TabularInline):
    model = Branch
    fields = ['name']

class PickerAdmin(admin.ModelAdmin):
	fields = ['name']
	inlines = [BranchInline]

    
admin.site.register(Product, PickerAdmin)
admin.site.register(Branch)
admin.site.register(Testcase)
admin.site.register(Testgroup)
admin.site.register(Subgroup)
