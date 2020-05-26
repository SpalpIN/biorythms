from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.utils.datastructures import MultiValueDictKeyError
from django.views.generic import TemplateView, FormView, UpdateView
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import logout, login
from .models import Human, BiorythmsModel, AtmosphericPressure
from .forms import UserCreationForm, HumanForm, BiorythmsForm, AtmosphericPressureForm
from django.contrib import messages

from bs4 import BeautifulSoup
import requests
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
        try:
            today = model.calculate_date
        except ObjectDoesNotExist:
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
        try:
            today = model.calculate_date
        except ObjectDoesNotExist:
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
        if len(b1) < 6 or len(b1) > 10:
            return HttpResponse('Введите коректные данные!')
        delim = {'.', ',', '/', '_', '!', '#', '$', '%', '&', '*', ';', ':', '?', '|', '~', ' '}

        try:
            int(b1)
            b2 = list(b1)
            if len(b2) == 8:
                b1 = '{}{}-{}{}-{}{}{}{}'.format(b2[0], b2[1], b2[2], b2[3], b2[4], b2[5], b2[6], b2[7])
            elif len(b2) == 6:
                b1 = '{}{}-{}{}-{}{}'.format(b2[0], b2[1], b2[2], b2[3], b2[4], b2[5])
            else:
                return HttpResponse('Введите коректные данные!')
        except ValueError:
            pass
        for i in delim:
            if i in b1:
                b1 = b1.replace(i, "-")
        b = b1.split('-')
        try:
            if int(b[0]) < 32:
                b[0], b[2] = b[2], b[0]
                if int(b[0]) < 100:
                    b[0] = str(int(b[0]) + 1900)
            if int(b[1]) > 12:
                b[1], b[2] = b[2], b[1]
            b1 = '-'.join(b)
        except ValueError:
            return HttpResponse('Введите коректные данные!')
        except IndexError:
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
        aa = ''
        try:
            aa = datetime.date(int(a[0]), int(a[1]), int(a[2]))
        except ValueError:
            return HttpResponse('Введите коректные данные!')
        bb = ''
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
        # bio = (sin((2 * pi * days) / p['phys']))
        chek = True
        model.phys = round((sin((2 * pi * days) / p['phys']) * 100), 2)
        model.mind = round((sin((2 * pi * days) / p['mind']) * 100), 2)
        model.intel = round((sin((2 * pi * days) / p['intel']) * 100), 2)
        model.birth_date = b1
        model.calculate_date = a1
        # model.save()
        model.save(update_fields=['phys', 'mind', 'intel', 'birth_date', 'calculate_date'])
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
            # mod = BiorythmsModel.objects.all()
            # bio = list(mod)
            ctx = {'all_employees': all_employees,
                   # 'bio':bio,
                   }
            return render(request, self.template_name, ctx)
        else:
            return render(request, self.template_name, {})


