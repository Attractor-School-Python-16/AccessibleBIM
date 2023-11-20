from quiz_bim.forms.quiz_bim_form import QuizBimForm
from step.forms.file_for_step_form import FileForStepForm
from step.forms.file_form import FileForm
from step.forms.step_form import StepTextForm, StepVideoForm, StepQuizForm
from step.forms.text_form import TextForm
from step.forms.video_form import VideoForm
from betterforms.multiform import MultiModelForm


class MultiStepTextForm(MultiModelForm):
    form_classes = {
        'step': StepTextForm,
        'file': FileForStepForm,
        'text': TextForm,
    }


class MultiStepVideoForm(MultiModelForm):
    form_classes = {
        'step': StepVideoForm,
        'file': FileForStepForm,
        'video': VideoForm,
    }


class MultiStepQuizForm(MultiModelForm):
    form_classes = {
        'step': StepQuizForm,
        'quiz': QuizBimForm,
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
