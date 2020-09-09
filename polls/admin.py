from django.contrib import admin
from .models import Question, Choice, UserProfileImg, UserRole


# Register your models here.


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3


class QuestionAdmin(admin.ModelAdmin):
    # fields = ['pub_date','question_text']
    search_fields = ['question_text']
    list_display = ('question_text', 'pub_date', 'was_recently_published')
    list_filter = ['pub_date']
    fieldsets = [
        ('The Question', {'fields': ['question_text']}),
        ('Date inforamtion', {'fields': ['pub_date'], 'classes': ['collapse']}),
    ]

    inlines = [ChoiceInline]


admin.site.register(Question, QuestionAdmin)
admin.site.register(UserProfileImg)
admin.site.register(UserRole)
