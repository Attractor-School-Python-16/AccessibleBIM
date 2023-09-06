from django.contrib import admin

from modules.models.chapter import ChapterModel
from modules.models.course_target import CourseTargetModel
from modules.models.courses import CourseModel
from modules.models.modules import ModuleModel
from modules.models.teacher import TeacherModel

# Register your models here.
admin.site.register(ChapterModel)
admin.site.register(CourseTargetModel)
admin.site.register(CourseModel)
admin.site.register(ModuleModel)
admin.site.register(TeacherModel)
