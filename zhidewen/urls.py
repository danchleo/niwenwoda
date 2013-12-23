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
    url(r'^q/(?P<question_id>(\d+))/$', 'questions.show', name='question'),
    url(r'^q/(?P<question_id>(\d+))/edit/$', 'questions.update', name='edit_question'),
    url(r'^q/(?P<question_id>(\d+))/delete/$', 'questions.delete', name='delete_question'),
    url(r'^q/(?P<question_id>(\d+))/answer/', 'answers.answer_question', name='answer_question'),
    url(r'^q/(?P<question_id>(\d+))/vote/', 'votes.vote_question', name='vote_question'),

    url(r'^a/(?P<answer_id>(\d+))/edit/', 'answers.update', name='edit_answer'),
    url(r'^a/(?P<answer_id>(\d+))/delete/', 'answers.delete', name='delete_answer'),
    url(r'^a/(?P<answer_id>(\d+))/vote/', 'votes.vote_answer', name='vote_answer'),

    url(r'^tags/$', 'tags.wall', name='tags'),
    url(r'^t/(?P<tag_name>([^/]*))/$', 'tags.page', name='tag'),
    url(r'^tags/hottest$', 'tags.hottest', name='hottest_tags'),

    url(r'^users/$', 'users.wall', name='users'),
    url(r'^u/([^/]*)/$', 'users.page', name='user'),
    url(r'^u/([^/]*)/questions/$', 'users.contents', name='user_questions',
        kwargs={'template': 'users/questions.html'}),
    url(r'^u/([^/]*)/answers/$', 'users.contents', name='user_answers', kwargs={'template': 'users/answers.html'}),

    url(r'^u/([^/]*)/marked/$', 'mark.marked', name='marked'),
    url(r'^u/([^/]*)/marked/questions/$', 'mark.marked', name='marked_questions', kwargs={'mark_type': 'question'}),
    url(r'^u/([^/]*)/marked/answers/$', 'mark.marked', name='marked_answers', kwargs={'mark_type': 'answer'}),
)

urlpatterns += patterns('',
    url(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'users/login.html'}, name='login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}, name='logout')
)

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
