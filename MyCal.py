from icalendar import Calendar, Event
import uuid
from dates import *
from Regatta import *


class MyCal():

    def icalendar_initial(self):
        self.cal = Calendar()
        self.cal['version'] = 2.0
        self.cal['prodid'] = "//Project//ical//Sailing_Calendar//EN"
        self.cal.add('BEGIN', 'VTIMEZONE')
        self.cal.add('TZID', 'Europe/Athens')
        self.cal.add('BEGIN', 'STANDARD')
        self.cal.add('TZOFFSETFROM', timedelta(hours=0, minutes=0, seconds=0))
        self.cal.add('TZOFFSETTO', -timedelta(hours=3))
        self.cal.add('TZNAME', 'UTC')
        self.cal.add('END', 'STANDARD')
        self.cal.add('END', 'VTIMEZONE')
    def create_new_event(self, regatta):
        self.cal['name'] = regatta.district

        if isinstance(regatta, RaceType1):
            event = Event()
            current_time = datetime.now()
            event.add('transp', 'TRANSPARENT')
            event.add('summary', regatta.name)
            event['description'] = [
                {'Όμιλος': regatta.club_name, 'Διαδρομή': regatta.course, 'Απόσταση': regatta.length,
                 'Περιφέρεια': regatta.district}]
            uid = str(uuid.uuid4())
            event.add('uid', uid)
            event['dtstart'] = format_timestamp(to_datetime(regatta.stdate, regatta.sttime))
            event['created'] = format_timestamp(current_time)
            event['last-modified'] = format_timestamp(current_time)
            event['dtstamp'] = format_timestamp(current_time)
            return event
        elif isinstance(regatta, RaceType2):
            event = Event()
            current_time = datetime.now()
            event.add('transp', 'TRANSPARENT')
            event.add('summary', regatta.name)
            event['description'] = [
                {'Όμιλος': regatta.club_name, 'Διαδορμή': regatta.course, 'Απόσταση': regatta.length,
                 'Περιφέρεια': regatta.district}]
            uid = str(uuid.uuid4())
            event.add('uid', uid)
            event['dtstart'] = format_timestamp(to_datetime(regatta.stdate, regatta.sttime))
            event['dtend'] = format_timestamp(to_datetime(regatta.todate, regatta.sttime))
            event['created'] = format_timestamp(current_time)
            event['last-modified'] = format_timestamp(current_time)
            event['dtstamp'] = format_timestamp(current_time)
            return event
        elif isinstance(regatta, RaceType3):
            events = []
            for reg in regatta.races:
                event = Event()
                current_time = datetime.now()
                event.add('transp', 'OPAQUE')
                event.add('summary', regatta.name)
                event['description'] = [
                    {'Όμιλος': regatta.club_name, 'Διαδρομή': reg.course, 'Απόσταση': reg.length,
                     'Περιφέρεια': regatta.district}]
                uid = str(uuid.uuid4())
                event.add('uid', uid)
                event['dtstart'] = format_timestamp(to_datetime(reg.stdate, reg.sttime))
                event['created'] = format_timestamp(current_time)
                event['last-modified'] = format_timestamp(current_time)
                event['dtstamp'] = format_timestamp(current_time)
                events.append(event)
            return events


    def google_calendar_event(self, regatta):
        if isinstance(regatta, RaceType1):
            event = {
                "kind": "calendar#event",
                'summary': regatta.name,
                'description': f"Όμιλος:{regatta.club_name},Διαδρομή: {regatta.course},Απόσταση:{regatta.length},Περιφέρεια: {regatta.district}",
                'start': {
                    'dateTime': to_google_time(to_datetime(regatta.stdate, regatta.sttime)),
                    'timezone': 'Europe/Athens'
                },
                'end': {
                    'dateTime': to_google_time(to_datetime(regatta.stdate, regatta.sttime) + timedelta(hours=2)),
                    'timezone': 'Europe/Athens'
                },
                'colorId': 5,
                'status': 'confirmed',

                'organizer': {
                    'displayName': "Επιτροπή Ανοιχτής Θαλάσσης"
                }
            }
            return event
        elif isinstance(regatta, RaceType2):
            event = {
                "kind": "calendar#event",
                'summary': regatta.name,
                'description': f"Όμιλος:{regatta.club_name},Διαδρομή: {regatta.course},Απόσταση:{regatta.length},Περιφέρεια: {regatta.district}",
                'start': {
                    'dateTime': to_google_time(to_datetime(regatta.stdate, regatta.sttime)),
                    'timezone': 'Europe/Athens'
                },
                'end': {
                    'dateTime': to_google_time(to_datetime(regatta.todate, regatta.sttime)),
                    'timezone': 'Europe/Athens'
                },
                'colorId': 5,
                'status': 'confirmed',
                'organizer': {
                    'displayName': "Επιτροπή Ανοιχτής Θαλάσσης"
                }
            }
            return event
        elif isinstance(regatta, RaceType3):
            events = []
            for reg in regatta.races:
                event = {
                    "kind": "calendar#event",
                    'summary': reg.name,
                    'description': f"Όμιλος:{regatta.club_name},Διαδρομή: {reg.course},Απόσταση:{reg.length},Περιφέρεια: {regatta.district}",
                    'start': {
                        'dateTime': to_google_time(to_datetime(reg.stdate, reg.sttime)),
                        'timezone': 'Europe/Athens'
                    },
                    'end': {
                        'dateTime': to_google_time(to_datetime(reg.stdate, reg.sttime) + timedelta(hours=2)),
                        'timezone': 'Europe/Athens'
                    },
                    'colorId': 5,
                    'status': 'confirmed',
                    'organizer': {
                        'displayName': "Επιτροπή Ανοιχτής Θαλάσσης"
                    }
                }
                events.append(event)
            return events

    def ms_calendar_event(self, regatta):
        if isinstance(regatta, RaceType1):
            event = {
                "subject": regatta.name,
                'start': {
                    'dateTime': to_google_time(to_datetime(regatta.stdate, regatta.sttime)),
                    'timezone': 'Europe/Athens'
                },
                'end': {
                    'dateTime': to_google_time(
                        to_datetime(regatta.stdate, regatta.sttime) + timedelta(hours=2)),
                    'timezone': 'Europe/Athens'
                },
                "body": {
                    "contentType": "HTML",
                    "content": f"Όμιλος:{regatta.club_name},Διαδρομή: {regatta.course},Απόσταση:{regatta.length},Περιφέρεια: {regatta.district}"
                },
            }

            return event
        elif isinstance(regatta, RaceType2):
            event = {
                "subject": regatta.name,

                'body': {
                    "contentType": "HTML",
                    "content": f"Όμιλος:{regatta.club_name},Διαδρομή: {regatta.course},Απόσταση:{regatta.length},Περιφέρεια: {regatta.district}",
                },
                'start': {
                    'dateTime': to_google_time(to_datetime(regatta.stdate, regatta.sttime)),
                    'timezone': 'Europe/Athens'
                },
                'end': {
                    'dateTime': to_google_time(to_datetime(regatta.todate, regatta.sttime)),
                    'timezone': 'Europe/Athens'
                },

            }
            return event
        elif isinstance(regatta, RaceType3):
            events = []
            for reg in regatta.races:
                event = {

                    'subject': reg.name,
                    'body': {
                        'contentType': "HTML",
                        'content': f"Όμιλος:{regatta.club_name},Διαδρομή: {reg.course},Απόσταση:{reg.length},Περιφέρεια: {regatta.district}",
                    },
                    'start': {
                        'dateTime': to_google_time(to_datetime(reg.stdate, reg.sttime)),
                        'timezone': 'Europe/Athens'
                    },
                    'end': {
                        'dateTime': to_google_time(to_datetime(reg.stdate, reg.sttime) + timedelta(hours=2)),
                        'timezone': 'Europe/Athens'
                    },
                }
                events.append(event)
            return events

    def write_event_to_file(self, event, filename):
        try:
            if isinstance(event, list):
                for e in event:
                    self.cal.add_component(e)
            else:
                self.cal.add_component(event)
            with open(filename, 'wb') as o:
                o.write(self.cal.to_ical(sorted=False))
        except FileNotFoundError as e:
            print(e)
        except Exception as e:
            print(e)
