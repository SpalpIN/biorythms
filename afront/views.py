from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import TemplateView, FormView, UpdateView
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import logout, login
from .models import Human, BiorythmsModel
from .forms import UserCreationForm, HumanForm, BiorythmsForm

import datetime
from math import sin, pi


# Create your views here.

def start(request):
    context = {}
    return render(request, 'main.html', context)


def info(request):
    context = {
        'name': request.user.username,
        'surname': "Moskalenko"
    }
    return render(request, 'biorythms.html', context)


def physics(request):
    return HttpResponse('yes')


class Bioresult(TemplateView):

    def get(self, request):

        try:
            person = Human.objects.get(email=request.user.email)
            peid = person.id
            model = BiorythmsModel.objects.get(person=peid)
            birthday = model.birth_date
        except ObjectDoesNotExist:
            model = ''
            birthday = ''
        today = datetime.date.today().strftime("%Y-%m-%d")
        chek = True
        ctx = {
            'today': today,
            'birthday': birthday,
            'phys': model.phys,
            'mind': model.mind,
            'intel': model.intel,
            'chek': chek,
        }

        return render(request, 'bioresult.html', ctx)

    def post(self, request):

        mestitle, mes, advice = '', '', ''
        try:
            person = Human.objects.get(email=request.user.email)
            peid = person.id
            model = BiorythmsModel.objects.get(person=peid)
            birthday = model.birth_date
        except ObjectDoesNotExist:
            model = ''
            birthday = ''
        today = datetime.date.today().strftime("%Y-%m-%d")
        chek = True
        ctx = {
            'today': today,
            'birthday': birthday,
            'phys': model.phys,
            'mind': model.mind,
            'intel': model.intel,
            'chek': chek,
        }
        if 'phys' in request.POST:
            res = request.POST['phys']
            if ctx['phys'] < 0:
                mestitle = 'Отрицательная фаза физического биоритма'
                mes = 'В отрицательной фазе физического биоритма вы чувствуете полный упадок физических сил. Работа, какой бы легкой она ни была, утомляет. Пониженный физический тонус, быстрая утомляемость, некоторое снижение сопротивляемости организма к заболеваниям. Ваше физическое состояние оставляет желать лучшего. После обеда на работе вас одолевает сонливость и вы не столько работаете, сколько боретесь со сном.'
                advice = 'Не слишком благоприятный период для активной физической деятельности. Советуем больше спать, пить минимум 1,5л. воды в день, не забывать про фрукты и овощи, все это придаст необходимых сил!'

            elif ctx['phys'] == 0:
                mestitle = 'Критический день физического биоритма!'
                mes = 'Критические дни физического биоритма обычно проявляются в резкой перемене самочувствия. Нестабильность физического состояния. Существует вероятность травм, аварий, обострений хронических заболеваний, головной боли. Проявляя физическуя активность мы не обращаем внимания на появившиеся болевые ощущения и дискомфорт. Между тем, это — сигналы о неблагополучии, чреватом риском получения серьезной травмы.'
                advice = 'Опасный день физического биоритма характеризующиеся упадком жизненных сил, советуем быть крайне осторожным в сферах физической деятельности. Не перетруждайтесь('
            elif ctx['phys'] == 100:
                mestitle = 'Пик физического биоритма!'
                mes = 'Положительная фаза физического биоритма — благоприятный период для занятий, связанных с физической нагрузкой.  Максимальная энергия, сила, выносливость, наивысшая устойчивость к воздействию экстремальных факторов. Вы бодры, энергичны и ваша физическая активность высока. Просыпаясь, вы ощущаете прилив сил и чувствуете себя превосходно. На работе вы проявляете чудеса ловкости и выносливости.'
                advice = 'Ваш физический пик, поздравляем! Сегодня тот самый день для начала любого вида физической деятельности. Больше никаких потом, за дело!'

            else:
                mestitle = 'Положительная фаза физического биоритма!'
                mes = 'Положительная фаза физического биоритма — благоприятный период для занятий, связанных с физической нагрузкой.  Максимальная энергия, сила, выносливость, наивысшая устойчивость к воздействию экстремальных факторов. Вы бодры, энергичны и ваша физическая активность высока. Просыпаясь, вы ощущаете прилив сил и чувствуете себя превосходно. На работе вы проявляете чудеса ловкости и выносливости.'
                advice = 'Да, да, это то самое время для занятия спортом, о котором вы так долго себя уговаривали. То самое время убраться в гараже или просто выйти на прогулку. Используйте свои силы по максимуму!'

        ######################################

        elif 'mind' in request.POST:
            res = request.POST['mind']
            if ctx['mind'] < 0:
                mestitle = 'Отрицательная фаза эмоционального биоритма'
                mes = 'В данной стадии эмоционального биоритма вы станете более раздражительны и чувствительны даже к вещам, которые вас обычно не тревожат. Вас будет одолевать плохое настроение, вы станете менее общительным. Из-за того, что негативные эмоции будут брать верх над разумом вы будете склонны оказываться в неловких ситуациях'
                advice = 'Во время отрицательной стадии эмоционального биоритма не рекомендуется заводить сомнительные знакомства, начинать новые проекты на работе и строить планы на ближайшее время из-за нестабильности вашего состояния. Советуем больше отдыхать и поддерживать правильный образ жизни'
            elif ctx['mind'] == 0:
                mestitle = 'Критическая фаза эмоционального биоритма'
                mes = 'В критические дни эмоционального биоритма вы склонны к неуместным шуткам и резким замечаниям. В связи с этим вызвано угнетенное состояние, ссоры, эмоциональная неустойчивость, сниженная реакция. Малейшие замечания в вашу сторону вызывают встречную агрессию.'
                advice = 'Критическая фаза характеризуется иррациональностью эмоционального поведения: Не вступать в конфликты, обходить ссоры, смотреть на проблему с разных сторон. В рабочих моментах не стоит договариться о дополнительных заданиях или отпуске. Советуем больше отдыха и придерживаться спокойному времяпровождению.'

            elif ctx['mind'] == 100:
                mestitle = 'Пик эмоционального биоритма!'
                mes = 'Положительная фаза физического биоритма — благоприятный период для занятий, связанных с физической нагрузкой.  Максимальная энергия, сила, выносливость, наивысшая устойчивость к воздействию экстремальных факторов. Вы бодры, энергичны и ваша физическая активность высока. Просыпаясь, вы ощущаете прилив сил и чувствуете себя превосходно. На работе вы проявляете чудеса ловкости и выносливости.'
                advice = 'Ваш эмоциональный пик, поздравляем! Сегодня прекрасный день, чтобы побыть с любой половинкой, друзьями, семьей. Наслаждайтесь временем с дорогими для вас людьми'

            else:
                mestitle = 'Положительная фаза эмоционального биоритма'
                mes = 'В положительной фазе эмоционального биоритма вы испытываете отличное настроение и наполнены энтузиазмом. Вам легко дается под контроль ваше эмоциональное состояние и блокирование внешнего психологического давления. Поскольку вы чувствуете себя окрыленным, вы становитесь открыты для общения. Так же ваш задор и энтузиазм будет передаваться партнерам, если речь будет идти о новом крупном деле.'
                advice = 'Прекрасное время для свершений запланированных целей, для новых знакомств. Вы находитесь в прекрасном эмоциональном состоянии и заражаете этим окружающих, так что самое время провести время с близкими вам людьми. Так же Ваши коллеги и партеры могут перейнять энтузиазм и дела пойдут вверх '

        # ####################################

        elif 'intel' in request.POST:
            res = request.POST['intel']
            if ctx['intel'] < 0:
                mestitle = 'Отрицательная фаза интеллектуального биоритма'
                mes = 'В негативной фазе интеллектуального биоритма процесс мышления вялый, прерывистый, восприятие тускнеет, заметно отсутствие концентрации. Ваша умственная деятельность замедляется. '
                advice = 'В такие дни стоит воздержаться от сложных операций на работе и быту. Так же не стоит начинать новые проекты. Стоит активно следить за образом жизни: сон, питание, водный баланс.'

            elif ctx['intel'] == 0:
                mestitle = 'Критический день интеллектуального биоритма!'
                mes = ' Мыслительные способности сыграют с вами злую шутку. Будет снижено внимание, появятся ошибочные умозаключения и будет наблюдаться ухудшение памяти'
                advice = 'Фаза характеризуется снижением способности к восприятию. Сегодня садиться за руль автомобиля необходимо с большой осторожностью! В эти дни лучше воздержаться от принятия ответственных решений на вашей работе и дома. Не стоит зацикливаться на решении различных задачи, даже если они вам кажутся совершенно легкими. Отдыхайте и помните о вашем здоровье.'

            elif ctx['intel'] == 100:
                mestitle = 'Пик интеллектуального биоритма!'
                mes = 'Положительная фаза физического биоритма — благоприятный период для занятий, связанных с физической нагрузкой.  Максимальная энергия, сила, выносливость, наивысшая устойчивость к воздействию экстремальных факторов. Вы бодры, энергичны и ваша физическая активность высока. Просыпаясь, вы ощущаете прилив сил и чувствуете себя превосходно. На работе вы проявляете чудеса ловкости и выносливости.'
                advice = 'Ваш интеллектуальный пик, поздравляем! Сегодня ваши умственные способности на высоте. Давно хотели разобраться с чем-то новым? Освоить новую программу? Научиться монтировать видеоролики? Сегодня прекрасный для этого день - за дело'

            else:
                mestitle = 'Положительная фаза интеллектуального биоритма!'
                mes = ' В положительной фазе интеллектуального биоритма вами руководит здравый смысл. Вы чувствуете себя в прекрасной творческой форме. Интеллектуальное состояние достигает наивысшего уровня, простые задачи решаются легко и без раздумий.'
                advice = 'В данной фазе рекомендуется выполнять все те задачи, отложенные на потом. «Потом» наступило! Решайте сложные задачи на работе, начните новый проэкт, разберитесь со счетами, посоветуйте друзьям, помогите детям. Сейчас самое время проявить себя.'

        ctx['mestitle'], ctx['mes'], ctx['advice'] = mestitle, mes, advice
        return render(request, 'bioresult.html', ctx)


