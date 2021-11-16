from core import socketio, status
from flask import session
from flask_socketio import send
from threading import Thread
from time import sleep
from core.routes.slideshare import start_slide_preparation
from core.routes.youtube import start_preparation


@socketio.on('message')
def socket_bidirct(msg):
    if msg[0] != "User has connected!" and len(msg) == 1:
        url = session['slide_url']
        t = Thread(target=start_slide_preparation, args=(
            msg[0], url,), daemon=True)
        t.start()

        while True:
            sleep(2)
            if status.get(f"slide_{msg[0]}") == "Download-Ready":
                send("Download-Ready")
                break
        del status[f"slide_{msg[0]}"]

    elif msg[0] != "User has connected!":
        url = session['video_link']
        t = Thread(target=start_preparation, args=(
            msg[0], url, msg[1],), daemon=True)
        t.start()

        while True:
            sleep(2)
            if status.get(msg[0]) == "Download-Ready":
                send("Download-Ready")
                break
        del status[msg[0]]

    if msg[0] == "User has connected!":
        print(msg[0])
