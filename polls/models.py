import datetime

from django.db import models
from django.utils import timezone
# Create your models here.
# polls/models.py


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now
        # return self.pub_date >= timezone.now() - datetime.timedelta(days=1)

    was_published_recently.admin_order_field = 'pub_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Published recently?'

    def __str__(self):
        return self.question_text

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text

from datetime import date

from django.db import models

# 测试 on_delete
class Artist(models.Model):
    name = models.CharField(max_length=10)

    def __str__(self):
        return self.name

class Album(models.Model):
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)  # 注意这里
    def __str__(self):
        return self.artist.name

class Song(models.Model):
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE) # 注意这里
    album = models.ForeignKey(Album, on_delete=models.RESTRICT) # 注意这里

# artist_one = models.Artist.objects.create(name='artist one')
# artist_two = models.Artist.objects.create(name='artist two')
# models.Album.objects.create(artist=artist_one)
# models.Album.objects.create(artist=artist_two)


#  测试related_name  /  related_query_name
# 一篇文章 有 多个标签
class Article(models.Model):
    art_name = models.CharField(max_length=255)


class Tag(models.Model):
    article = models.ForeignKey(
        Article,
        on_delete=models.CASCADE,
        # related_name="tags",
        # related_query_name="tag",       # 注意这一行
    )
    name = models.CharField(max_length=255)


# 多对多的使用
class Person(models.Model):
    name = models.CharField(max_length=128)
    def __str__(self):
        return self.name

class Group(models.Model):
    name = models.CharField(max_length=128)
    members = models.ManyToManyField(Person, through='Membership')
    def __str__(self):
        return self.name

class Membership(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    date_joined = models.DateField()        # 进组时间
    invite_reason = models.CharField(max_length=64)  # 邀请原因

'''
from xxx.models import Person, Group, Membership

ringo = Person.objects.create(name="Ringo Starr")
paul = Person.objects.create(name="Paul McCartney")
beatles = Group.objects.create(name="The Beatles")

m1 = Membership(person=ringo, group=beatles,
    date_joined=date(1962, 8, 16),
    invite_reason="Needed a new drummer.")
m1.save()
beatles.members.all()

ringo.group_set.all()
m2 = Membership.objects.create(person=paul, group=beatles,
    date_joined=date(1960, 8, 1),
    invite_reason="Wanted to form a band.")
beatles.members.all()
'''

# 多表继承
from django.db import models

class Place(models.Model):
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=80)

class Restaurant(Place):
    serves_hot_dogs = models.BooleanField(default=False)
    serves_pizza = models.BooleanField(default=False)

"""
from xxx.models import Place, Restaurant
"""


# QuerySet
from django.db import models

class Blog(models.Model):
    name = models.CharField(max_length=100)
    tagline = models.TextField()

    def __str__(self):
        return self.name

class Author(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()

    def __str__(self):
        return self.name

class Entry(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    headline = models.CharField(max_length=255)
    body_text = models.TextField()
    pub_date = models.DateField()
    mod_date = models.DateField()
    authors = models.ManyToManyField(Author)
    number_of_comments = models.IntegerField()
    number_of_pingbacks = models.IntegerField()
    rating = models.IntegerField()

    def __str__(self):
        return self.headline