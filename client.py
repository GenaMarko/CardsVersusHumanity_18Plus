import tkinter as tk
from tkinter import ttk, messagebox
import socket
import threading


#настройки подключения к серверу
PORT = 5555

client_socket = None

nickname = ""
role = ""


# ============================================================
# ТЕСТОВОЕ СОСТОЯНИЕ ИГРЫ
#
# Позже эти данные будут приходить с server.py
# ============================================================

game_state = {
    "round": 3,

    "host": "Алекс",

    "players": [
        {
            "name": "Алекс",
            "score": 15,
            "is_host": True
        },
        {
            "name": "Михалыч",
            "score": 12,
            "is_host": False
        },
        {
            "name": "Дима",
            "score": 8,
            "is_host": False
        },
        {
            "name": "Саша",
            "score": 5,
            "is_host": False
        }
    ],

    "question": "Что я делаю, когда никто не смотрит?",

    "cards": [
        "Притворяюсь, что работаю",
        "Начинаю танцевать",
        "Ем холодильник",
        "Иду спать",
        "Забываю, зачем пришёл"
    ]
}


#обновление игрового интерфейса
def update_game_interface():
    """
    Обновляет все элементы игрового интерфейса
    на основе game_state.
    """

    #раунд
    round_label.config(
        text=f"Раунд {game_state['round']}"
    )

    #ведущий
    host_label.config(
        text=f"★ Ведущий: {game_state['host']}"
    )

    #список игроков
    for widget in players_frame.winfo_children():
        widget.destroy()

    for player in game_state["players"]:

        player_text = (
            f"{player['name']}     "
            f"{player['score']} очк."
        )

        if player["is_host"]:
            player_text = "★ " + player_text

        player_label = tk.Label(
            players_frame,
            text=player_text,
            font=("Arial", 13),
            anchor="w"
        )

        player_label.pack(
            fill="x",
            pady=5
        )

    #вопрос
    question_label.config(
        text=game_state["question"]
    )

    #карты
    for widget in cards_frame.winfo_children():
        widget.destroy()

    for index, card_text in enumerate(
        game_state["cards"]
    ):

        card_button = tk.Button(
            cards_frame,
            text=card_text,
            font=("Arial", 11),
            wraplength=150,
            justify="center",
            width=15,
            height=7,

            command=lambda card=card_text:
                select_card(card)
        )

        card_button.grid(
            row=0,
            column=index,
            padx=8,
            pady=10,
            sticky="nsew"
        )


#выбор карты
def select_card(card):
    """
    Пока просто показывает выбранную карту.

    Позже здесь будет отправка выбора
    на server.py.
    """

    messagebox.showinfo(
        "Карта выбрана",
        f"Ты выбрал:\n\n{card}"
    )


#получение данных от сервера
def receive_from_server():
    """
    Отдельный поток, который постоянно ждёт
    сообщения от сервера.

    Позже здесь будет разбор JSON-состояния игры.
    """

    global client_socket

    while True:

        try:

            data = client_socket.recv(4096)

            if not data:
                break

            message = data.decode("utf-8")

            print("Получено от сервера:")
            print(message)

            # В будущем:
            #
            # game_state = json.loads(message)
            #
            # window.after(
            #     0,
            #     update_game_interface
            # )

        except OSError:
            break


