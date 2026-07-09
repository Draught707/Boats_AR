import http.server
import socketserver
import os
import socket

# Переходим в папку с проектом
os.chdir(os.path.dirname(os.path.abspath(__file__)))


def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return '127.0.0.1'


class CustomHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    # Отключаем автоматическое перенаправление на HTTPS
    def do_GET(self):
        # Проверяем, не пытается ли браузер использовать HTTPS
        if self.headers.get('X-Forwarded-Proto') == 'https':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b"<h1>Please use HTTP, not HTTPS</h1>")
            return

        # Обрабатываем обычные GET-запросы
        return super().do_GET()

    def do_HEAD(self):
        return super().do_HEAD()

    def log_message(self, format, *args):
        # Фильтруем мусорные HTTPS-запросы
        if 'Bad request version' in str(args):
            return
        super().log_message(format, *args)

    def end_headers(self):
        # Добавляем заголовки для безопасности
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        # Запрещаем переход на HTTPS
        self.send_header('Strict-Transport-Security', 'max-age=0')
        super().end_headers()


PORT = 8000
Handler = CustomHTTPRequestHandler

# Создаем папки если их нет
os.makedirs('static/models', exist_ok=True)

# Создаем сервер
try:
    with socketserver.TCPServer(("0.0.0.0", PORT), Handler) as httpd:
        local_ip = get_local_ip()
        print(f"\n{'=' * 60}")
        print(f"✅ HTTP сервер запущен!")
        print(f"⚠️  ВАЖНО: используйте ТОЛЬКО HTTP!")
        print(f"📱 Для телефона: http://{local_ip}:{PORT}")
        print(f"💻 Для компьютера: http://127.0.0.1:{PORT}")
        print(f"{'=' * 60}\n")
        print("📁 Ваши файлы должны быть в папке:")
        print(f"   {os.getcwd()}")
        print("\n⚠️  НЕ используйте HTTPS (https://)")
        print("🔄 Для остановки нажмите Ctrl+C\n")
        httpd.serve_forever()
except KeyboardInterrupt:
    print("\n✅ Сервер остановлен")
except Exception as e:
    print(f"\n❌ Ошибка: {e}")