# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#     * Rearrange models' order
#     * Make sure each model has one field with primary_key=True
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin.py sqlcustom [appname]'
# into your database.

from django.db import models

class Product(models.Model):
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

class Branch(models.Model):
    branch_id = models.IntegerField(primary_key=True)
    product = models.ForeignKey(Product)
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






class Testgroup(models.Model):
    testgroup_id = models.IntegerField(primary_key=True)
    product = models.ManyToManyField(Product, through='GroupProductMap')
    name = models.CharField(max_length=192)
    enabled = models.IntegerField(null=True, blank=True)
    branch = models.ForeignKey(Branch)
    creator_id = models.IntegerField()
    last_updated = models.DateTimeField()
    creation_date = models.DateTimeField()

    def __unicode__(self):
        return self.name

    class Meta:
        db_table = u'testgroups'



class Subgroup(models.Model):
    subgroup_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=192)
    enabled = models.IntegerField(null=True, blank=True)
    product = models.ForeignKey(Product)
    branch = models.ForeignKey(Branch)
    creator_id = models.IntegerField()
    last_updated = models.DateTimeField()
    creation_date = models.DateTimeField()
    testgroup = models.ManyToManyField(Testgroup, through='SubgroupTestgroup')

    def __unicode__(self):
        return self.name

    class Meta:
        db_table = u'subgroups'

class Testcase(models.Model):
    testcase_id = models.IntegerField(primary_key=True)
    summary = models.CharField(max_length=765)
    details = models.TextField(blank=True)
    community_enabled = models.IntegerField(null=True, blank=True)
    format_id = models.IntegerField()
    regression_bug_id = models.IntegerField(null=True, blank=True)
    steps = models.TextField(blank=True)
    expected_results = models.TextField(blank=True)
    author_id = models.IntegerField()
    creation_date = models.DateTimeField()
    last_updated = models.DateTimeField()
    version = models.IntegerField()
    enabled = models.IntegerField()
    product = models.ForeignKey(Product)
    branch = models.ForeignKey(Branch)
    subgroup = models.ManyToManyField(Subgroup, through='TestcaseSubgroup')

    def __unicode__(self):
        return self.summary

    class Meta:
        db_table = u'testcases'



class GroupProductMap(models.Model):
    group = models.ForeignKey(Testgroup)
    product = models.ForeignKey(Product)

    def __unicode__(self):
        return self.name

    class Meta:
        db_table = u'group_product_map'


class SubgroupTestgroup(models.Model):
    subgroup = models.ForeignKey(Subgroup)
    testgroup = models.ForeignKey(Testgroup)
    sort_order = models.IntegerField()

    def __unicode__(self):
        return self.name

    class Meta:
        db_table = u'subgroup_testgroups'


class TestcaseSubgroup(models.Model):
    testcase = models.ForeignKey(Testcase)
    subgroup = models.ForeignKey(Subgroup)
    sort_order = models.IntegerField()

    def __unicode__(self):
        return self.name

    class Meta:
        db_table = u'testcase_subgroups'