class Biorhythms(TemplateView):

    def get(self, request):
        form = BiorythmsForm
        try:
            person = Human.objects.get(email=request.user.email)
            peid = person.id
            model = BiorythmsModel.objects.get(person=peid)
            birthday = model.birth_date
        except ObjectDoesNotExist:
            birthday = ''
        today = datetime.date.today().strftime("%Y-%m-%d")
        ctx = {
            'form': form,
            'today': today,
            'birthday': birthday
        }
        return render(request, 'biorythms.html', ctx)

    def post(self, request):
        a1, b1 = request.POST['curentday'], request.POST['birthday']
        a = a1.split('-')
        if len(b1)<8 or len(b1)>10:
            return HttpResponse('Введите коректные данные!')
        if '.' or ',' or '/' or '_' in b1:
            b1 = b1.replace(".", "-")
            b1 = b1.replace(",", "-")
            b1 = b1.replace("/", "-")
            b1 = b1.replace("_", "-")
        b = b1.split('-')
        try:
            if int(b[0]) < 32:
                b[0], b[2] = b[2], b[0]
                if int(b[0]) < 100:
                    b[0] = str(int(b[0]) + 1900)
                b1 = '-'.join(b)
        except ValueError:
            return HttpResponse('Введите коректные данные!')

        try:
            person = Human.objects.get(email=request.user.email)
            peid = person.id
            mod = BiorythmsModel(birth_date=b1, person_id=peid, calculate_date=a1)
            mod.save()
        except ObjectDoesNotExist:
            er = 'Для расчета биоритмов необходимо внести персональные данные в личном кабинете, '
            ctx = {'er': er}
            return render(request, 'biorythms.html', ctx)
        except IntegrityError:
            pass
        model = BiorythmsModel.objects.get(person=peid)
        aa = datetime.date(int(a[0]), int(a[1]), int(a[2]))
        bb=''
        try:
            bb = datetime.date(int(b[0]), int(b[1]), int(b[2]))
        except ValueError:
            return HttpResponse('Введите коректные данные!')
        except IndexError:
            return HttpResponse('Введите коректные данные!')
        dd = str(aa - bb)
        days = int(dd.split()[0])
        p = {'phys': 23,
             'mind': 28,
             'intel': 33}
        bio = (sin((2 * pi * days) / p['phys']))
        chek = True
        model.phys = round((sin((2 * pi * days) / p['phys']) * 100), 2)
        model.mind = round((sin((2 * pi * days) / p['mind']) * 100), 2)
        model.intel = round((sin((2 * pi * days) / p['intel']) * 100), 2)
        model.birth_date = b1
        model.save()
        ctx = {'phys': model.phys,
               'mind': model.mind,
               'intel': model.intel,
               'today': a1,
               'birthday': b1,
               'chek': chek
               }
        return render(request, 'biorythms.html', ctx)


