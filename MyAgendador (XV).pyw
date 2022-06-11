from tkinter import ttk, messagebox, Frame, Button, Label, Entry, Tk, Menu, mainloop
from tkinter.ttk import Style, Progressbar
import time
from datetime import datetime, timedelta
from time import sleep
import mysql.connector
mydb = mysql.connector.connect(host='192.168.0.7',
  charset='utf8',
  user='york',
  passwd='osan2030',
  database='clinica')

def task():
    global data_amanha_string
    global data_hoje_string
    global hora_string
    global list_medicos
    global list_pacientes
    global mycursor
    global mydb
    pbar['value'] = 5
    pbar.update()
    now = datetime.now()
    tomorrow = datetime.now() + timedelta(days=1)
    data_hoje_string = now.strftime('%Y-%m-%d')
    data_amanha_string = tomorrow.strftime('%Y-%m-%d')
    hora_string = now.strftime('%H:%M:%S')
    pbar['value'] = 15
    pbar.update()
    pbar['value'] = 25
    pbar.update()
    mydb = mysql.connector.connect(host='192.168.0.7',
      charset='utf8',
      user='york',
      passwd='osan2030',
      database='clinica')
    mycursor = mydb.cursor()
    mycursor.execute("select distinct p.nome from cl_agenda a inner join cl_profissional as p on a.UUIDPROF = p.UUIDPROF inner join cl_ga_local as l on a.LOCAL = l.codlocal where a.MOM_INI >= {d '" + data_hoje_string + "'} and a.MOM_FIN < {d '" + data_amanha_string + "'} and l.descricao = 'XV de Novembro (Santos)' and a.senha is null order by p.nome")
    list_medicos = [x[0] for x in mycursor.fetchall()]
    pbar['value'] = 70
    pbar.update()
    time.sleep(0.05)
    mycursor.execute("select distinct nome from cl_agenda a inner join cl_ga_local as l on a.LOCAL = l.codlocal where MOM_INI >= {d '" + data_hoje_string + "'} and MOM_FIN < {d '" + data_amanha_string + "'} and l.descricao = 'XV de Novembro (Santos)' and a.senha is null order by nome")
    list_pacientes = ''
    list_pacientes = [x[0] for x in mycursor.fetchall()]
    pbar['value'] = 100
    pbar.update()
    time.sleep(0.05)
    janela_loading.destroy()


def senha_atual():
    global senha
    mydb = mysql.connector.connect(host='192.168.0.7',
      charset='utf8',
      user='york',
      passwd='osan2030',
      database='paineladc')
    mycursor = mydb.cursor()
    mycursor.execute('select Senha from conta')
    senha = mycursor.fetchone()
    lb6['text'] = senha[0]


def definir_senha():
    global ed3
    global janela_definir_senha
    janela_definir_senha = Tk()
    lb10 = Label(janela_definir_senha, text='Definir senha')
    lb11 = Label(janela_definir_senha, text='')
    bt4 = Button(janela_definir_senha, width=20, text='Enviar', command=bt_onclick_definir_senha)
    ed3 = Entry(janela_definir_senha)
    lb11.pack()
    lb10.pack()
    ed3.pack()
    bt4.pack()
    janela_definir_senha.title('')
    janela_definir_senha.resizable(False, False)
    janela_definir_senha.geometry('200x120+860+400')
    janela_definir_senha.mainloop()
    bt_onclick_definir_senha()


def bt_onclick_definir_senha():
    a = ed3.get()
    mydb = mysql.connector.connect(host='192.168.0.7',
      charset='utf8',
      user='york',
      passwd='osan2030',
      database='paineladc')
    mycursor = mydb.cursor()
    try:
        int(a)
    except ValueError:
        messagebox.showerror('Erro', 'A senha deve conter apenas números')
        janela_definir_senha.destroy()
        definir_senha()

    if len(a) > 3:
        messagebox.showerror('Erro', 'A senha deve conter no máximo 3 números')
        janela_definir_senha.destroy()
        definir_senha()
    if a != '':
        if int(a):
            if len(a) <= 3:
                sql = 'update conta set senha = ' + a + ' where senha >= 0'
                mycursor.execute(sql)
                mydb.commit()
                janela_definir_senha.destroy()
                senha_atual()


def bt_onclick_enviar():
    global combo2
    b = combo2.get()
    c = ed1.get()
    mydb = mysql.connector.connect(host='192.168.0.7',
      charset='utf8',
      user='york',
      passwd='osan2030',
      database='clinica')
    if b == '':
        messagebox.showerror('Erro', 'Selecione o Paciente')
    try:
        int(c)
    except ValueError:
        messagebox.showerror('Erro', 'A senha deve conter apenas números')

    if len(c) > 3:
        messagebox.showerror('Erro', 'A senha deve conter no máximo 3 números')
    if b != '':
        if c != '':
            if int(c):
                if len(c) <= 3:
                    mycursor = mydb.cursor()
                    sql = 'update cl_agenda set hrecp = date_format(now(), "%H:%i:%s"), senha = ' + c + ' where nome = "' + b + '" and (MOM_INI >= {d "' + data_hoje_string + '"} and MOM_FIN < {d "' + data_amanha_string + '"})'
                    mycursor.execute(sql)
                    mydb.commit()
                    messagebox.showinfo('Sucesso', 'O status do paciente foi atualizado !!!')


