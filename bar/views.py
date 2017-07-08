from django.shortcuts import render
from bar.models import Article


def index(request):
    articles = list(Article.objects.all())
    article = Article.objects.defer('content').get(title='foobar')
    return render(request, 'index.html', {'articles': articles, 'article': article})
