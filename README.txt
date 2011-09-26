d3fb
====

Render Exchange 2007 free/busy calendar to svg with d3.js. Uses Exchange
web services to fetch the information.

Usage
-----

d3fb is configured with 3 environment variables: 

EWS_DOMAIN = owa.example.org
EWS_USER = EXAMPLE\\username
EWS_PASS = "battery horse staple"

And one config file setting:

freebusy.email = a.distribution.list@example.org

The web application connects to Exchange Web Services using these credentials,
serving the free/busy information as JSON. JavaScript renders a calendar
from the data. By default this data is cached for 5 minutes to avoid overloading
the server.