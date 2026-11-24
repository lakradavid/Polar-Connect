from django.contrib import admin
from .models import LearningCategory, LearningModule, Quiz, Question, QuizAttempt, LearningProgress


@admin.register(LearningCategory)
class LearningCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'order']
    prepopulated_fields = {'slug': ('name',)}


class QuestionInline(admin.TabularInline):
    model = Question
    extra = 4


@admin.register(LearningModule)
class LearningModuleAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'difficulty', 'duration_minutes', 'is_published', 'order']
    list_filter = ['category', 'difficulty', 'is_published']
    prepopulated_fields = {'slug': ('title',)}
    list_editable = ['is_published', 'order']


@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ['title', 'module', 'passing_score', 'time_limit_minutes']
    inlines = [QuestionInline]


@admin.register(QuizAttempt)
class QuizAttemptAdmin(admin.ModelAdmin):
    list_display = ['user', 'quiz', 'score', 'percentage', 'passed', 'attempted_at']
    list_filter = ['passed', 'quiz']


@admin.register(LearningProgress)
class LearningProgressAdmin(admin.ModelAdmin):
    list_display = ['user', 'module', 'completed', 'completed_at']
