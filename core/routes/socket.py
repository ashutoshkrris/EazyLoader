from flask_socketio import send
from threading import Thread
from time import sleep
from flask import session
from core import socketio, status
from core.routes.youtube import start_preparation
from core.routes.slideshare import start_slide_preparation


@socketio.on('message')
def socket_bidirct(msg):

    if msg[0] == "Youtube has connected!":
        print("yt ready")
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

    elif msg[0] == "Slideshare ready!":
        print("ss ready")
        url = session['slide_url']
        t = Thread(target=start_slide_preparation, args=(
            msg[0], url,), daemon=True)
        t.start()

        while True:
            print("Iha aaye")
            sleep(2)
            print(status)
            if status.get(msg[0]) == "Download-Ready":
                print("Bhejiye n rhe")
                send("Download-Ready")
                break
        del status[msg[0]]


    if msg[0] == "User has connected!":
        print(msg[0])
