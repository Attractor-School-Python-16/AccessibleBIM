import factory


class ModuleFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'modules.ModuleModel'

    title = factory.sequence(lambda n: f"Module {n}")
    description = factory.Faker('sentence', nb_words=10)
    image = factory.django.ImageField(filename='image.jpg')


class CourseTargetFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'modules.CourseTargetModel'

    title = factory.sequence(lambda n: f"Target {n}")
    description = factory.Faker('sentence', nb_words=10)


class CourseFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'modules.CourseModel'

    title = factory.sequence(lambda n: f"Course {n}")
    description = factory.Faker('sentence', nb_words=10)
    image = factory.django.ImageField(filename='image.jpg')
    module_id = factory.SubFactory(ModuleFactory)
    courseTarget_id = factory.SubFactory(CourseTargetFactory)
    language = factory.Faker('random_element', elements=['RU', 'EN', 'KG'])
    learnTime = factory.Faker('random_int', min=0, max=100)


class ChapterFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'modules.ChapterModel'

    course = factory.SubFactory(CourseFactory)
    title = factory.sequence(lambda n: f"Chapter {n}")
    description = factory.Faker('sentence', nb_words=10)
