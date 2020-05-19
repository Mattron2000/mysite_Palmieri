"""mysite_Palmieri URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('polls/', include('polls.urls'))
]

"""
Creo un nuovo progetto Django: $django-admin startproject mysite_Palmieri
Creo una nuova applicazione: $django manage.py startap polls
Aggiungo a polls/views.py :
    from django.http import HttpResponse

    def index(request):
        return HttpResponse("Hello, world. You're at the polls index.")

polls/urls.py :
    from django.urls import path
    from . import views

    urlpatterns = [
        path('', views.index, name='index'),
    ]

Aggiungo a mysite_Palmieri/urls.py :
    from django.contrib import admin
    from django.urls import include, path

    urlpatterns = [
        path('admin/', admin.site.urls),
        path('polls/', include('polls.urls')) # include() è una funzione che permette di puntare a un altro file uyrls.py
    ]
#
#

L'urlpatterns è una sorta di array di path() e queste funzioni path() necessitano di 4 parametri (2 obbligatori e 2 opzionali):
- path() route : route è una stringa dove contiene l'URL, infatto quando processa la richiesta, Django controlla la lista urlpatterns finche trova quella richiesta
- path() view : Quando Django trova l'associazione, chiama la funzione view() con HttpRequest e cattura qualsiasai primo valore dalla route
- path() kwargs : Parametro arbitrario che può passare un determinato valore
- path() name : nominare un URL permette di riferire univocamente da qualsiasi parte di Django permettedsndo di compiere modifiche globali del sito senza cambiare nomi a tutti i file coinvolti

#
#

Modifico il TIME_ZONE in mysite_Palmieri :
    TIME_ZONE = 'Europe/Rome'

python manage.py migrate # potente comando utila a crreare automaticamente tutti i database necessari seguendo il file setting.py di mysite_Palmieri

Modifico polls/model.py :
    from django.db import models
    from django.utils import timezone
    import datetime

    # Create your models here.

    class Question(models.Model):   # modello per le domande
        question_text = models.CharField(max_length=200)
        pub_date = models.DateTimeField('data pubblicata')

        def __str__(self):      # utile in shell per visualizzare il contenuto dell'object 
            return self.question_text

        def was_published_recently(self):   # funzione per vedere che è una domanda "nuova"
            return self.pub_date >= timezone.now() - datetime.timedelta(days=1)

    class Choice(models.Model):     # modello per le scelte in risposta alle domande
        question = models.ForeignKey(Question, on_delete=models.CASCADE)
        choice_text = models.CharField(max_length=200)
        votes = models.IntegerField(default=0)

        def __str__(self):      # utile in shell per visualizzare il contenuto dell'object 
            return self.choice_text

Aggiungere a INSTALLED_APPS di mysite_Palmieri/settings.py : 'polls.apps.PollsConfig',

python manage.py makemigrations polls # con questo comando diciamo a Django che abbiamo fatto delle modifiche e vogliamo che siamo immagazzinate nella cartella migration
    Migrations for 'polls':
    polls\migrations\0001_initial.py
        - Create model Question
        - Create model Choice
    
python manage.py sqlmigrate polls 0001  # questo permette di eseguire le migrazioni e gestire le tabelle automaticamente
    BEGIN;
    --
    -- Create model Question
    --
    CREATE TABLE "polls_question" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "question_text" varchar(200) NOT NULL, "pub_date" datetime NOT NULL);
    --
    -- Create model Choice
    --
    CREATE TABLE "polls_choice" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "choice_text" varchar(200) NOT NULL, "votes" integer NOT NULL, "question_id" integer NOT NULL REFERENCES "polls_question" ("id") DEFERRABLE INITIALLY DEFERRED);
    CREATE INDEX "polls_choice_question_id_c5b4b260" ON "polls_choice" ("question_id");
    COMMIT;

python manage.py migrate    # con questo applichiamo le migrations non applicate per sincronizzare i cambiamenti con le tabelle del DB

python manage.py shell  # per aprire la shell

