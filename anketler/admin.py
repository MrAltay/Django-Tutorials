from django.contrib import admin

from .models import Choice, Question, Poll


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3


class QuestionInline(admin.TabularInline):
    model = Question
    extra = 1


class PollAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {"fields": ["title"]}),
        ("Date information", {"fields": ["pub_date"], "classes": ["collapse"]}),
    ]
    inlines = [QuestionInline]
    list_display = ["title", "pub_date", "was_published_recently"]
    list_filter = ["pub_date"]
    search_fields = ["title"]


class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {"fields": ["poll", "question_text"]}),
    ]
    inlines = [ChoiceInline]
    list_display = ["question_text", "poll"]
    list_filter = ["poll"]
    search_fields = ["question_text"]


admin.site.register(Poll, PollAdmin)
admin.site.register(Question, QuestionAdmin)
