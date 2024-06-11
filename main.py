import os
os.environ['KIVY_TEXT'] = 'pil'
import tkinter as tk
from tkinter import filedialog
from kivy.lang import Builder
from kivy.properties import StringProperty
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen
from tabulate import tabulate
from MyFile import *
from WebScrapper import *
from MyCal import *
from google_api import *
from ms_graph_api import *
from kivymd.app import MDApp

Window.maximize()
Window.icon = "images/logo.png"


class FirstWindow(Screen):
    pass


class SecondScreen(Screen):
    MyFile().write_file()
    races = []
    df = pd.DataFrame()
    current_datetime = current_date()
    screen = StringProperty()
    title = StringProperty()
    myCalendar = MyCal()
    district = " "

    def spinner_choice(self, value):
        self.ids.screen_title.text = "Περιφέρεια: {}".format(value)
        wbs = WebScrapper(file, self.ids.spinner_id.text)
        SecondScreen.races, SecondScreen.df = wbs.retrieve_data()
        self.ids.main_screen.text = tabulate(SecondScreen.df, showindex=False, stralign="left",
                                             colalign=("left", "center", "center",), tablefmt='rst')
        SecondScreen.district = value
        return SecondScreen.district

    def next_race_retrieve(self):
        try:
            condition = SecondScreen.df['Ημέρ'] > datetime.now()
            df_future = SecondScreen.df[condition].sort_values(['Ημέρ'])
            self.ids.main_screen.text = str(df_future.iloc[0].to_string())
        except:
            s = "Παρακαλώ επιλέξτε περιφέρεια"
            self.ids.main_screen.text = "{:^200}".format(s)

    def open_url(self):
        try:
            webbrowser.open('https://offshore.org.gr/index.php', new=0)
        except:
            self.ids.main_screen.text = "Αποτυχία σύνδεσης με την σελίδα."

    def save_file(self):
        if len(SecondScreen.races) == 0:
            s = "Παρακαλώ επιλέξτε περιφέρεια"
            self.ids.main_screen.text = f" {s:^160}"
        else:
            root = tk.Tk()
            root.withdraw()
            file_path = filedialog.asksaveasfilename(initialdir="C:/", title="Save file", defaultextension=".ics",
                                                     filetypes=(("Calendar file", "*.ics"), ("All Files", "*.*")))
            if len(file_path) == 0:
                return
            else:
                try:
                    SecondScreen.myCalendar.icalendar_initial()
                    for regatta in SecondScreen.races:
                        SecondScreen.myCalendar.write_event_to_file(SecondScreen.myCalendar.create_new_event(regatta),
                                                                    file_path)
                    self.ids.main_screen.text = f"Το αρχείο αποθηκεύτηκε επιτυχώς στην τοποθεσία {file_path}"
                except IOError:
                    self.ids.main_screen.text = "Αποτυχία αποθήκευσης αρχείου"
                    return

    def google_api_connection(self):
        if len(SecondScreen.races) == 0:
            s = "Παρακαλώ επιλέξτε περιφέρεια"
            self.ids.main_screen.text = f" {s:^160}"
        else:
            self.ids.main_screen.text = "Παρακαλώ περιμένετε........"
            google_api = Google_Api(SecondScreen.district)
            for regatta in SecondScreen.races:
                event = SecondScreen.myCalendar.google_calendar_event(regatta)
                if isinstance(event, list):
                    for e in event:
                        google_api.insert_event(e)
                else:
                    google_api.insert_event(event)
            s = "Επιτυχής εισαγωγή ημερολογίου"
            self.ids.main_screen.text = f" {s:^180}"

    def ms_graph_api_connection(self):
        if len(SecondScreen.races) == 0:
            s = "Παρακαλώ επιλέξτε περιφέρεια"
            self.ids.main_screen.text = f" {s:^160}"
        else:
            s = "Παρακαλώ περιμένετε......"
            self.ids.main_screen.text = s
            ms_graph_api = Ms_Graph_api()
            for regatta in SecondScreen.races:
                event = SecondScreen.myCalendar.ms_calendar_event(regatta)
                if isinstance(event, list):
                    for e in event:
                        ms_graph_api.insert_ms_event(e)
                else:
                    ms_graph_api.insert_ms_event(event)
            s = "Επιτυχής εισαγωγή ημερολογίου"
            self.ids.main_screen.text = f" {s:^180}"

    def update_calendar(self):
        MyFile().update_file()
        s = "Επιτυχής ενημέρωση του ημερολογίου"
        self.ids.main_screen.text = f" {s:^180}"

    def user_manual(self):
        txt = " "
        try:
            with open("txt/readme.txt", "r", encoding='utf-8') as f:
                self.ids.screen_title.text = "Οδηγίες Χρήσης"
                txt += f.read()
                self.ids.main_screen.text = txt
        except FileNotFoundError:
            return

    def about_app(self):
        txt = " "
        try:
            with open("txt/about.txt", "r", encoding='utf-8') as f:
                txt += f.read()
                self.ids.main_screen.text = txt
        except FileNotFoundError:
            return

    def quit_app(self):
        os._exit(0)

    def restart(self):
        MDApp.get_running_app().restart()


class WindowManager(ScreenManager):
    pass


class SailingCalendarApp(MDApp):

    def build(self):
        self.icon = "images/logo.png"
        self.title = "Sailing Calendar"
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "DeepPurple"
        return Builder.load_file('kv/SailingCalendar.kv')

    def restart(self):
        self.root.clear_widgets()
        self.stop()
        return SailingCalendarApp().run()


if __name__ == '__main__':
    file = MyFile().open_file()
    SailingCalendarApp().run()
