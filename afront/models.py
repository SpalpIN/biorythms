from django.db import models


# Create your models here.

class Human(models.Model):
    # person = models.ForeignKey(User,on_delete=models.CASCADE)
    name = models.CharField(max_length=50, verbose_name='Имя')
    surname = models.CharField(max_length=50, verbose_name='Фамилия')
    email = models.EmailField(max_length=50)
    phone = models.PositiveSmallIntegerField()
    age = models.PositiveSmallIntegerField()
    genders = (
        ('мужской', 'мужской'),
        ('женский', 'женский'),
    )
    gender = models.CharField(max_length=10, choices=genders)
    height = models.PositiveSmallIntegerField()
    weight = models.PositiveSmallIntegerField()

    def __str__(self):
        return '{} {}'.format(self.name, self.surname)
    hronoType = models.CharField(max_length=30)


class BiorythmsModel(models.Model):
    person = models.OneToOneField(Human, on_delete=models.CASCADE)
    birth_date = models.CharField(max_length=10)
    calculate_date = models.CharField(max_length=10)
    phys = models.FloatField(default=0)
    mind = models.FloatField(default=0)
    intel = models.FloatField(default=0)