class CircadeRythm(TemplateView):
    template_name = 'circade.html'

    def get(self, request):
        if request.user.is_authenticated:
            our_user = Human.objects.filter(email=request.user.email)
            try:
                model = Human.objects.get(email=request.user.email)
            except ObjectDoesNotExist:
                er = 'Для расчета хронотипа необходимо внести персональные данные в личном кабинете, '
                ctx = {'er': er}
                return render(request, 'biorythms.html', ctx)
            yar, sov, gol = False, False, False
            if 'Сова' in model.hronoType:
                sov = True
                artic = 'Вы - «сова». Ваши биологические часы идут медленнее, чем астрономические. Соответственно, Вам трудно заснуть вечером и трудно проснуться утром. «Совы» — люди, у которых наблюдается отставание фазы сна. Установлено, что лица вечернего типа легче приспосабливаются к работе в ночную смену и трехсменному труду. Совы лучше контролируют ритм сон-бодрствование по сравнению с другими людьми. Они предпочитают ложиться спать позже 23—24 часов, но зато им тяжелее вставать в ранние утренние часы. Они с удовольствием работают по ночам и выбирают такие профессии, чтобы не вставать слишком рано, а еще лучше — самим планировать свой рабочий график.'
            elif 'Жаворонок' in model.hronoType:
                yar = True
                artic = 'Вы - «жаворонок». Ваши биологические часы идут быстрее, чем астрономические. Соответственно, Вы раньше ложитесь спать и раньше встаете. «Жаворонки» — люди, у которых циркадный ритм сдвигается вперед, то есть имеющие синдром опережающей фазы сна. У них период колебания околосуточных ритмов меньше 24 часов. Люди «жаворонки» спят столько же времени, сколько остальные, но их ритм отхода ко сну сдвинут на более ранний вечер. Они рано хотят спать, быстро засыпают и очень рано встают в одни и те же утренние часы. Лучше всего им работается утром на «свежую голову», а к концу дня их работоспособность снижается. Вечерние и третьи смены не для «жаворонков», они с трудом переносят ночные дежурства, клубы и дискотеки.'
            elif 'Голубь' in model.hronoType:
                gol = True
                artic = 'Вы - «голубь». Ваши биологические часы идут приблизительно так же, как и астрономические. Это наиболее благоприятный тип суточного ритма, при котором не возникает проблем как с отходом косну, так и с подъемом. «Голуби» — люди дневного типа. Их циркадный ритм наиболее приспособлен к обычной смене дня и ночи. Период их наилучшей умственной и физической активности отмечается с 10 до 18 часов. Они лучше адаптированы к смене света и темноты. Но даже у них при переездах на большие расстояния со сменой часовых поясов и ночной работе наблюдается сбой собственных биологических часов. Например, при 3-часовой разнице во времени у них возникает бессонница ночью, сонливость и усталость днем, снижение работоспособности.'
            else:
                artic = ''

            ctx = {'our_user': our_user, 'artic': artic,
                   'yar': yar, 'sov': sov, 'gol': gol}
            return render(request, self.template_name, ctx)
        else:
            return render(request, 'main.html', {})


class HronoTest(TemplateView):
    template_name = 'hronoTest.html'

    def get(self, request):
        return render(request, self.template_name, {})

    def post(self, request):
        res = 0
        try:
            for i in range(1, 24):
                res += int(request.POST[str(i)])
        except MultiValueDictKeyError:
            return HttpResponse('Необходимо ответить на все вопросы')
        our_user = Human.objects.get(email=request.user.email)
        if res < 41:
            our_user.hronoType = 'Четко выраженая Сова'
        elif 42 <= res <= 57:
            our_user.hronoType = 'Слабо выраженая Сова'
        elif 58 <= res <= 76:
            our_user.hronoType = 'Голубь'
        elif 77 <= res <= 91:
            our_user.hronoType = 'Слабо выраженый Жаворонок'
        else:
            our_user.hronoType = 'Четко выраженый Жаворонок'
        our_user.save(update_fields=['hronoType'])
        return redirect('circad/')


def account_form(request):
    form_for_human = HumanForm
    ctx = {
        'form_for_human': form_for_human
    }
    return render(request, 'changePersonalData.html', ctx)


def imt(our_us):
    try:
        person = Human.objects.get(email=our_us)
    except ObjectDoesNotExist:
        return False
    return round(person.weight / ((person.height / 100) * (person.height / 100)), 1)


