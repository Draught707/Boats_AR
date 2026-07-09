from flask import Flask, render_template
import socket

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return '127.0.0.1'


if __name__ == '__main__':
    local_ip = get_local_ip()

    print(f"\n{'=' * 60}")
    print(f"✅ Сервер успешно запущен!")
    print(f"📱 Для телефона: http://{local_ip}:5000")
    print(f"💻 Для компьютера: http://127.0.0.1:5000")
    print(f"{'=' * 60}\n")

    # Простейший запуск без лишних импортов
    app.run(host='192.168.0.152', port=5000, debug=False)