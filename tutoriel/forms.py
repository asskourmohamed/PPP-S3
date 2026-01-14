from django import forms
from .models import Question, Reponse

class QuizForm(forms.Form):
    def __init__(self, quiz, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.quiz = quiz
        
        # Créer un champ pour chaque question
        for question in quiz.questions.all().order_by('ordre'):
            if question.type_question == 'CHOIX_MULTIPLE':
                choices = [(r.id, r.reponse_text) for r in question.reponses.all()]
                self.fields[f'question_{question.id}'] = forms.MultipleChoiceField(
                    label=question.question_text,
                    choices=choices,
                    widget=forms.CheckboxSelectMultiple,
                    required=False
                )
            elif question.type_question == 'VRAI_FAUX':
                self.fields[f'question_{question.id}'] = forms.ChoiceField(
                    label=question.question_text,
                    choices=[(True, 'Vrai'), (False, 'Faux')],
                    widget=forms.RadioSelect
                )
    
    def calculate_score(self):
        """Calcule le score du quiz"""
        total_questions = self.quiz.questions.count()
        correct_answers = 0
        
        for question in self.quiz.questions.all():
            field_name = f'question_{question.id}'
            user_answer = self.cleaned_data.get(field_name)
            
            if question.type_question == 'CHOIX_MULTIPLE':
                # Pour les choix multiples, vérifier toutes les réponses correctes
                correct_ids = set(r.id for r in question.reponses.filter(est_correcte=True))
                user_ids = set(int(id) for id in user_answer) if user_answer else set()
                if correct_ids == user_ids:
                    correct_answers += 1
                    
            elif question.type_question == 'VRAI_FAUX':
                # Pour vrai/faux
                correct_answer = question.reponses.filter(est_correcte=True).first()
                if correct_answer and str(user_answer) == str(correct_answer.reponse_text == 'Vrai'):
                    correct_answers += 1
        
        return int((correct_answers / total_questions) * 100) if total_questions > 0 else 0