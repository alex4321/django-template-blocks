Description
===================
Adds ability to use your blocks in django code.

Installation
-------------

After `git clone https://github.com/alex4321/django-template-blocks` add application to `INSTALLED_APPS`
`INSTALLED_APPS = (
   ...,
  'blocks',
)`

Usage
-------------
To use it you need 2 things:

 - create a "view" that returns string with rendered block code
 - add tags to your templates
 - associate "block name" and "view" in settings.py

E.g. you can use next template:
`{% load blocks %}
...
{% view_block tagcloud %}`

In settings.py
`BLOCK_VIEWS = {
    'tagcloud': "tags.views.tagcloud"
}`
In tag.views:
`from django.shortcuts import render
from tags.models import Tag
from django.conf import settings
from django.template import Context, loader

TAG_CATEGORY = getattr(settings, "TAG_CATEGORY", 0)

def tagcloud():
    tags = Tag.objects.filter(category=TAG_CATEGORY)
    if len(tags) > 0:
        template = loader.get_template("blocks/tagcloud.html")
        context = Context({"tags": tags})
        return template.render(context)
    else:
        return ""
`