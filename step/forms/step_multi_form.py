from quiz_bim.forms.quiz_bim_for_step_form import QuizBimForStepForm
from step.forms.file_for_step_form import FileForStepForm
from step.forms.step_form import StepTextForm, StepVideoForm, StepQuizForm
from step.forms.text_for_step_form import TextForStepForm
from step.forms.video_for_step_form import VideoForStepForm
from betterforms.multiform import MultiModelForm


class MultiStepTextForm(MultiModelForm):
    form_classes = {
        'step': StepTextForm,
        'file': FileForStepForm,
        'text': TextForStepForm,
    }


class MultiStepVideoForm(MultiModelForm):
    form_classes = {
        'step': StepVideoForm,
        'file': FileForStepForm,
        'video': VideoForStepForm,
    }


class MultiStepQuizForm(MultiModelForm):
    form_classes = {
        'step': StepQuizForm,
        'quiz': QuizBimForStepForm,
    }

class MultiStepVideoUpdateForm(MultiModelForm):
    form_classes = {
        'step': StepVideoForm,
        'file': FileForStepForm,
    }

class MultiStepTextUpdateForm(MultiModelForm):
    form_classes = {
        'step': StepTextForm,
        'file': FileForStepForm,
    }
