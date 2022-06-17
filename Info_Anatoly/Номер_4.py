def copy_student_marks(surname: str, row_number: int):
    scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']

    credentials = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)

    gc = gspread.authorize(credentials)
    sh = gc.open("conduit_8")
    t_t = sh.worksheet('8t')
    t_s = sh.worksheet('8s')
    T_my  = sh.worksheet('Кирюшин')
    try:
        t_t = sh.worksheet('8t')
    except Exception:
        t_t = sh.worksheet('8s')

    cell = t_t.find('Кирюшин')
    nombers  = t_t.row_values(2)
    row   = t_t.row_values(cell.row)
    T_my.update_cell(1, 3, 'Pillow')
    if (row_number==1 or 2):
       raise Except("Это шапка, поэтому нельзя создавать")
    for i in range(len(row)):
        T_my.update_cell(2, i+1, nombers[i])
        T_my.update_cell(row_number, i+1, row[i])
copy_student_marks('Кирюшин',4)