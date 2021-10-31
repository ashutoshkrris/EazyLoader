from core import app, socketio

if __name__ == '__main__':
    socketio.run(app, debug=True)
    