class Reduct(TemplateView):
    template_name = 'reduct.html'

    def get(self, request):
        if request.user.is_authenticated:
            all_users = Human.objects.all()
            ctx = {'all_users': all_users}
            return render(request, self.template_name, ctx)
        else:
            return render(request, self.template_name, {})

    def post(self, request):
        col = request.POST['delete']
        Human.objects.filter(id=col).delete()
        return redirect('reduct/')


class Ivent(TemplateView):
    template_name = 'ivent.html'

    def get(self, request):
        if request.user.is_authenticated:
            all_employees = Human.objects.all()
            # biorythms = BiorythmsModel.objects.all()
            ctx = {'all_employees': all_employees,
                   # 'biorythms' : biorythms
                   }
            return render(request, self.template_name, ctx)
        else:
            return render(request, self.template_name, {})


def account_form(request):
    form_for_human = HumanForm
    ctx = {
        'form_for_human': form_for_human
    }
    return render(request, 'changePersonalData.html', ctx)


class Account(TemplateView):
    template_name = 'account.html'

    def get(self, request):
        our_user = Human.objects.filter(email=request.user.email)
        ctx = {
            'our_user': our_user,
        }
        return render(request, self.template_name, ctx)

    def post(self, request):
        form = HumanForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('account/')
        else:
            return HttpResponse(form.errors.as_text())


