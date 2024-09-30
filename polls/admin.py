from django.contrib import admin
from .models import Question, Choice
from django.core.exceptions import ValidationError
from django.forms import inlineformset_factory

class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3
    
# @admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        ("Question", {"fields": ["question_text"]}),
        ("Date information", {"fields": ["pub_date"]}),
    ]
    inlines = [ChoiceInline]
    list_display = ["question_text", "pub_date", "was_published_recently"]
    list_filter = ["pub_date"]
    search_fields = ["question_text"]
    
    def save_model(self, request, obj, form, change):
        super().save_model(request,obj,form,change)
    
    def save_related(self, request, form, formsets, change):
        super().save_related(request,form, formsets, change)
        choice_count=Choice.objects.filter(question=form.instance).count()
        if choice_count<2:
            raise ValidationError("Each question must have Atleast two choices")

admin.site.register(Question, QuestionAdmin)