from django.shortcuts import render, redirect, get_object_or_404
from django.shortcuts import render, redirect
from .models import Article, PlainNote, HighlightedNote
from django.http import HttpResponseBadRequest, JsonResponse
from django.shortcuts import redirect, get_object_or_404


def index(request):
    articles = Article.objects.all()
    return render(request, 'index.html', {'articles': articles})


def add_highlighted_note(request, article_id):
    if request.method == 'POST':
        selected_text = request.POST.get('selected_text')
        note_text = request.POST.get('note_text')
        article = get_object_or_404(Article, pk=article_id)

        # Create a new HighlightedNote instance
        HighlightedNote.objects.create(
            article=article,
            selected_text=selected_text,
            note_text=note_text
        )
        return JsonResponse({'success': True})
    return JsonResponse({'success': False}, status=400)


def article_view(request, article_id):
    article = get_object_or_404(Article, pk=article_id)
    if request.method == "POST":
        if 'plain_note' in request.POST:
            text = request.POST.get('plain_note_text')
            PlainNote.objects.create(article=article, text=text)
        elif 'highlighted_note' in request.POST:
            selected_text = request.POST.get('selected_text')
            note_text = request.POST.get('highlighted_note_text')
            HighlightedNote.objects.create(
                article=article, selected_text=selected_text, note_text=note_text)
        return redirect('notes:article_view', article_id=article_id)
    plain_notes = article.plain_notes.all()
    highlighted_notes = article.highlighted_notes.all()
    return render(request, 'article.html', {
        'article': article,
        'plain_notes': plain_notes,
        'highlighted_notes': highlighted_notes
    })


def new_article(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        article = Article.objects.create(title=title, content=content)
        return redirect('notes:article_view', article_id=article.id)
    return render(request, 'new_article.html')


def delete_note(request, note_type, note_id):
    if note_type == 'plain':
        note = get_object_or_404(PlainNote, pk=note_id)
    elif note_type == 'highlighted':
        note = get_object_or_404(HighlightedNote, pk=note_id)
    else:
        return HttpResponseBadRequest("Invalid note type specified")

    article_id = note.article.id
    note.delete()
    return redirect('notes:article_view', article_id=article_id)
