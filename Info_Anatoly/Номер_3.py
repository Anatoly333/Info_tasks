import gspread
from oauth2client.service_account import ServiceAccountCredentials
def create_table_without_duplicate(sheet_name: str, row_number: int, col_number: int):
    scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']

    credentials = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)

    gc = gspread.authorize(credentials)
    sh = gc.open("conduit_8")
    try:
        worksheet = sh.worksheet(sheet_name)
        sh.del_worksheet(worksheet)
    except Exception: 
        pass
    worksheet = sh.add_worksheet(title=sheet_name, rows=row_number, cols=col_number)
create_table_without_duplicate("Кирюшин", 30,20)