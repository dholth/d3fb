from pyramid.config import Configurator
from d3fb.resources import Root
import ewsclient
from suds.transport.https import WindowsHttpAuthenticated
from suds.client import Client
from suds.cache import ObjectCache
import os

def get_ewsclient():
    ews_domain, ews_user, ews_pass = \
        map(os.environ.get, ('EWS_DOMAIN', 'EWS_USER', 'EWS_PASS'))
    transport = WindowsHttpAuthenticated(username=ews_user,
        password=ews_pass)
    uri = "https://%s/EWS/Services.wsdl" % ews_domain
    # Long cache to avoid w3c xml.xsd lifetime issue:
    client = Client(uri,
                    transport=transport,
                    cache=ObjectCache(weeks=52),
                    plugins=[ewsclient.AddService()])
    return client

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    settings['ews.client'] = get_ewsclient()

    config = Configurator(root_factory=Root, settings=settings)
    config.add_view('d3fb.views.my_view',
                    context='d3fb:resources.Root',
                    renderer='d3fb:templates/mytemplate.pt')
    config.add_view('d3fb.views.freebusy',
                    context='d3fb:resources.Root',
                    name="freebusy.json")
    config.add_static_view('static', 'd3fb:static', cache_max_age=3600)
    return config.make_wsgi_app()
