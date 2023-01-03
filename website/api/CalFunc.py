from .Google import Create_Service, convert_to_RFC_datetime

API_NAME = 'Appointment Sys'
API_VERSION = 'v3'
SCOPES = ['https://www.googleapis.com/auth/calendar',
              'https://www.googleapis.com/auth/calendar.events']
TIMEOFFSET = 5
OPENTIME = 10
CLOSETIME = 19

def makeService(json):
    """
    Creates a Google Calendar Api Service with a json file.
    """
    CLIENT_SECRET_FILE = f'media/{json}'
    return Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)

def makeAppointment(year, month, date, hour, min, email, name, phone, json):
    """
    Creates an Instance of an Appointment and updates customer and Artist Profile
    """
    #Creates the service 
    service = makeService(json)

    #Fix
    Ehour = hour
    Emin = 30
    if min == 30:
        Ehour = hour + 1
        Emin = 0
   
    #Creates the Google Calendar Event
    event_request_body = {
        'start': {
            'dateTime': convert_to_RFC_datetime(year, month, date, (hour+TIMEOFFSET)%24, min),
            'timeZone': 'America/New_York'
        },
        'end': {
            'dateTime': convert_to_RFC_datetime(year, month, date,(Ehour+TIMEOFFSET)%24, Emin),
            'timeZone': 'America/New_York'
        },
        'summary': f'{name}`s Appointment,{phone}',
        'description': 'Consulting',
        'colorId': 2,
        'status': 'confirmed',
        'visiblility': 'public',
        'location': 'New York City, NY',
        'attendees': [
            {'email': f'{email}'}],
        'reminders': {
            'useDefault': False,
            'overrides': [
                {'method': 'email', 'minutes': 24 * 60},
                {'method': 'popup', 'minutes': 10},
            ],
        },
    }

    #Uploads the event to the Google Calendar
    response = service.events().insert(
        calendarId='primary',
        body=event_request_body
    ).execute()


def returnTimes(year, month, date, json):
    """
    Returns the times that the Artist is available for an Appointment
    """

    hours = []
    minutes = []
    result = []
    hour = OPENTIME-1
    minute = 0

    #Loops each 30 minute interval and checks if it is a open time. Adds to result if it is.
    while (hour < CLOSETIME):
        if minute == 0:
            hour += 1

            if checkOpen(json, year, month, date, hour, minute, hour, 30):
                result.append([hour, minute, hour - 12])

            minute += 30
        else:
            if checkOpen(json, year, month, date, hour, minute, hour + 1, 0):
                result.append([hour, minute, hour - 12])
            minute = 00

    return result

def checkOpen(json, year, month, date,hour, minute, ehour, eminute):
    #Creates Google Api Service 
    service = makeService(json)

    #Gets all events from start time to end time
    response = service.events().list(
            calendarId='primary',
            timeZone='America/New_York',
            timeMin=convert_to_RFC_datetime(
                year, month, date, (hour+TIMEOFFSET)%24, minute),
            timeMax=convert_to_RFC_datetime(
                year, month, date, (ehour+TIMEOFFSET)%24, eminute),
            singleEvents=True
        ).execute()
    events = response.get('items', [])

    #returns true if there are no events else false
    return (len(events) < 1)
          
