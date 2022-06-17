import gspread
from oauth2client.service_account import ServiceAccountCredentials

scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']

credentials = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)

gc = gspread.authorize(credentials)
sh = gc.open("conduit_8")
worksheet = sh.worksheet("8t")
list_of_lists = worksheet.get_all_values()
list_of_lists