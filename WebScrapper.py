import xml.etree.ElementTree as ET
import pandas as pd
from Regatta import *
from dates import *


class WebScrapper:
    def __init__(self, file, choice):
        self.file = file
        self.file.seek(0)
        self.choice = choice
        self.myRoot = ET.parse(file).getroot()

    def retrieve_data(self):
        regatta_list = []
        df = pd.DataFrame()
        for child in self.myRoot[1]:
            if child.get('Name') == self.choice:
                district = child.get('Name')
                for reg in child.findall('REGATTA'):
                    index = reg.get('index')
                    name = reg.get('Name')
                    club_name = reg.find('CLUBNAME').text
                    if reg.find('SINGLERACE').text == 'True' and name != '20o ΑΡΜΕΝΙΖΟΝΤΑΣ ΓΙΑ ΤΟ ΠΑΙΔΙ (2 ατόμων Α+Γ)':
                        length = reg.find('LENGTH').text
                        if length is None: length = ' - '
                        course = reg.find('COURSE').text
                        frdate = str(reg.find('FRDATE').text)
                        stdate, sttime = date_analyze(frdate)
                        if reg.find('TODATE').text is not None:
                            todate = str(reg.find('TODATE').text)
                            todate, totime = date_analyze(todate)
                            regatta_list.append(
                                RaceType2(district, index, name, club_name, stdate, sttime, course, length, todate))
                        else:
                            regatta_list.append(
                                RaceType1(district, index, name, club_name, stdate, sttime, course, length))
                        df_dict = {'Ονομασία': name, 'Ημέρ': stdate, 'Ώρα': sttime, 'Διαδρομή': course,
                                   "Απόσταση": length, 'Όμιλος': club_name}
                        df = pd.concat([df, pd.DataFrame.from_records([df_dict])])
                    else:
                        obj = RaceType3(district, index, name, club_name)
                        for race in reg.findall('RACE'):
                            course = race.get('Name')
                            length = reg.find('LENGTH').text
                            if length is None: length = ' - '
                            stdate = race.find('STDATE').text
                            stdate, sttime = date_analyze(stdate)
                            stday = race.find('STDATE').get('Day')
                            obj.races.append(Race(name, stdate, sttime, course, length))
                            df_dict = {'Ονομασία': name, 'Ημέρ': stdate, 'Ώρα': sttime,
                                       'Διαδρομή': course,
                                       "Απόσταση": length, 'Όμιλος': club_name, }
                            df = pd.concat([df, pd.DataFrame.from_records([df_dict])])
                        regatta_list.append(obj)
        return regatta_list, df
