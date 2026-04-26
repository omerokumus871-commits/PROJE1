import customtkinter as ctk
import tkinter as tk
import time
import winsound
import random
import math
from threading import Thread

# Tasarım Ayarları
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class NAR_Master_System(ctk.CTk):
    def __init__(self):
        super().__init__()

        # --- PENCERE AYARLARI ---
        self.title("NAR-1 STRATEJİK HAREKAT MERKEZİ")
        self.geometry("1100x700")
        self.resizable(False, False)

        # 3 Sütunlu Grid Sistemi (Sol: Kontrol, Orta: Radar, Sağ: Loglar)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=2)
        self.grid_columnconfigure(2, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # ==================== 1. SOL PANEL (KONTROL VE VERİLER) ====================
        self.sol_panel = ctk.CTkFrame(self, fg_color="#1a1a1a", corner_radius=10)
        self.sol_panel.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        ctk.CTkLabel(self.sol_panel, text="NAR-1 KONTROL", font=("Orbitron", 24, "bold"), text_color="#ff4d4d").pack(pady=(20, 10))
        ctk.CTkLabel(self.sol_panel, text="Sistem Durumu: ÇEVRİMİÇİ", text_color="#00ff00", font=("Consolas", 12)).pack()

        # Ayrılma Mesafesi Girişi
        ayrilma_frame = ctk.CTkFrame(self.sol_panel, fg_color="transparent")
        ayrilma_frame.pack(pady=30, fill="x", padx=10)
        ctk.CTkLabel(ayrilma_frame, text="Kabuk Ayrılma Mesafesi (KM):", font=("Consolas", 13)).pack(anchor="w")
        
        self.ayrilma_input = ctk.CTkEntry(ayrilma_frame, font=("Consolas", 16), justify="center")
        self.ayrilma_input.insert(0, "65") # Varsayılan değer
        self.ayrilma_input.pack(fill="x", pady=5)
        ctk.CTkLabel(ayrilma_frame, text="*Demir Kubbe radarı 70. km'de algılar.", font=("Consolas", 10), text_color="gray").pack(anchor="w")

        # Fırlatma Butonu
        self.btn_firlat = ctk.CTkButton(self.sol_panel, text="SİSTEMİ FIRLAT (BAŞLAT)", font=("Consolas", 16, "bold"), 
                                        fg_color="#990000", hover_color="#ff0000", height=50, command=self.operasyonu_baslat)
        self.btn_firlat.pack(pady=20, padx=20, fill="x")

        # Telemetri Verileri (Canlı İstatistikler)
        self.stats = {}
        for item in ["DURUM", "HIZ", "MENZİL", "İRTİFA", "MÜHİMMAT"]:
            lbl = ctk.CTkLabel(self.sol_panel, text=f"{item}: ---", font=("Consolas", 14), text_color="#00ffff")
            lbl.pack(pady=5, padx=15, anchor="w")
            self.stats[item] = lbl

        # ==================== 2. ORTA PANEL (CANLI RADAR) ====================
        self.orta_panel = ctk.CTkFrame(self, fg_color="#000000", corner_radius=10, border_width=2, border_color="#333")
        self.orta_panel.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

        ctk.CTkLabel(self.orta_panel, text="TAKTİKSEL RADAR EKRANI", font=("Consolas", 18, "bold"), text_color="#4dff4d").pack(pady=10)
        
        self.canvas = tk.Canvas(self.orta_panel, width=500, height=600, bg="#051005", highlightthickness=0)
        self.canvas.pack(expand=True)
        self.radar_ciz()

        # ==================== 3. SAĞ PANEL (OPERASYON GÜNLÜĞÜ) ====================
        self.sag_panel = ctk.CTkFrame(self, fg_color="#0a0a0a", corner_radius=10)
        self.sag_panel.grid(row=0, column=2, sticky="nsew", padx=10, pady=10)

        ctk.CTkLabel(self.sag_panel, text="SİSTEM LOGLARI", font=("Consolas", 16, "bold"), text_color="#ffffff").pack(pady=(20, 10))
        
        self.log_box = ctk.CTkTextbox(self.sag_panel, fg_color="#000", text_color="#00ff00", font=("Consolas", 12))
        self.log_box.pack(padx=10, pady=10, fill="both", expand=True)
        self.log_ekle("SİSTEM HAZIR. Emir bekleniyor...")

    # --- YARDIMCI FONKSİYONLAR ---
    def radar_ciz(self):
        # Arka plan çizgileri ve daireleri
        for r in [50, 150, 250, 350, 450]:
            self.canvas.create_oval(250-r, 300-r, 250+r, 300+r, outline="#0f330f", width=1)
        self.canvas.create_line(250, 0, 250, 600, fill="#0f330f")
        self.canvas.create_line(0, 300, 500, 300, fill="#0f330f")
        
        # Hedef Bölgesi (En Üst)
        self.canvas.create_line(0, 50, 500, 50, fill="red", dash=(4, 4))
        self.canvas.create_text(250, 35, text="HEDEF BÖLGESİ", fill="red", font=("Consolas", 10))

    def ses_cal(self, frekans, sure):
        # Sesi arka planda çalar, programı dondurmaz
        Thread(target=lambda: winsound.Beep(frekans, sure), daemon=True).start()

    def log_ekle(self, mesaj):
        zaman = time.strftime("%H:%M:%S")
        self.log_box.insert("end", f"[{zaman}] {mesaj}\n")
        self.log_box.see("end") # Otomatik en alta kaydır

    # --- ANA OPERASYON MOTORU ---
    def operasyonu_baslat(self):
        # Kullanıcıdan girilen ayrılma değerini al (Hatalı girerse 65 kabul et)
        try:
            self.ayrilma_km = int(self.ayrilma_input.get())
        except:
            self.ayrilma_km = 65
            self.ayrilma_input.delete(0, "end")
            self.ayrilma_input.insert(0, "65")

        self.btn_firlat.configure(state="disabled", fg_color="#333", text="OPERASYONDA...")
        self.ayrilma_input.configure(state="disabled")
        
        self.log_ekle(">>> ATEŞLEME EMRİ ONAYLANDI!")
        self.log_ekle(f"Planlanan Ayrılma Mesafesi: {self.ayrilma_km} km")
        self.ses_cal(800, 1500) # Uzun fırlatma sesi
        
        # Simülasyonu yeni bir Thread (İş Parçacığı) içinde başlatıyoruz ki arayüz donmasın
        Thread(target=self.simulasyon_dongusu, daemon=True).start()

    def simulasyon_dongusu(self):
        dist = 1400.0 # Toplam Menzil
        ayrilma_gerceklesti = False
        radar_uyarisi = False
        
        # Çizim Objeleri
        self.ana_fuze = self.canvas.create_oval(240, 580, 260, 600, fill="#ff0000") # Kırmızı Ana Gövde
        self.alt_fuzeler = []

        self.stats["MÜHİMMAT"].configure(text="MÜHİMMAT: 1 (ANA GÖVDE)")
        
        # DÖNGÜ (Uçuş Süresi)
        while dist > 0:
            # Daha yavaş ve detaylı akması için 2 km - 2 km düşürüyoruz
            dist -= 2.0 
            if dist < 0: dist = 0

            # --- VERİ GÜNCELLEMELERİ ---
            # Hızı Mach 8 civarında titreşimli göster
            hiz_mach = round(8.0 + random.uniform(-0.1, 0.2), 2)
            self.stats["HIZ"].configure(text=f"HIZ: Mach {hiz_mach} (~9800 km/s)")
            self.stats["MENZİL"].configure(text=f"MENZİL: {int(dist)} KM")
            self.stats["DURUM"].configure(text="DURUM: SEYİR HALİNDE", text_color="#00ffff")
            
            # --- GÖRSEL (RADAR) GÜNCELLEMESİ ---
            # 1400 km'yi radar ekranındaki 600 piksele oranlıyoruz (Y ekseni)
            y_koordinati = 50 + (dist / 1400) * 550 
            
            if not ayrilma_gerceklesti:
                # Ana füzeyi yukarı taşı
                self.canvas.coords(self.ana_fuze, 245, y_koordinati-5, 255, y_koordinati+5)
            else:
                # Ayrılma olduysa alt füzeleri koni şeklinde dağıt
                # Mesafe azaldıkça (hedefe yaklaştıkça) X ekseninde daha çok açılırlar
                yayilma_miktari = (self.ayrilma_km - dist) * 1.5 
                
                # Sahte ana gövde soluk şekilde ortada devam etsin
                self.canvas.coords(self.ana_fuze, 248, y_koordinati-2, 252, y_koordinati+2)
                
                # 8 Alt füzeyi güncelle
                for i, alt_fuze in enumerate(self.alt_fuzeler):
                    # -4 ile +4 arasında açılarla dağıtıyoruz
                    aci_farki = (i - 3.5) * 15 # Genişlik açısı
                    x_sapma = math.sin(math.radians(aci_farki)) * yayilma_miktari
                    
                    self.canvas.coords(alt_fuze, 248 + x_sapma, y_koordinati-3, 252 + x_sapma, y_koordinati+3)

            # --- OLAYLAR ---
            # 1. RADAR TESPİTİ (70. KM)
            if dist <= 70 and not radar_uyarisi:
                radar_uyarisi = True
                self.stats["DURUM"].configure(text="DURUM: RADAR TESPİTİ!", text_color="#ffcc00")
                self.log_ekle("!!! DİKKAT: Düşman radarı (Demir Kubbe) tespiti.")
                self.ses_cal(1000, 300) # Uyarı sesi bip
                time.sleep(0.3)
                self.ses_cal(1000, 300)

            # 2. TAKTİKSEL KABUK AYRILMASI (Kullanıcının Girdiği KM)
            if dist <= self.ayrilma_km and not ayrilma_gerceklesti:
                ayrilma_gerceklesti = True
                self.stats["DURUM"].configure(text="DURUM: TAKTİKSEL AYRILMA", text_color="#ff4d4d")
                self.stats["MÜHİMMAT"].configure(text="MÜHİMMAT: 8 (NAR TANESİ)")
                self.log_ekle(f">>> {self.ayrilma_km}. KM: ANA GÖVDE PARÇALANDI!")
                self.log_ekle(">>> 8 Adet alt füze ölüm çemberi formasyonuna geçti.")
                
                # Ayrılma Sesi (Art arda hızlı bipler)
                for _ in range(4):
                    self.ses_cal(1500, 100)
                    time.sleep(0.1)
                
                # Sahte gövdenin rengini soluk gri yap
                self.canvas.itemconfig(self.ana_fuze, fill="#333333")
                
                # 8 Adet sarı alt füze objesi oluştur
                for _ in range(8):
                    tane = self.canvas.create_oval(248, y_koordinati, 252, y_koordinati, fill="#ffff00")
                    self.alt_fuzeler.append(tane)
                
                time.sleep(1) # O dramatik anı izlemek için 1 saniye donma

            # Simülasyonun akış hızı (Bunu artırırsan daha yavaş, azaltırsan daha hızlı uçar)
            time.sleep(0.04) 

        # --- DÖNGÜ BİTİŞİ (HEDEFE VARIŞ) ---
        self.stats["DURUM"].configure(text="DURUM: İMHA EDİLDİ", text_color="#00ff00")
        self.stats["MENZİL"].configure(text="MENZİL: 0 KM")
        self.log_ekle("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
        self.log_ekle("GÖREV BAŞARILI: HEDEF TAM İSABETLE VURULDU.")
        self.log_ekle("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
        
        # Patlama Sesi ve Efekti
        self.ses_cal(400, 2000)
        self.canvas.create_oval(150, 0, 350, 100, fill="#ff6600", outline="#ffff00", width=5)
        self.canvas.create_text(250, 50, text="BOOM!", font=("Impact", 30), fill="white")

# Sistemi Çalıştır
if __name__ == "__main__":
    app = NAR_Master_System()
    app.mainloop()