from django.contrib import admin
from .models import Tutorial, Lecon, Quiz, Question, Reponse, ProgressionUtilisateur

class QuestionInline(admin.TabularInline):
    model = Question
    extra = 1
    show_change_link = True

class ReponseInline(admin.TabularInline):
    model = Reponse
    extra = 3
    max_num = 6

class LeconInline(admin.TabularInline):
    model = Lecon
    extra = 1
    show_change_link = True

@admin.register(Tutorial)
class TutorialAdmin(admin.ModelAdmin):
    list_display = ('titre', 'created_at', 'nombre_lecons')
    list_filter = ('created_at',)
    search_fields = ('titre', 'description')
    inlines = [LeconInline]
    
    def nombre_lecons(self, obj):
        return obj.lecons.count()
    nombre_lecons.short_description = 'Nombre de leçons'

@admin.register(Lecon)
class LeconAdmin(admin.ModelAdmin):
    list_display = ('titre', 'tutorial', 'ordre', 'duree')
    list_filter = ('tutorial',)
    search_fields = ('titre', 'texte_explicatif')
    ordering = ('tutorial', 'ordre')

@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ('titre', 'lecon', 'pass_mark')
    list_filter = ('lecon__tutorial',)
    inlines = [QuestionInline]
    search_fields = ('titre', 'description')

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('question_text', 'quiz', 'type_question', 'ordre')
    list_filter = ('quiz', 'type_question')
    ordering = ('quiz', 'ordre')
    inlines = [ReponseInline]
    search_fields = ('question_text',)

@admin.register(ProgressionUtilisateur)
class ProgressionUtilisateurAdmin(admin.ModelAdmin):
    list_display = ('utilisateur', 'tutorial', 'lecon', 'est_completee', 'score_quiz')
    list_filter = ('est_completee', 'tutorial', 'utilisateur')
    search_fields = ('utilisateur__username', 'lecon__titre')
    readonly_fields = ('date_completion',)
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related(
            'utilisateur', 'tutorial', 'lecon'
        )