class ChangeAccData(UpdateView):

    def get(self, request):
        form = HumanForm
        model = Human.objects.filter(email=request.user.email)
        ctx = {
            'form': form,
            'model': model
        }
        return render(request, 'changeAccData.html', ctx)

    def post(self, request):
        form = HumanForm(request.POST)
        if form.is_valid():
            our_user = Human.objects.filter(email=request.user.email)
            our_user.delete()
            form.save()
            return redirect('account/')
        else:
            return HttpResponse(form.errors.as_text())


class RegisterForm(FormView):
    form_class = UserCreationForm
    success_url = '/auth'
    template_name = 'register.html'

    def form_valid(self, form):
        form.save()
        return super(RegisterForm, self).form_valid(form)

    def form_invalid(self, form):
        return super(RegisterForm, self).form_invalid(form)


class AuthForm(FormView):
    form_class = AuthenticationForm
    template_name = 'auth.html'
    success_url = '/main'

    def form_valid(self, form):
        self.user = form.get_user()
        login(self.request, self.user)
        return super(AuthForm, self).form_valid(form)

    def form_invalid(self, form):
        msg = 'Please enter a correct username and password. Note that both fields may be case-sensitive.'
        return HttpResponse(form.errors.as_text())


class LogoutForm(FormView):
    def get(self, request):
        logout(request)
        return HttpResponseRedirect('/main')
