from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import LearningCategory, LearningModule, Quiz, Question, QuizAttempt, LearningProgress


def modules_list(request):
    from education.models import Quiz
    categories = LearningCategory.objects.prefetch_related('modules').all()
    total_modules = sum(c.modules.count() for c in categories)
    total_quizzes = Quiz.objects.count()
    return render(request, 'education/modules.html', {
        'categories': categories,
        'total_modules': total_modules,
        'total_quizzes': total_quizzes,
    })


def category_detail(request, slug):
    category = get_object_or_404(LearningCategory, slug=slug)
    modules = LearningModule.objects.filter(category=category, is_published=True)
    return render(request, 'education/category.html', {'category': category, 'modules': modules})


def module_detail(request, slug):
    module = get_object_or_404(LearningModule, slug=slug, is_published=True)
    completed = False
    if request.user.is_authenticated:
        progress, _ = LearningProgress.objects.get_or_create(user=request.user, module=module)
        if request.method == 'POST' and request.POST.get('mark_complete'):
            progress.completed = True
            progress.completed_at = timezone.now()
            progress.save()
            messages.success(request, 'Module marked as complete!')
            return redirect('education:module', slug=slug)
        completed = progress.completed
    return render(request, 'education/module_detail.html', {'module': module, 'completed': completed})


def quiz_list(request):
    quizzes = Quiz.objects.select_related('module').all()
    return render(request, 'education/quiz_list.html', {'quizzes': quizzes})


@login_required
def quiz_take(request, pk):
    quiz = get_object_or_404(Quiz, pk=pk)
    questions = quiz.questions.all()
    if request.method == 'POST':
        score = 0
        for question in questions:
            answer = request.POST.get(f'q_{question.pk}', '')
            if answer.upper() == question.correct_option:
                score += 1
        total = questions.count()
        pct = (score / total * 100) if total else 0
        passed = pct >= quiz.passing_score
        attempt = QuizAttempt.objects.create(
            user=request.user,
            quiz=quiz,
            score=score,
            total_questions=total,
            percentage=pct,
            passed=passed,
        )
        return redirect('education:quiz_result', pk=attempt.pk)
    return render(request, 'education/quiz_take.html', {'quiz': quiz, 'questions': questions})


@login_required
def quiz_result(request, pk):
    attempt = get_object_or_404(QuizAttempt, pk=pk, user=request.user)
    return render(request, 'education/quiz_result.html', {'attempt': attempt})
