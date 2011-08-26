# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#     * Rearrange models' order
#     * Make sure each model has one field with primary_key=True
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin.py sqlcustom [appname]'
# into your database.

from django.db import models


class Products(models.Model):
    product_id = models.IntegerField(primary_key=True)
    name = models.CharField(unique=True, max_length=192)
    iconpath = models.CharField(max_length=765, blank=True)
    enabled = models.IntegerField(null=True, blank=True)
    creator_id = models.IntegerField()
    last_updated = models.DateTimeField()
    creation_date = models.DateTimeField()
    
    def __unicode__(self):
        return self.name
    
    class Meta:
        db_table = u'products'

class Branches(models.Model):
    product = models.ForeignKey(Products)
    branch_id = models.IntegerField(primary_key=True)
    product_id = models.IntegerField()
    name = models.CharField(max_length=192)
    detect_regexp = models.CharField(max_length=765, blank=True)
    enabled = models.IntegerField(null=True, blank=True)
    creator_id = models.IntegerField()
    last_updated = models.DateTimeField()
    creation_date = models.DateTimeField()
    
    def __unicode__(self):
        return self.name
    
    class Meta:
        db_table = u'branches'

class Testgroups(models.Model):
    testgroup_id = models.IntegerField(primary_key=True)
    product = models.ForeignKey(Products)
    name = models.CharField(max_length=192)
    enabled = models.IntegerField(null=True, blank=True)
    branch_id = models.IntegerField()
    creator_id = models.IntegerField()
    last_updated = models.DateTimeField()
    creation_date = models.DateTimeField()
    
    def __unicode__(self):
        return self.name
    
    class Meta:
        db_table = u'testgroups'
