from django.contrib import admin
from .models import Quiz, Question, Choice, Submission, User

class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3

class QuestionAdmin(admin.ModelAdmin):
    inlines = [ChoiceInline]

class QuizAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'creator', 'created_at', 'time_limit')
    list_filter = ('creator', 'created_at')
    search_fields = ['title', 'creator__username']

class SubmissionAdmin(admin.ModelAdmin):
    list_display = ('user', 'quiz', 'score', 'submitted_at', 'time_taken')
    list_filter = ('quiz', 'submitted_at', 'user')
    search_fields = ['quiz__title', 'user__username']

class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_admin')
    list_filter = ('is_admin',)
    search_fields = ('username', 'email')

admin.site.register(User, UserAdmin)
admin.site.register(Quiz, QuizAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice)
admin.site.register(Submission, SubmissionAdmin)