def bt_onclick_buscar():
    global combo2
    global list_pacientes
    a = combo1.get()
    if a == '':
        messagebox.showerror('Erro', 'Selecione o profissional')
    else:
        mycursor.execute("select distinct a.nome from cl_agenda a inner join cl_profissional as p on a.UUIDPROF = p.UUIDPROF inner join cl_ga_local as l on a.LOCAL = l.codlocal where (MOM_INI >= {d '" + data_hoje_string + "'} and MOM_FIN < {d '" + data_amanha_string + "'} and l.descricao = 'XV de Novembro (Santos)') and p.nome = '" + a + "' order by a.nome")
        list_pacientes = [x[0] for x in mycursor.fetchall()]
        combo2['state'] = 'readonly'
        combo2['values'] = list_pacientes
        combo2 = ttk.Combobox(janela, values=list_pacientes, width=60, state='readonly')
        combo2.place(x=80, y=220)


def incrementar_senha():
    a = combo3.get()
    mydb = mysql.connector.connect(host='192.168.0.7',
      charset='utf8',
      user='york',
      passwd='osan2030',
      database='paineladc')
    if a == '':
        messagebox.showerror('Erro', 'Selecione o caixa')
    else:
        if a == 'Caixa 1':
            guiche = 1
        else:
            if a == 'Caixa 2':
                guiche = 2
            else:
                if a == 'Caixa 3':
                    guiche = 3
                else:
                    if a == 'Caixa 4':
                        guiche = 4
                    else:
                        if a == 'Caixa 5':
                            guiche = 5
        senha_atual()
        senha_incrementada = int(senha[0]) + 1
        mycursor = mydb.cursor()
        sql = 'update conta set senha = ' + str(senha_incrementada) + ' where senha = ' + str(int(senha[0]))
        mycursor.execute(sql)
        sql = 'insert into painelsenha (senha, guiche, datacad, hcad) values (' + str(senha_incrementada) + ', ' + str(guiche) + ', now(), hour(now()));'
        mycursor.execute(sql)
        mydb.commit()
        senha_atual()


janela_loading = Tk()
w = janela_loading.winfo_reqwidth()
h = janela_loading.winfo_reqheight()
ws = janela_loading.winfo_screenwidth()
hs = janela_loading.winfo_screenheight()
x = ws / 2 - w / 2
y = hs / 2 - h / 2
janela_loading.geometry('300x200+800+350')
janela_loading.overrideredirect(True)
janela_loading.title('Painel de senha')
label = Label(janela_loading, text='Iniciando a aplicação...')
label.place(x=85, y=70)
janela_loading.after(200, task)
style = Style()
style.configure('black.Horizontal.TProgressbar', background='grey')
pbar = Progressbar(janela_loading, length=200, style='black.Horizontal.TProgressbar')
pbar['maximum'] = 100
pbar['value'] = 10
pbar.place(x=50, y=100)
janela_loading.mainloop()
janela = Tk()
janela.title('MyAgendador XV')
janela.resizable(False, False)
window_height = 450
window_width = 700
screen_width = janela.winfo_screenwidth()
screen_height = janela.winfo_screenheight()
x_cordinate = int(screen_width / 2 - window_width / 2)
y_cordinate = int(screen_height / 2 - window_height / 2)
lb1 = Label(janela, text='Profissional')
lb2 = Label(janela, text='Paciente')
lb3 = Label(janela, text='Senha')
lb4 = Label(janela, text='Ultima senha:')
lb6 = Label(janela, text='')
combo1 = ttk.Combobox(janela, values=list_medicos, width=60, state='readonly')
combo2 = ttk.Combobox(janela, values=list_pacientes, width=60, state='disabled')
combo3 = ttk.Combobox(janela, values=['Caixa 1', 'Caixa 2', 'Caixa 3', 'Caixa 4', 'Caixa 5'], width=20, state='readonly')
bt1 = Button(janela, width=20, text='Enviar', command=bt_onclick_enviar)
bt2 = Button(janela, width=20, text='Buscar', command=bt_onclick_buscar)
bt4 = Button(janela, width=20, text='Proxima senha', command=incrementar_senha)
ed1 = Entry()
lb4.place(x=80, y=20)
lb6.place(x=80, y=50)
lb1.place(x=80, y=120)
combo1.place(x=80, y=150)
lb2.place(x=80, y=190)
combo2.place(x=80, y=220)
lb3.place(x=80, y=260)
ed1.place(x=80, y=290)
bt1.place(x=80, y=330)
bt2.place(x=500, y=150)
combo3.place(x=250, y=20)
bt4.place(x=250, y=50)
menubar = Menu(janela)
file = Menu(menubar, tearoff=0)
menubar.add_cascade(label='Arquivo', menu=file)
file.add_command(label='Definir Senha', command=definir_senha)
file.add_separator()
file.add_command(label='Sair', command=(janela.destroy))
help_ = Menu(menubar, tearoff=0)
menubar.add_cascade(label='Ajuda', menu=help_)
help_.add_command(label='Help Desk', command=None)
help_.add_separator()
help_.add_command(label='Sobre', command=None)
senha_atual()
janela.geometry('{}x{}+{}+{}'.format(window_width, window_height, x_cordinate, y_cordinate))
janela.config(menu=menubar)
janela.mainloop()