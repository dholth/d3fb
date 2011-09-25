from pyramid.config import Configurator
from d3fb.resources import Root

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(root_factory=Root, settings=settings)
    config.add_view('d3fb.views.my_view',
                    context='d3fb:resources.Root',
                    renderer='d3fb:templates/mytemplate.pt')
    config.add_static_view('static', 'd3fb:static', cache_max_age=3600)
    return config.make_wsgi_app()
