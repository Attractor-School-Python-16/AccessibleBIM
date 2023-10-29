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
