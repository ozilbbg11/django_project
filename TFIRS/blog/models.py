from django.db import models
from django.contrib.auth.models import User


class Recipe(models.Model):
    objects = models.Manager()
    recipe_id = models.AutoField(primary_key=True)
    keyword = models.CharField(max_length=100)
    cuisines = models.CharField(max_length=100)
    name = models.CharField(max_length=300)
    ingredient = models.CharField(max_length=10000, blank=True)

    def __str__(self):
        return self.name


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    content = models.TextField(max_length=1000)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{}-{}'.format(self.recipe.name, str(self.user.username))