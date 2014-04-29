__author__ = 'i.bauer'

from django.conf.urls import patterns, url


urlpatterns = patterns('',
                       url(r'^(?P<payment_id>\d+)/redirect/$', "payment.views.redirect_view", name="redirect"),
                       url(r'^(?P<payment_id>\d+)/success/$', "payment.views.success_view", name="success"),
                       url(r'^(?P<payment_id>\d+)/cancel/$', "payment.views.cancel_view", name="cancel"),
)
