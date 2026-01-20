from django.contrib import admin
from .models import Question, Choice

# Register your models here.
class ChoiceAdmin(admin.TabularInline):
    model = Choice
    extra = 3

class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
            (None, {"fields":["question_text"]}),
            ("Date Info", {"fields":["pub_time"], "classes":["collapse"]}),
            ]
    inlines = [ChoiceAdmin]
    list_display = ["question_text", "pub_time", "was_published_today"]
    list_filter = ["pub_time"]
    search_fields = ["question_text"]

admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice)