>>> from polls.models import Choice, Question
>>> Question.objects.all()
<QuerySet []>
>>> from django.utils import timezone
>>> q = Question(question_text="What's new?", pub_date=timezone.now())
>>> q.save()
>>> q.id
1
>>> q.question_text
"What's new?"
>>> q.pub_date
datetime.datetime(2020, 5, 19, 7, 23, 45, 328005, tzinfo=<UTC>)
>>> q.question_text = "What's up?"
>>> q.save()
>>> Question.objects.all()
<QuerySet [<Question: Question object (1)>]>
"""
"""
>>> from polls.models import Choice, Question
>>> Question.objects.all()
<QuerySet [<Question: What's up?>]>
>>> Question.objects.filter(id=1)
<QuerySet [<Question: What's up?>]>
>>> Question.objects.filter(question_text__startswith='What')
<QuerySet [<Question: What's up?>]>
>>> from django.utils import timezone
>>> current_year = timezone.now().year
>>> Question.objects.get(pub_date__year=current_year)
<Question: What's up?>
>>> Question.objects.get(id=2)
Traceback (most recent call last):
  ...
polls.models.Question.DoesNotExist: Question matching query does not exist.
>>> Question.objects.get(pk=1)
<Question: What's up?>
>>> q = Question.objects.get(pk=1)
>>> q.was_published_recently()
True
>>> q = Question.objects.get(pk=1)
>>> q.choice_set.all()
<QuerySet []>
>>> q.choice_set.create(choice_text='Not much', votes=0)
<Choice: Not much>
>>> q.choice_set.create(choice_text='The sky', votes=0)
<Choice: The sky>
>>> c = q.choice_set.create(choice_text='Just hacking again', votes=0)
>>> c.question
<Question: What's up?>
>>> q.choice_set.all()
<QuerySet [<Choice: Not much>, <Choice: The sky>, <Choice: Just hacking again>]>
>>> q.choice_set.count()
3
>>> Choice.objects.filter(question__pub_date__year=current_year)
<QuerySet [<Choice: Not much>, <Choice: The sky>, <Choice: Just hacking again>]>
>>> c = q.choice_set.filter(choice_text__startswith='Just hacking')
>>> c.delete()
(1, {'polls.Choice': 1})
>>> exit()

python manage.py createsuperuser usr : Palmieri pwd: admin

nuovi def in polls/views.py:
    def detail(request, question_id):
        return HttpResponse("You're looking at question %s." % question_id)

    def results(request, question_id):
        response = "You're looking at the results of question %s."
        return HttpResponse(response % question_id)

    def vote(request, question_id):
        return HttpResponse("You're voting on question %s." % question_id)

di conseguenza annotarli in polls/urls.py :"
    from django.urls import path
    from . import views

    urlpatterns = [
        # ex: /polls/
        path('', views.index, name='index'),
        # ex: /polls/5/
        path('<int:question_id>/', views.detail, name='detail'),
        # ex: /polls/5/results/
        path('<int:question_id>/results/', views.results, name='results'),
        # ex: /polls/5/vote/
        path('<int:question_id>/vote/', views.vote, name='vote'),
    ]

Modifichiamo def in polls/views.py in :
    from django.shortcuts import render, get_object_or_404
    from django.http import HttpResponse, Http404
    from .models import Question
    from django.template import loader

    # Create your views here.

    def index(request):
        latest_question_list = Question.objects.order_by('-pub_date')[:5]   
        context = {'latest_question_list': latest_question_list}
        return render(request, 'polls/index.html', context)

    def detail(request, question_id):   # questo def utilizza la funzione get_object_or_404() che permette di semplificare il problema del 404 lasciando a Django di mostrare l'errore
        question = get_object_or_404(Question, pk=question_id)
        return render(request, 'polls/detail.html', {'question': question})

    def results(request, question_id):
        response = "You're looking at the results of question %s."
        return HttpResponse(response % question_id)

    def vote(request, question_id):
        return HttpResponse("You're voting on question %s." % question_id)

Aggiungo nuovi path() in polls/urls.py :
    from django.urls import path
    from . import views

    urlpatterns = [
        # ex: /polls/
        path('', views.index, name='index'),
        # ex: /polls/5/
        path('<int:question_id>/', views.detail, name='detail'),
        # ex: /polls/5/results/
        path('<int:question_id>/results/', views.results, name='results'),
        # ex: /polls/5/vote/
        path('<int:question_id>/vote/', views.vote, name='vote'),
    ]

In polls/templates/polls/index.html :
    {% if latest_question_list %}
        <ul>
        {% for question in latest_question_list %}
            <li><a href="{% url 'polls:detail' question.id %}">{{ question.question_text }}</a></li>    # bisogna evitare di utilizare glihardcore URLs nei templates perchè complicano nel momento in cui cambiamo i link e per effetto cascata dobbiamo cambiare tutti gli altri perdendo tempo e il modo migliore per farlo e utilizzare il tag {% url %} 
        {% endfor %}
        </ul>
    {% else %}
        <p>No polls are available.</p>
    {% endif %}

In polls/templates/polls/detail.html :
    <h1>{{ question.question_text }}</h1>
    <ul>
    {% for choice in question.choice_set.all %}
        <li>{{ choice.choice_text }}</li>
    {% endfor %}
    </ul>

Modifico in polls/urls.py 
    path('<int:question_id>/', views.detail, name='detail'), in path('specifics/<int:question_id>/', views.detail, name='detail'),

    # nel file urls.py si utilizzaa il parametro name = "" per migliorare la comodità nella scrittura delle views e dare un nome univoco alle funzioni

Aggiorno detail.html:
    <h1>{{ question.question_text }}</h1>

    {% if error_message %}<p><strong>{{ error_message }}</strong></p>{% endif %}

    <form action="{% url 'polls:vote' question.id %}" method="post">
    {% csrf_token %}
    {% for choice in question.choice_set.all %}
        <input type="radio" name="choice" id="choice{{ forloop.counter }}" value="{{ choice.id }}">
        <label for="choice{{ forloop.counter }}">{{ choice.choice_text }}</label><br>
    {% endfor %}
    <input type="submit" value="Vote">
    </form>

Aggiorno i def vote() e results() in polls/views.py :

    from django.http import HttpResponse, HttpResponseRedirect
    from django.shortcuts import get_object_or_404, render
    from django.urls import reverse
    from .models import Choice, Question

    def vote(request, question_id):
        question = get_object_or_404(Question, pk=question_id)
        try:
            selected_choice = question.choice_set.get(pk=request.POST['choice'])
        except (KeyError, Choice.DoesNotExist):
            # Redisplay the question voting form.
            return render(request, 'polls/detail.html', {
                'question': question,
                'error_message': "You didn't select a choice.",
            })
        else:
            selected_choice.votes += 1
            selected_choice.save()
            # Always return an HttpResponseRedirect after successfully dealing
            # with POST data. This prevents data from being posted twice if a
            # user hits the Back button.
            return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))

    from django.shortcuts import get_object_or_404, render

    def results(request, question_id):
        question = get_object_or_404(Question, pk=question_id)
        return render(request, 'polls/results.html', {'question': question})

Creo results.html :
    <h1>{{ question.question_text }}</h1>

    <ul>
    {% for choice in question.choice_set.all %}
        <li>{{ choice.choice_text }} -- {{ choice.votes }} vote{{ choice.votes|pluralize }}</li>
    {% endfor %}
    </ul>

    <a href="{% url 'polls:detail' question.id %}">Vote again?</a>

modifico polls/urls.py :
    from django.urls import path
    from . import views

    app_name = 'polls'
    urlpatterns = [
        path('', views.IndexView.as_view(), name='index'),
        path('<int:pk>/', views.DetailView.as_view(), name='detail'),
        path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
        path('<int:question_id>/vote/', views.vote, name='vote'),
    ]

di conseguenza modificare i views.py di polls :
    from django.http import HttpResponseRedirect
    from django.shortcuts import get_object_or_404, render
    from django.urls import reverse
    from django.views import generic

    from .models import Choice, Question


    class IndexView(generic.ListView):
        template_name = 'polls/index.html'
        context_object_name = 'latest_question_list'

        def get_queryset(self):
            #Return the last five published questions.
            return Question.objects.order_by('-pub_date')[:5]


    class DetailView(generic.DetailView):
        model = Question
        template_name = 'polls/detail.html'


    class ResultsView(generic.DetailView):
        model = Question
        template_name = 'polls/results.html'


    def vote(request, question_id):
        ... # same as above, no changes needed.
"""