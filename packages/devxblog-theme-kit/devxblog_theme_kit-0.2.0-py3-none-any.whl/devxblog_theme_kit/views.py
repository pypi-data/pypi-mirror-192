import datetime
import json
from os import environ
from urllib.parse import urlparse, parse_qs, urlencode
import pkg_resources
import yaml

from django.utils import timezone
from django.views.generic import TemplateView
import jsonschema

DEVXBLOG_VARS = json.loads(environ.get('DEVXBLOG_VARS', '{}'))
with open('theme.yaml') as data:
    theme_meta = yaml.load(data.read(), Loader=yaml.Loader)

variable_def = theme_meta.get('variables', {'type': 'object'})
variables = theme_meta.get('variables_default', {})
variables.update(DEVXBLOG_VARS)

jsonschema.validate(variable_def, variables)
print(f'Final theme variables {variables}')


def get_data(key: str) -> dict:
    data = {}
    with open('data.json', 'r') as f:
        data['blog'] = json.load(f)[key]
    data['navigation'] = {
        'items': data['blog'].pop('navigation')
    }
    return data


def get_page_content():
    return pkg_resources.resource_string('devxblog_theme_kit', 'page_template.html').decode()


class ThemePageView(TemplateView):
    template_name = 'page_view.html'

    def get_context_data(self, **kwargs):
        from django.conf import settings

        context = super(ThemePageView, self).get_context_data(**kwargs)
        context['theme'] = {
            'name': 'My theme',
        }
        context['vars'] = variables
        context['page'] = {
            'title': 'Example Page Name',
            'slug': 'page-slug',
            'date_created': timezone.datetime(2022, 6, 1, 12, 0, 0),
            'date_updated': timezone.datetime(2022, 6, 2, 13, 30, 22),
            'content': get_page_content(),
            'protected': False
        }
        context['today'] = datetime.date.today()
        context['meta'] = [
            {'name': 'description', 'content': 'test'},
            {'name': 'author', 'content': 'John Doe'},
        ]

        context.update(get_data('blog'))
        return context


class ThemePostView(TemplateView):
    template_name = 'post_view.html'

    def get_context_data(self, **kwargs):
        context = super(ThemePostView, self).get_context_data(**kwargs)
        context.update(get_data('blog'))
        context['theme'] = {
            'name': 'My theme',
        }
        context['vars'] = variables
        context['post'] = {
            'id': 10,
            'title': 'Example post',
            'content': get_page_content(),
            'date_posted': timezone.datetime(2022, 6, 1, 12, 0, 0),
            'date_updated': timezone.datetime(2022, 6, 1, 13, 0, 0),
            'categories': list(context['blog']['categories'][:2]),
            'author': {
                'id': 3,
                'name': 'John Doe',
                'avatar': None
            }
        }
        context['today'] = datetime.date.today()
        context['back_to_blog_url'] = '/posts/'
        context['meta'] = [
            {'name': 'description', 'content': 'test'},
            {'name': 'author', 'content': 'John Doe'},
        ]
        return context


class ThemePostList(TemplateView):
    template_name = 'post_list.html'

    def get_context_data(self, **kwargs):
        context = super(ThemePostList, self).get_context_data(**kwargs)
        context.update(get_data('blog'))
        context['theme'] = {
            'name': 'My theme',
        }
        context['vars'] = variables


        def is_same_category(c):
            # noinspection PyTypeChecker
            return parse_qs(urlparse(c['href']).query).get('category') == [self.request.GET.get('category')]

        current_category = list(filter(is_same_category, context['blog']['categories']))
        context['category'] = current_category[0] if current_category else None
        context['posts'] = [
            {
                'id': i,
                'title': 'test',
                'date_posted': datetime.datetime(2022, 1, i + 1),
                'href': '/post/' + str(i) + '/'
            } for i in range(15)
        ]
        context['today'] = datetime.date.today()

        current_page = int(self.request.GET.get('page', 1))
        query_params = self._get_query_params_base(current_page)
        previous = self._get_previous_page(current_page, query_params)
        next = self._get_next_page(current_page, query_params)

        context['pagination'] = {
            'previous': previous,
            'current': {
                'number': current_page
            },
            'next': next,
            'first': {'number': 1, 'url': '/posts/?' + urlencode((lambda: {**query_params, 'page': 1})())},
            'last': {'number': 5, 'url': '/posts/?' + urlencode((lambda: {**query_params, 'page': 5})())}
        }
        return context

    def _get_query_params_base(self, current_page):
        if self.request.GET.get('category'):
            query_params = {
                'page': current_page,
                'category': self.request.GET.get('category')
            }
        else:
            query_params = {
                'page': current_page
            }
        return query_params

    def _get_next_page(self, current_page, query_params):
        if current_page < 5:
            next = {
                'number': '3',
                'url': '/posts/?' + urlencode((lambda: {**query_params, 'page': current_page + 1})()),
            }
        else:
            next = None
        return next

    def _get_previous_page(self, current_page, query_params):
        if current_page > 1:
            previous = {
                'number': '1',
                'url': '/posts/?' + urlencode((lambda: {**query_params, 'page': current_page - 1})()),
            }
        else:
            previous = None
        return previous
