<Root>:
    orientation:'vertical'
    Label:
        text:'Введите своё имя'
    TextInput:
        id:form
    Label:
        id:field
    Button:
        text: 'OK'
        on_press:
            field.text = 'Привет, '+form.text+'!'