from django.shortcuts import render, redirect, get_object_or_404
from django.shortcuts import render, redirect
from .models import Article, PlainNote, HighlightedNote
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseRedirect, JsonResponse
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
        return redirect('notes:index')
    return render(request, 'new_article.html')


def edit_plain_note(request, note_id):
    note = get_object_or_404(PlainNote, pk=note_id)
    # Retrieve the 'next' parameter from the URL, or default to 'notes:index' if not provided
    next_url = request.GET.get('next', 'notes:index')

    if request.method == 'POST':
        note.text = request.POST.get('text')
        note.save()
        # Redirect to the 'next' URL after saving changes
        return redirect(next_url)

    return render(request, 'edit_plain_note.html', {'note': note, 'next': next_url})


def edit_highlighted_note(request, note_id):
    note = get_object_or_404(HighlightedNote, pk=note_id)
    next_url = request.GET.get('next', 'notes:index')

    if request.method == 'POST':
        # note.selected_text = request.POST.get('selected_text')
        note.note_text = request.POST.get('note_text')
        # note.start_position = int(request.POST.get('start_position', 0))
        # note.end_position = int(request.POST.get('end_position', 0))
        note.save()
        return redirect(next_url)  # Adjust the redirect as needed
    return render(request, 'edit_highlighted_note.html', {'note': note})


# Ensure this view only handles POST requests to avoid accidental deletions

def delete_note(request, note_id):
    # Determine the type based on model or pass the type as parameter
    # Example assumes type is known and passed via URL or determined somehow
    try:
        note = get_object_or_404(PlainNote, pk=note_id)
        note_type = 'plain'
    except PlainNote.DoesNotExist:
        note = get_object_or_404(HighlightedNote, pk=note_id)
        note_type = 'highlighted'

    if request.method == 'POST':
        article_id = note.article.id  # Store the article ID before deleting
        note.delete()
        next_url = request.POST.get(
            'next', 'notes:index')  # Default redirection
        return HttpResponseRedirect(next_url)

    # if not POST method, maybe display a confirmation page or handle differently
    return HttpResponseBadRequest("Invalid request")


def delete_highlighted_note(request, note_id):
    # Determine the type based on model or pass the type as parameter
    # Example assumes type is known and passed via URL or determined somehow
    try:
        note = get_object_or_404(HighlightedNote, pk=note_id)
        note_type = 'highlighted'
    except HighlightedNote.DoesNotExist:
        note = get_object_or_404(PlainNote, pk=note_id)
        note_type = 'plain'

    if request.method == 'POST':
        article_id = note.article.id  # Store the article ID before deleting
        note.delete()
        next_url = request.POST.get(
            'next', 'notes:index')  # Default redirection
        return HttpResponseRedirect(next_url)

    # if not POST method, maybe display a confirmation page or handle differently
    return HttpResponseBadRequest("Invalid request")
