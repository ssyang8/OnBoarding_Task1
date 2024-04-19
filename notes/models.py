from django.db import models


class Article(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()

    def __str__(self):
        return self.title


class PlainNote(models.Model):
    article = models.ForeignKey(
        Article, on_delete=models.CASCADE, related_name='plain_notes')
    text = models.TextField()

    def __str__(self):
        return self.text[:50]


class HighlightedNote(models.Model):
    article = models.ForeignKey(
        Article, on_delete=models.CASCADE, related_name='highlighted_notes')
    selected_text = models.TextField()
    note_text = models.TextField()
    start_position = models.IntegerField(default=0)
    end_position = models.IntegerField(default=0)

    def __str__(self):
        return f"'{self.selected_text}': '{self.note_text}'"
