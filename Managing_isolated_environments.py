import os
import argparse
import random
import string
import libtmux
import time

def generate_token():
    token_length = 16
    characters = string.ascii_letters + string.digits
    return "".join(random.choice(characters) for i in range(token_length))

def generate_session_name():
    return f"session_{int(time.time())}_{random.randint(1000, 9999)}"

def start_notebook(port, token, notebook_dir):
    tmux_session_name = generate_session_name()
    tmux_session = server.new_session(session_name=tmux_session_name)
    tmux_window = tmux_session.new_window(attach=False)
    tmux_pane = tmux_window.panes[0]
    tmux_pane.send_keys(f"jupyter notebook --ip 127.0.0.1 --port {port} --no-browser --NotebookApp.token='{token}' --NotebookApp.notebook_dir='{notebook_dir}'")
    return tmux_session, tmux_pane

def start(window_num):
    notebooks = []
    current_dir = os.getcwd()
    for i in range(window_num):
        port = random.randint(8000, 65535)
        token = generate_token()
        notebook_dir = f"{current_dir}/dir{i}"
        os.makedirs(notebook_dir, exist_ok=True)

        tmux_session, tmux_pane = start_notebook(port, token, notebook_dir)
        notebooks.append((i + 1, port, token, tmux_session.get("session_name")))
        time.sleep(3)

    print("Запущены следующие окружения:")
    for i, port, token, session_name in notebooks:
        print(f"Окружение {i}: Порт {port}, Токен {token}, Сессия {session_name}")


if __name__ == "main":
    parser = argparse.ArgumentParser(description="Управление изолированными окружениями Jupyter Notebook.")
    parser.add_argument("arg", nargs="?", type=int)
    parser.add_argument("command", choices=["start", "stop", "stop_all"])
    args = parser.parse_args()

    server = libtmux.Server()

    if args.command == "start":
        if args.arg is None:
            print("Необходимо указать количество окружений.")
        else:
            start(args.arg)

    elif args.command == "stop":
        if args.arg is None:
            print("Необходимо указать номер окружения для остановки.")
        else:
            for session_to_stop in server.list_sessions():
                session_name = session_to_stop.get("session_name")
                if session_name and session_name.startswith("session_") and session_name.endswith(str(args.arg)):
                    session_to_stop.kill_session()
                    print(f"Окружение {args.arg} остановлено.")
                    break
            else:
                print(f"Окружение {args.arg} не найдено.")

    elif args.command == "stop_all":
        for session_to_stop in server.list_sessions():
            if session_to_stop.get("session_name", "").startswith("session_"):
                session_to_stop.kill_session()
        print("Все окружения остановлены.")