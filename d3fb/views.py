import json
import datetime

class DateTimeJSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime.datetime):
            return o.isoformat()
        json.JSONEncoder.default(self, o)
            
def my_view(request):
    return {'project':'d3fb'}

def expand_dl(client, email):
    """Expand a distribution list."""
    return [email]

def get_user_availability(client, emails):
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
    fb = client.factory.create('t:FreeBusyViewOptions')
    fb.TimeWindow.StartTime = datetime.datetime.now().isoformat()
    fb.TimeWindow.EndTime = datetime.datetime.now() + datetime.timedelta(hours=12).isoformat()
    fb.MergedFreeBusyIntervalInMinutes = 60
    fb.RequestedView = 'DetailedMerged'
    
    availability = client.service.GetUserAvailability(tz, md, fb)
    
    return availability

def freebusy(request):
    """Return free/busy information for an expanded Exchange distribution list
    as some JSON, cached aggressively."""
    
    client = request.settings['ews.client']
    email = request.settings['freebusy.email']
    
    emails = expand_dl(client, email)
    availability = get_user_availability(client, emails)    
     
    return DateTimeJSONEncoder.encode(availability)