#Создание игрового окна
def open_game_interface():

    global round_label
    global host_label
    global players_frame
    global question_label
    global cards_frame

    connection_frame.destroy()

    #основной frame
    game_frame = tk.Frame(
        window
    )

    game_frame.pack(
        fill="both",
        expand=True
    )

    #верхняя панель
    top_frame = tk.Frame(
        game_frame
    )

    top_frame.pack(
        fill="x",
        padx=20,
        pady=15
    )

    round_label = tk.Label(
        top_frame,
        text="Раунд 1",
        font=("Arial", 20, "bold")
    )

    round_label.pack(
        side="left"
    )

    exit_button = tk.Button(
        top_frame,
        text="Выйти",
        font=("Arial", 11)
    )

    exit_button.pack(
        side="right"
    )

    #основная область
    main_frame = tk.Frame(
        game_frame
    )

    main_frame.pack(
        fill="both",
        expand=True,
        padx=20,
        pady=10
    )

    main_frame.columnconfigure(
        0,
        weight=1
    )

    main_frame.columnconfigure(
        1,
        weight=3
    )

    main_frame.rowconfigure(
        0,
        weight=1
    )

    #панель игроков
    players_container = tk.LabelFrame(
        main_frame,
        text="Игроки",
        font=("Arial", 13, "bold")
    )

    players_container.grid(
        row=0,
        column=0,
        sticky="nsew",
        padx=(0, 10)
    )

    host_label = tk.Label(
        players_container,
        text="★ Ведущий:",
        font=("Arial", 13, "bold"),
        anchor="w"
    )

    host_label.pack(
        fill="x",
        padx=10,
        pady=(10, 15)
    )

    players_frame = tk.Frame(
        players_container
    )

    players_frame.pack(
        fill="both",
        expand=True,
        padx=10
    )

    #область вопроса
    question_container = tk.LabelFrame(
        main_frame,
        text="Вопрос",
        font=("Arial", 13, "bold")
    )

    question_container.grid(
        row=0,
        column=1,
        sticky="nsew"
    )

    question_label = tk.Label(
        question_container,
        text="",
        font=("Arial", 20, "bold"),
        wraplength=650,
        justify="center"
    )

    question_label.pack(
        fill="both",
        expand=True,
        padx=30,
        pady=30
    )

    #Карты
    cards_container = tk.LabelFrame(
        game_frame,
        text="Ваши карты",
        font=("Arial", 13, "bold")
    )

    cards_container.pack(
        fill="x",
        padx=20,
        pady=(10, 20)
    )

    cards_frame = tk.Frame(
        cards_container
    )

    cards_frame.pack(
        fill="x",
        padx=10,
        pady=10
    )

    update_game_interface()


#Подключение к серверу
def connect_to_server():

    global client_socket
    global nickname
    global role

    server_ip = ip_entry.get().strip()

    nickname = nickname_entry.get().strip()

    role = role_combobox.get()

    if not server_ip:

        messagebox.showwarning(
            "Ошибка",
            "Введите IP-адрес сервера."
        )

        return

    if not nickname:

        messagebox.showwarning(
            "Ошибка",
            "Введите никнейм."
        )

        return

    try:

        client_socket = socket.socket(
            socket.AF_INET,
            socket.SOCK_STREAM
        )

        client_socket.settimeout(5)

        client_socket.connect(
            (
                server_ip,
                PORT
            )
        )

        message = client_socket.recv(
            4096
        ).decode("utf-8")

        print(
            "Сервер:",
            message
        )

        thread = threading.Thread(
            target=receive_from_server,
            daemon=True
        )

        thread.start()

        open_game_interface()

    except socket.timeout:

        messagebox.showerror(
            "Ошибка",
            "Сервер не ответил."
        )

        client_socket.close()

    except ConnectionRefusedError:

        messagebox.showerror(
            "Ошибка",
            "Сервер отклонил подключение."
        )

        client_socket.close()

    except OSError as error:

        messagebox.showerror(
            "Ошибка",
            str(error)
        )

        client_socket.close()


#главное окно
window = tk.Tk()

window.title(
    "Карточная игра"
)

window.geometry(
    "1100x700"
)

window.minsize(
    800,
    600
)


#Интерфейс подключения
connection_frame = tk.Frame(
    window
)

connection_frame.pack(
    fill="both",
    expand=True
)


title_label = tk.Label(
    connection_frame,
    text="Карточная игра",
    font=("Arial", 26, "bold")
)

title_label.pack(
    pady=(60, 30)
)


#Имя
nickname_label = tk.Label(
    connection_frame,
    text="Никнейм:",
    font=("Arial", 13)
)

nickname_label.pack()

nickname_entry = tk.Entry(
    connection_frame,
    width=35,
    font=("Arial", 13)
)

nickname_entry.pack(
    pady=(5, 20)
)


#ip
ip_label = tk.Label(
    connection_frame,
    text="IP-адрес сервера:",
    font=("Arial", 13)
)

ip_label.pack()

ip_entry = tk.Entry(
    connection_frame,
    width=35,
    font=("Arial", 13)
)

ip_entry.insert(
    0,
    "127.0.0.1"
)

ip_entry.pack(
    pady=(5, 20)
)


#Роль
role_label = tk.Label(
    connection_frame,
    text="Роль:",
    font=("Arial", 13)
)

role_label.pack()

role_combobox = ttk.Combobox(
    connection_frame,
    values=[
        "Игрок",
        "Ведущий"
    ],
    state="readonly",
    width=32,
    font=("Arial", 13)
)

role_combobox.current(0)

role_combobox.pack(
    pady=(5, 30)
)

#Подключение
connect_button = tk.Button(
    connection_frame,
    text="Подключиться",
    width=20,
    height=2,
    font=("Arial", 13),
    command=connect_to_server
)

connect_button.pack()

window.mainloop()