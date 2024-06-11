import requests
import os


class MyFile():

    def resource_path(self,relative):
        return os.path.join(
            os.environ.get(
                "_MEIPASS2",
                os.path.abspath(".")
            ),
            relative
        )

    def get_respone(self):
        # Αρχική ανάγνωση αρχείου από διαδίκτυο
        URL = 'https://offshore.org.gr/index.php?mx=Race_Schedule_2022&x=Program.xsl'
        response = requests.get(URL)
        return response

    def write_file(self):
        with open(self.resource_path("file.xml"), 'wb') as file:
            file.write(self.get_respone().content)


    def update_file(self):
        try:
            os.remove(self.resource_path("file.xml"))
        except OSError:
            pass
        self.open_file()

    def open_file(self):
        try:
            file = open(self.resource_path('file.xml'), 'rb')
            return file
        except FileNotFoundError:
            self.write_file()
    def copy_file(self,source,target):
        try:
            with open(source,'r') as f:
                contents = f.read()
            with open(f'{target}','w') as f:
                f.write(contents)
        except FileNotFoundError:
            print("File not Found Error")