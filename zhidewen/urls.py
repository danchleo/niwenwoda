from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.conf import settings

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('zhidewen.views',

    url(r'^$', 'questions.newest', name='home'),
    url(r'^newest/$', 'questions.newest', name='newest_questions'),
    url(r'^hottest/$', 'questions.hottest', name='hottest_questions'),
    url(r'^unanswered/$', 'questions.unanswered', name='unanswered_questions'),

    url(r'^ask/$', 'questions.ask', name='ask'),
    url(r'^q/(\d+)/$', 'questions.show', name='question'),
    url(r'^q/(\d+)/edit/$', 'questions.update', name='edit_question'),
    url(r'^q/(\d+)/delete/$', 'questions.delete', name='delete_question'),
    url(r'^q/(\d+)/answer/', 'answers.answer_question', name='answer_question'),
    url(r'^q/(\d+)/vote/', 'votes.vote_question', name='vote_question'),

    url(r'^a/(\d+)/edit/', 'answers.update', name='edit_answer'),
    url(r'^a/(\d+)/delete/', 'answers.delete', name='delete_answer'),
    url(r'^a/(\d+)/vote/', 'votes.vote_answer', name='vote_answer'),

    url(r'^tags/$', 'tags.index', name='tags'),
    url(r'^t/([^/]*)/$', 'tags.questions', name='tag'),

    url(r'^users/$', 'users.index', name='users'),
    url(r'^u/([^/]*)/$', 'users.show', name='user'),
    url(r'^u/([^/]*)/questions/$', 'users.contents', name='user_questions', kwargs={'template': 'users/questions.html'}),
    url(r'^u/([^/]*)/answers/$', 'users.contents', name='user_answers', kwargs={'template': 'users/answers.html'}),
)

urlpatterns += patterns('',
    url(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'users/login.html'}, name='login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}, name='logout')
)

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
