from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from .models import Article, Category

def article_list(request):
    query = request.GET.get('q', '').strip()
    articles = Article.objects.filter(is_published=True)
    
    if query:
        articles = articles.filter(
            Q(title__icontains=query) | 
            Q(content__icontains=query) | 
            Q(summary__icontains=query)
        )
        
    categories = Category.objects.all()
    return render(request, 'news/article_list.html', {
        'articles': articles,
        'categories': categories,
        'query': query,
    })

def article_detail(request, pk):
    article = get_object_or_404(Article, pk=pk, is_published=True)
    return render(request, 'news/article_detail.html', {'article': article})

def category_articles(request, slug):
    category = get_object_or_404(Category, slug=slug)
    articles = Article.objects.filter(category=category, is_published=True)
    return render(request, 'news/category_articles.html', {
        'category': category,
        'articles': articles,
    })
from django.shortcuts import render
from .models import Article

def index(request):
    articles = Article.objects.all().order_by('-created_at') if hasattr(Article, 'created_at') else Article.objects.all()
    # Change 'news/index.html' to match your actual file name (e.g., 'index.html' or 'home.html')
    return render(request, 'index.html', {'articles': articles})