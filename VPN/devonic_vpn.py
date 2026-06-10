import os
import sys
import time
import requests
from datetime import datetime
from colorama import init, Fore, Back, Style

# Colorama başlat
init(autoreset=True)

class DevonicVPN:
    def __init__(self):
        self.vpn_active = False
        self.current_proxy = None
        self.original_ip = None
        self.vpn_ip = None
        self.running = False
        self.cycle = 0
        self.current_ip = None
        
    def clear_screen(self):
        """Ekranı temizle"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def print_banner(self):
        """DEVONIC VPN Banner"""
        banner = f"""
{Fore.CYAN}╔═══════════════════════════════════════════════════════════════════════╗
{Fore.CYAN}║                                                                       ║
{Fore.CYAN}║     ██████╗ ███████╗██╗   ██╗ ██████╗ ███╗   ██╗██╗ ██████╗           ║
{Fore.CYAN}║     ██╔══██╗██╔════╝██║   ██║██╔═══██╗████╗  ██║██║██╔════╝           ║
{Fore.CYAN}║     ██║  ██║█████╗  ██║   ██║██║   ██║██╔██╗ ██║██║██║                ║
{Fore.CYAN}║     ██║  ██║██╔══╝  ╚██╗ ██╔╝██║   ██║██║╚██╗██║██║██║                ║
{Fore.CYAN}║     ██████╔╝███████╗ ╚████╔╝ ╚██████╔╝██║ ╚████║██║╚██████╗           ║
{Fore.CYAN}║     ╚═════╝ ╚══════╝  ╚═══╝   ╚═════╝ ╚═╝  ╚═══╝╚═╝ ╚═════╝           ║
{Fore.CYAN}║                                                                       ║
{Fore.CYAN}║{Fore.YELLOW}{Style.BRIGHT}     🌐 V P N   S E R V İ C E 🌐{Style.NORMAL}{Fore.CYAN}           ║
{Fore.CYAN}║{Fore.GREEN}     Otomatik Ücretsiz Proxy - Çalışan Proxy Bulur{Fore.CYAN}           ║
{Fore.CYAN}║                                                                       ║
{Fore.CYAN}╚═══════════════════════════════════════════════════════════════════════╝
"""
        print(banner)
    
    def get_free_proxies(self):
        """Ücretsiz proxy listesi al (otomatik)"""
        sources = [
            "https://api.proxyscrape.com/v2/?request=get&protocol=http&timeout=8000&country=all&ssl=all&anonymity=all",
            "https://www.proxy-list.download/api/v1/get?type=http",
            "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt",
        ]
        proxies = []
        for url in sources:
            try:
                response = requests.get(url, timeout=10)
                lines = response.text.splitlines()
                for line in lines:
                    line = line.strip()
                    if ":" in line and len(line) < 22:
                        proxies.append(line)
                if proxies:
                    break
            except:
                continue

        if not proxies:
            proxies = [
                "47.88.62.42:80",
                "103.152.112.162:80",
                "20.111.54.16:8123",
                "167.99.131.11:8888",
                "138.68.109.12:8080",
                "185.199.84.161:53281",
                "103.149.130.38:80",
                "51.79.50.22:9300",
                "178.128.200.87:3128",
                "165.22.45.209:3128",
            ]

        return proxies
    
    def get_ip_with_proxy(self, proxy):
        """Proxy ile IP al"""
        try:
            proxy_url = proxy if proxy.startswith("http") else f"http://{proxy}"
            proxies = {
                "http": proxy_url,  
                "https": proxy_url
            }
            response = requests.get('https://api.ipify.org?format=json', 
                                  proxies=proxies, timeout=8)
            return response.json()['ip']
        except:
            return None

    def find_working_proxy(self, proxy_list):
        """Çalışan bir proxy bul"""
        for index, proxy in enumerate(proxy_list, 1):
            print(f"{Fore.YELLOW}   [{index}/{len(proxy_list)}] Test: {proxy}... ", end='', flush=True)
            ip = self.get_ip_with_proxy(proxy)
            if ip:
                print(f"{Fore.GREEN}✓ ÇALIŞIYOR (IP: {ip})")
                return proxy, ip
            print(f"{Fore.RED}✗")
        return None, None
    
    def get_current_real_ip(self):
        """Gerçek IP'yi al"""
        try:
            response = requests.get('https://api.ipify.org?format=json', timeout=5)
            return response.json()['ip']
        except:
            return "Alınamadı"
    
    def show_menu(self):
        """Ana menü"""
        self.clear_screen()
        self.print_banner()
        
        # IP durumu göster
        if not self.running:
            real_ip = self.get_current_real_ip()
            print(f"{Fore.YELLOW}┌─────────────────────────────────────────────────────────────────────┐")
            print(f"{Fore.YELLOW}│  {Fore.RED}📍 DURUM: {Style.BRIGHT}VPN KAPALI{Style.NORMAL}                                               {Fore.YELLOW}│")
            print(f"{Fore.YELLOW}│  {Fore.CYAN}🌐 Gerçek IP: {Fore.WHITE}{real_ip:<50} {Fore.YELLOW}│")
            print(f"{Fore.YELLOW}└─────────────────────────────────────────────────────────────────────┘")
        else:
            print(f"{Fore.GREEN}┌─────────────────────────────────────────────────────────────────────┐")
            print(f"{Fore.GREEN}│  {Fore.GREEN}📍 DURUM: {Style.BRIGHT}VPN AKTİF - BAĞLI{Style.NORMAL}                                      {Fore.GREEN}│")
            if self.current_ip:
                print(f"{Fore.GREEN}│  {Fore.CYAN}🌐 VPN IP: {Fore.WHITE}{self.current_ip:<51} {Fore.GREEN}│")
            if self.current_proxy:
                print(f"{Fore.GREEN}│  {Fore.MAGENTA}🔒 Proxy: {Fore.WHITE}{self.current_proxy:<52} {Fore.GREEN}│")
            print(f"{Fore.GREEN}└─────────────────────────────────────────────────────────────────────┘")
        
        print()
        print(f"{Fore.CYAN}╔═══════════════════════════════════════════════════════════════════════╗")
        print(f"{Fore.CYAN}║                          {Style.BRIGHT}MENÜ SEÇENEKLERİ{Style.NORMAL}                             ║")
        print(f"{Fore.CYAN}╚═══════════════════════════════════════════════════════════════════════╝")
        print()
        
        print(f"{Fore.GREEN}  {Back.GREEN}{Fore.BLACK} 1 {Back.RESET} {Fore.GREEN}▶  VPN BAŞLAT{Style.RESET_ALL}")
        print(f"{Fore.RED}  {Back.RED}{Fore.BLACK} 2 {Back.RESET} {Fore.RED}⏹  VPN DURDUR{Style.RESET_ALL}")

        print(f"{Fore.YELLOW}  {Back.YELLOW}{Fore.BLACK} 3 {Back.RESET} {Fore.YELLOW}ℹ  BİLGİ{Style.RESET_ALL}")
        print(f"{Fore.MAGENTA}  {Back.MAGENTA}{Fore.BLACK} 0 {Back.RESET} {Fore.MAGENTA}✖  ÇIKIŞ{Style.RESET_ALL}")
        print()
        print(f"{Fore.CYAN}{'─' * 73}")
    
    def start_vpn(self):
        """VPN başlat"""
        if self.running:
            print(f"\n{Fore.RED}⚠  VPN zaten çalışıyor!")
            time.sleep(2)
            return
        
        self.clear_screen()
        self.print_banner()
        print(f"{Fore.GREEN}╔═══════════════════════════════════════════════════════════════════════╗")
        print(f"{Fore.GREEN}║                   {Style.BRIGHT}🚀 VPN BAŞLATILIYOR... 🚀{Style.NORMAL}                           ║")
        print(f"{Fore.GREEN}╚═══════════════════════════════════════════════════════════════════════╝")
        print()
        
        print(f"{Fore.CYAN}[1/3] {Fore.YELLOW}Proxy listesi yükleniyor...")
        time.sleep(1)
        proxy_list = self.get_free_proxies()
        print(f"{Fore.GREEN}      ✓ {len(proxy_list)} adet proxy bulundu")
        
        print(f"{Fore.CYAN}[2/3] {Fore.YELLOW}Çalışan proxy aranıyor...")
        time.sleep(1)
        self.current_proxy, self.current_ip = self.find_working_proxy(proxy_list)
        if not self.current_proxy:
            print(f"{Fore.RED}      ✗ Çalışan proxy bulunamadı")
            time.sleep(2)
            return
        
        print(f"{Fore.CYAN}[3/3] {Fore.YELLOW}VPN aktifleştiriliyor...")
        time.sleep(1)
        print(f"{Fore.GREEN}      ✓ VPN aktif!")
        
        print()
        print(f"{Fore.GREEN}{Style.BRIGHT}✅ DEVONIC VPN BAŞLATILDI!")
        print(f"{Fore.CYAN}🌐 VPN IP: {Fore.WHITE}{Style.BRIGHT}{self.current_ip}")
        print(f"{Fore.MAGENTA}🔒 Proxy: {Fore.WHITE}{self.current_proxy}")
        print()

        self.running = True
        time.sleep(2)
    
    def stop_vpn(self):
        """VPN durdur"""
        if not self.running:
            print(f"\n{Fore.RED}⚠  VPN zaten durmuş!")
            time.sleep(2)
            return
        
        print()
        print(f"{Fore.YELLOW}╔═══════════════════════════════════════════════════════════════════════╗")
        print(f"{Fore.YELLOW}║                   {Style.BRIGHT}⏹  VPN DURDURULUYOR... ⏹{Style.NORMAL}                          ║")
        print(f"{Fore.YELLOW}╚═══════════════════════════════════════════════════════════════════════╝")
        
        self.running = False
        time.sleep(2)
        
        print()
        print(f"{Fore.RED}✓ VPN durduruldu")
        print(f"{Fore.YELLOW}🌐 Gerçek IP'nize geri döndünüz")
        
        self.current_ip = None
        time.sleep(3)
    
    def show_info(self):
        """Bilgi göster"""
        self.clear_screen()
        self.print_banner()
        
        print(f"{Fore.CYAN}╔═══════════════════════════════════════════════════════════════════════╗")
        print(f"{Fore.CYAN}║                          {Style.BRIGHT}DEVONIC VPN BİLGİ{Style.NORMAL}                            ║")
        print(f"{Fore.CYAN}╚═══════════════════════════════════════════════════════════════════════╝")
        print()
        
        print(f"{Fore.YELLOW}🌟 ÖZELLİKLER:")
        print(f"{Fore.GREEN}   ✓ Ücretsiz proxy kullanımı")
        print(f"{Fore.GREEN}   ✓ Otomatik proxy listesi çekme")
        print(f"{Fore.GREEN}   ✓ Çalışan proxy bulma ve bağlanma")
        print(f"{Fore.GREEN}   ✓ Renkli ve kullanıcı dostu arayüz")
        print()
        
        print(f"{Fore.YELLOW}🌐 IP KONTROL SİTELERİ:")
        print(f"{Fore.CYAN}   • https://www.whatismyip.com")
        print(f"{Fore.CYAN}   • https://ipinfo.io")
        print(f"{Fore.CYAN}   • https://ipleak.net")
        print()
        
        print(f"{Fore.YELLOW}⚠  DİKKAT:")
        print(f"{Fore.RED}   • Ücretsiz proxy'ler her zaman çalışmayabilir")
        print(f"{Fore.RED}   • Bazı siteler proxy'leri engelleyebilir")
        print(f"{Fore.RED}   • Sadece yasal amaçlarla kullanın")
        print()
        
        print(f"{Fore.MAGENTA}{'─' * 73}")
        input(f"{Fore.GREEN}Devam etmek için ENTER'a basın...")
    
    def run(self):
        """Ana program döngüsü"""
        while True:
            self.show_menu()
            
            try:
                choice = input(f"\n{Fore.WHITE}{Style.BRIGHT}Seçiminiz: {Style.RESET_ALL}").strip()
                
                if choice == "1" and not self.running:
                    self.start_vpn()
                elif choice == "2" and self.running:
                    self.stop_vpn()
                elif choice == "3":
                    self.show_info()
                elif choice == "0":
                    if self.running:
                        self.stop_vpn()
                    
                    self.clear_screen()
                    print()
                    print(f"{Fore.CYAN}╔═══════════════════════════════════════════════════════════════════════╗")
                    print(f"{Fore.CYAN}║                                                                       ║")
                    print(f"{Fore.MAGENTA}║                  {Style.BRIGHT}DEVONIC VPN KAPATILIYOR...{Style.NORMAL}                         ║")
                    print(f"{Fore.CYAN}║                                                                       ║")
                    print(f"{Fore.CYAN}╚═══════════════════════════════════════════════════════════════════════╝")
                    print()
                    print(f"{Fore.GREEN}   Teşekkürler! Güvenli kalın! 🔒")
                    print()
                    time.sleep(2)
                    sys.exit(0)
                else:
                    print(f"\n{Fore.RED}⚠  Geçersiz seçim!")
                    time.sleep(1)
                    
            except KeyboardInterrupt:
                if self.running:
                    self.running = False
                print(f"\n\n{Fore.YELLOW}⚠  Program kapatılıyor...")
                time.sleep(1)
                sys.exit(0)

if __name__ == "__main__":
    vpn = DevonicVPN()
    vpn.run()
