import json
import datetime

class DateTimeJSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime.datetime):
            return o.isoformat()
        json.JSONEncoder.default(self, o)

_json_encoder = DateTimeJSONEncoder(indent=2, sort_keys=True)        

def my_view(request):
    return {'project':'d3fb'}

def expand_dl(client, email):
    """Expand a distribution list."""
    return [email]

def get_user_availability(client, emails,
                          start=None, 
                          duration=datetime.timedelta(hours=48)):
    """
    Return user availability for users in emails between start and start + duration
    
    client: suds client
    emails: list of e-mail addresses to query
    start: beginning of free/busy duration (None for datetime.datetime.now())
    duration: duration of free/busy duration
    """        
    # EWS's way of saying EST5EDT:
    tz = client.factory.create('t:TimeZone')
    tz.Bias = 300
    tz.StandardTime.Bias = 0
    tz.StandardTime.Time = '02:00:00'
    tz.StandardTime.DayOrder = 1
    tz.StandardTime.Month = 11
    tz.StandardTime.DayOfWeek = 'Sunday'
    tz.DaylightTime.Bias = -60
    tz.DaylightTime.Time = '02:00:00'
    tz.DaylightTime.DayOrder = 2
    tz.DaylightTime.Month = 3
    tz.DaylightTime.DayOfWeek = 'Sunday'
    
    # List of mailboxes to query for free/busy information
    md = client.factory.create('MailboxDataArray')
    for email in emails:
        mde = client.factory.create('t:MailboxData')
        mde.Email.Address = email
        mde.AttendeeType = 'Room'
        mde.ExcludeConflicts = 'false'
        md.MailboxData.append(mde)

    # Next x hours of free/busy at a specified resolution
    if start is None:
        start = datetime.datetime.now()
    fb = client.factory.create('t:FreeBusyViewOptions')
    fb.TimeWindow.StartTime = start.isoformat()
    fb.TimeWindow.EndTime = (start+duration).isoformat()
    fb.MergedFreeBusyIntervalInMinutes = 60
    fb.RequestedView = 'DetailedMerged'
    
    availability = client.service.GetUserAvailability(tz, md, fb)
    
    return availability

def format_availability(client, email):
    """Fetch user availability and format as a dict 
    (instead of a SOAP object structure)"""
    emails = expand_dl(client, email)
    reply = get_user_availability(client, emails)
    
    availability = {}
        
    for email, fbr in zip(emails, reply.FreeBusyResponseArray.FreeBusyResponse):
        if not hasattr(fbr.FreeBusyView, 'CalendarEventArray'):
            continue
        appointments = []
        for event in fbr.FreeBusyView.CalendarEventArray.CalendarEvent:
            data = {}
            data['start'] = event.StartTime
            data['end'] = event.EndTime
            data['busy'] = event.BusyType
            data['id'] = event.CalendarEventDetails.ID
            data['subject'] = event.CalendarEventDetails.Subject
            appointments.append(data)
        availability[email] = appointments
    return availability

def freebusy(request):
    """Return free/busy information for an expanded Exchange distribution list
    as some JSON, cached aggressively."""    
    client = request.registry.settings['ews.client']
    email = request.registry.settings['freebusy.email']    
    availability = format_availability(client, email)
    json = _json_encoder.encode(availability)
    response = request.response
    response.content_type = 'application/json'
    response.body = json
    return response
