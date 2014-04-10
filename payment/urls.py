__author__ = 'i.bauer'

from django.conf.urls import patterns, url


urlpatterns = patterns('',
                       url(r'^(?P<payment_id>\d+)/success/$', "cuescience_payment.views.success_view", name="success"),
                       url(r'^(?P<payment_id>\d+)/cancel/$', "cuescience_payment.views.cancel_view", name="cancel"),
)
