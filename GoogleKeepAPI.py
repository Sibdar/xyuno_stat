import gkeepapi
import os


class GoogleKeepAPI:

    # `xyUNO` Note ID
    # note_id = '1ee-NbypcnofPck10MzOW3_D7U5bmPoZrXKif8Mqj_BIp6uAK6ifG3JnDeEAlJXXHD7aa'
    note_id = os.getenv('GOOGLE_API_XYUNO_NOTE_ID')
    email = os.getenv('GOOGLE_API_EMAIL')  # sibdar93@gmail.com
    app_pswrd = os.getenv('GOOGLE_API_APP_PSWRD')  # ahyqdeszarlqedjl

    def __init__(self):
        self.keep = gkeepapi.Keep()
        self.success = self.keep.login(self.email, self.app_pswrd)

    def get_xyuno_note_data(self):
        """ Get raw score data """
        return self.keep.get(self.note_id).text.split('\n')


if __name__ == '__main__':
    gk_api = GoogleKeepAPI()
    xyuno_data = gk_api.get_xyuno_note_data()
    print(xyuno_data)



