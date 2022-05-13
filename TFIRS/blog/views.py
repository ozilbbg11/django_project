from django.contrib.admin.templatetags.admin_list import pagination
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView
from django.db.models import Q
from pymongo import MongoClient
from operator import itemgetter
from datetime import *
from .models import Recipe
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger, InvalidPage


# Create your views here.
#date and wk num
today = datetime.today()
thisWeek = today.strftime("%U")

def home(request):
    return render(request, 'blog/home.html',)


def about(request):
    return render(request, 'blog/about.html', {'title': 'About'})


def trend(request):
    client = MongoClient("mongodb://localhost:27017/")
    database = client["fyp"]
    collection = database["forecast"]
    nextWeek = int(thisWeek) + 1

    # Weekly top
    query = {"trend.%s.value" % nextWeek: {'$gt': 75}}
    cursor = collection.find(query).sort([("trend.%s.value" % nextWeek, -1)])
    keyword = []
    try:
        for doc in cursor:
            keyword.append({'id': doc['keyword'], 'heat': doc['trend']})
        keyword = keyword[:5]
    finally:
        client.close()

    # Monthly top 5

    query = {"trend.%s.value" % nextWeek: {'$gt': 50}}
    cursor = collection.find(query).sort([("trend.%s.value" % nextWeek, -1)])
    topInMonth = {}
    arrSum = []
    try:
        for doc in cursor:
            print(doc['keyword'])
            month = doc['trend'][nextWeek]['value'] + doc['trend'][nextWeek + 1]['value'] + doc['trend'][nextWeek + 2][
                'value'] + \
                    doc['trend'][nextWeek + 3]['value']
            topInMonth = {'id': doc['keyword'], 'value': month, 'heat': doc['trend']}
            arrSum.append(topInMonth)
        newlist = sorted(arrSum, key=itemgetter('value'), reverse=True)
        top5 = newlist[:5]
    finally:
        client.close()

    # Hidden Gem
    query = {"trend.value": {'$gt': 95}}
    cursor = collection.find(query).sort([("trend.value", -1)])
    hidden = []
    try:
        for doc in cursor:
            hidden.append({'id': doc['keyword'], 'heat': doc['trend']})
        hidden = hidden[:5]
    finally:
        client.close()

    return render(request, 'blog/trend.html', {'weekTrend': keyword, 'monthTrend': top5, 'hiddenGem': hidden})


def generate(request):
    return render(request, 'blog/generate.html', {'title': 'Generate Menu'})


def search_list(request):

    query = request.GET.get('q')
    if query:
        recipe_list = Recipe.objects.filter(
            Q(keyword__icontains=query) |
            Q(cuisines__icontains=query) |
            Q(name__icontains=query)
        ).distinct()
    else:
        recipe_list = Recipe.objects.all()

    #paginator = Paginator(recipe_list, 4)  # Show 25 contacts per page.
    #page = request.GET.get('page')
    #try:
        #recipe = paginator.page(page)
    #except PageNotAnInteger:
        #recipe = paginator.page(1)
    #except EmptyPage:
        #recipe = paginator.page(paginator.num_pages)

    context = {
        'recipes': recipe_list,
    }

    return render(request, 'blog/search.html', context)




def recipe_detail(request, slug):
    ob = Recipe.objects.get(recipe_id=slug)
    string = ob.ingredient
    #string = string.replace("'", "").replace("]", "").replace("[", "")

    ingredient = [string.strip().split(' ') for string in string]

    recipe = get_object_or_404(Recipe, recipe_id=slug)
    context = {
        'recipe': recipe,
        'ingredient': ingredient,
    }
    return render(request, 'blog/recipe_detail.html', context)


class RecipeListView(ListView):
    model = Recipe
    template_name = 'blog/search.html'
