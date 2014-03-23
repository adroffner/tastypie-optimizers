tastypie-optimizers
===================

Optimize Tastypie ModelResource requests. Limit unnecessary SQL queries on related data. This is most important to OLTP applications.

Unit Tests
==========

Run **unit tests** with your **tastypie** version to make sure this is compatible. Simply, add both to a Django project's **INSTALLED_APPS** and hook the **API URLs** into the project's urls.py.

* project/urls.py

```
from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

from tastypie_optimizers.api import v1_api

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'github.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),

    # Run API Unit Tests
    url(r'^optimizer/', include(v1_api.urls)),
)
```
