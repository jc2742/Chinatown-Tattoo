from .Google import Create_Service, convert_to_RFC_datetime


def makeAppointment(year, month, date, hour, min, email, name, phone, json):
    CLIENT_SECRET_FILE = f'media/{json}'
    API_NAME = 'Appointment Sys'
    API_VERSION = 'v3'
    SCOPES = ['https://www.googleapis.com/auth/calendar',
              'https://www.googleapis.com/auth/calendar.events']
    service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)
    timeOffset = 4
    Ehour = hour
    Emin = 30
    if min == 30:
        Ehour = hour + 1
        Emin = 0

    event_request_body = {
        'start': {
            'dateTime': convert_to_RFC_datetime(year, month, date, hour+timeOffset, min),
            'timeZone': 'America/New_York'
        },
        'end': {
            'dateTime': convert_to_RFC_datetime(year, month, date, Ehour+timeOffset, Emin),
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
    response = service.events().insert(
        calendarId='primary',
        body=event_request_body
    ).execute()


def returnTimes(year, month, date, json):
    CLIENT_SECRET_FILE = f'media/{json}'
    API_NAME = 'Appointment Sys'
    API_VERSION = 'v3'
    SCOPES = ['https://www.googleapis.com/auth/calendar',
              'https://www.googleapis.com/auth/calendar.events']
    service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)
    timeOffset = 4
    hours = []
    minutes = []
    openTime = 10
    closeTime = 19
    hour = 9
    minute = 00
    result = []

    while (hour < closeTime):
        if minute == 00:
            hour += 1
            hours.append(hour)
            minutes.append(minute)
            minute += 30
        else:
            hours.append(hour)
            minutes.append(minute)
            minute = 00

    for i in range(len(hours)-1):
        response = service.events().list(
            calendarId='primary',
            timeZone='America/New_York',
            timeMin=convert_to_RFC_datetime(
                year, month, date, hours[i]+timeOffset, minutes[i]),
            timeMax=convert_to_RFC_datetime(
                year, month, date, hours[i+1]+timeOffset, minutes[i+1]),
            singleEvents=True
        ).execute()
        events = response.get('items', [])

        if len(events) < 1:
            pm = False
            result.append([hours[i], minutes[i], hours[i]-12])

    return result