def imtMSG(our_us, masindex):
    status = ''
    color = ''
    try:
        person = Human.objects.get(email=our_us)
    except ObjectDoesNotExist:
        return ['', '']
    if person.age < 26:
        if masindex < 17.5:
            status = ' - Недостаточен, опасно для здоровья'
            color = '#e23b42'
        elif 17.5 <= masindex <= 19.4:
            status = ' - Слегка снижен, неопасно для здоровья'
            color = '#00e211'
        elif 19.5 <= masindex <= 22.9:
            status = ' - Нормальный'
            color = '#007bff'
        elif 23 <= masindex <= 27.4:
            status = ' - Излишний'
            color = '#e8b300'
        elif 27.5 <= masindex <= 29.9:
            status = ' - Ожирение 1 степени'
            color = '#e87e0c'
        elif 30 <= masindex <= 34.9:
            status = ' - Ожирение 2 степени'
            color = '#e8490e'
        elif 35 <= masindex <= 39.9:
            status = ' - Ожирение 3 степени'
            color = '#e80b0d'
        elif 40 <= masindex:
            status = ' - Ожирение 4 степени'
            color = '#c00000'
    else:
        if masindex < 18:
            status = ' - Недостаточен, опасно для здоровья'
            color = '#e23b42'
        elif 18 <= masindex <= 19.9:
            status = ' - Слегка снижен, неопасно для здоровья'
            color = '#00e211'
        elif 20 <= masindex <= 25.9:
            status = ' - Нормальный'
            color = '#007bff'
        elif 26 <= masindex <= 27.9:
            status = ' - Излишний'
            color = '#e8b300'
        elif 28 <= masindex <= 30.9:
            status = ' - Ожирение 1 степени'
            color = '#e87e0c'
        elif 31 <= masindex <= 35.9:
            status = ' - Ожирение 2 степени'
            color = '#e8490e'
        elif 36 <= masindex <= 40.9:
            status = ' - Ожирение 3 степени'
            color = '#e80b0d'
        elif 41 <= masindex:
            status = ' - Ожирение 4 степени'
            color = '#c00000'
    return [status, color]


def parsing(raw_html):
    res = 0
    r = requests.get(raw_html)
    soup = BeautifulSoup(r.content, 'html.parser')
    for tag in soup.find_all("td", 'p5'):
        try:
            if int(tag.text) > 641:
                res = tag.text
        except ValueError:
            pass
    return res


class WellBeing(TemplateView):
    template_name = 'well-being.html'

    def get(self, request):
        form = AtmosphericPressureForm
        ctx = {'form': form}
        return render(request, self.template_name, ctx)

    def post(self, request):
        form = AtmosphericPressureForm(request.POST)
        well_being = request.POST['well-being']
        today = datetime.date.today().strftime("%Y-%m-%d")
        day = request.POST['day']
        if day > today:
            messages.error(request,"Введите верную дату")
            return redirect(self.template_name)
        city = request.POST['city']
        pressure = parsing('https://sinoptik.ua/погода-{}/{}'.format(city, day))
        try:
            peid = Human.objects.get(email=request.user.email).id
            mod = AtmosphericPressure(well_being=well_being, person_id=peid, day=day, pressure=pressure)
            mod.save()
        except ObjectDoesNotExist:
            er = 'Для использования данной функции необходимо внести персональные данные в личном кабинете, '
            ctx = {'er': er}
            return render(request, 'well-being.html', ctx)
        except IntegrityError:
            pass

        # model = AtmosphericPressure.objects.get(person=peid)
        messages.success(request, 'Данные за {} успешно добавлены, город - {}, атмосферное давление - {}'.format(day, city, pressure))
        return redirect(self.template_name)


class WellBeingDataList(TemplateView):
    template_name = 'wellbeingdatalist.html'

    def get(self, request):
        if request.user.is_authenticated:
            all_data = AtmosphericPressure.objects.filter(person_id=Human.objects.get(email=request.user.email).id).order_by('day')
            ctx = {'all_data': all_data}
            return render(request, self.template_name, ctx)
        else:
            return render(request, self.template_name, {})

    def post(self, request):
        col = request.POST['delete1']
        AtmosphericPressure.objects.filter(id=col).delete()
        return redirect(self.template_name)


class Account(TemplateView):
    template_name = 'account.html'

    def get(self, request):
        our_user = Human.objects.filter(email=request.user.email)
        inbase = True
        a = list(our_user)
        masindex = imt(request.user.email)
        res = imtMSG(request.user.email, masindex)
        masindex_result = res[0]
        masindex_color = res[1]
        try:
            b = a[0]
        except IndexError:
            inbase = False
        ctx = {
            'our_user': our_user,
            'inbase': inbase,
            'imt': masindex,
            'imtres': masindex_result,
            'imtcolr': masindex_color,
        }
        return render(request, self.template_name, ctx)

    def post(self, request):
        form = HumanForm(request.POST)
        if form.is_valid():
            # chk = request.POST['hide_data']
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
