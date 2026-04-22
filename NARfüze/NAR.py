import time
import math

class NARSistemi:
    def __init__(self):
        # 1. TEMEL KİMLİK BİLGİLERİ
        self.ana_fuze_isim = "NAR"
        self.alt_fuze_isim = "NAR Taneleri"
        self.alt_fuze_sayisi = 8
        self.toplam_menzil = 1400.0  # km
        
        # 2. HIZ HESAPLAMALARI (Mach 8)
        self.hiz_mach = 8.0
        # 1 Mach ortalama 1234.8 km/saattir.
        self.hiz_kms = (self.hiz_mach * 1234.8) / 3600  # Saniyedeki hızı (yaklaşık 2.74 km/s)

        # 3. TAKTİKSEL GÖREV MESAFELERİ
        self.radar_siniri = 70.0
        self.ayrilma_mesafesi = self.radar_siniri - 5.0  # Radarın 5 km içinde (65. km)
        self.atesleme_mesafesi = self.ayrilma_mesafesi + 15.0 # Ayrılmadan 15 km önce (80. km)
        self.formasyon_yari_capi = 400 # metre
        
        # 4. SİSTEM DONANIM DURUMLARI (Bayraklar)
        self.alt_motorlar_hazir = False
        self.radar_tespiti = False
        self.ayrilma_gerceklesti = False
        self.ana_motor_durumu = "AKTİF VE YANIYOR"

    def sistem_raporu_ver(self):
        print("="*60)
        print(" UÇUŞ KONTROL BİLGİSAYARI BAŞLATILDI ".center(60, "*"))
        print(f"[*] Görev Tanımı    : {self.ana_fuze_isim} Hipersonik Saldırı Sistemi")
        print(f"[*] Uçuş Hızı       : Mach {self.hiz_mach} (Saniyede {self.hiz_kms:.2f} km)")
        print(f"[*] Toplam Menzil   : {self.toplam_menzil} km")
        print(f"[*] Yük Kapasitesi  : {self.alt_fuze_sayisi} Adet '{self.alt_fuze_isim}'")
        print("="*60)
        print("SİSTEM ONAYI: Fırlatma başarılı. Hedefe kilitlenildi.\n")
        time.sleep(2)

    def ucusu_baslat(self):
        kalan_mesafe = self.toplam_menzil

        while kalan_mesafe > 0:
            kalan_mesafe -= self.hiz_kms
            if kalan_mesafe < 0: kalan_mesafe = 0

            # Ekranda mesafenin düzgün görünmesi için yuvarlıyoruz
            gosterge_mesafesi = round(kalan_mesafe, 1)

            # --- AŞAMA 1: ALT MOTORLARIN ATEŞLENMESİ (80. km) ---
            if kalan_mesafe <= self.atesleme_mesafesi and not self.alt_motorlar_hazir:
                print("\n" + "[SİSTEM BİLDİRİMİ]".center(60, "-"))
                print(f"MESAFE: {gosterge_mesafesi} km")
                print(f">> Ayrılmaya 15 km kaldı!")
                print(f">> İÇ SİSTEM AKTİVASYONU: {self.alt_fuze_sayisi} adet '{self.alt_fuze_isim}' motoru ön ateşleme döngüsüne girdi.")
                print(f">> Ana gövde içinde itki birikimi sağlanıyor...")
                print("-" * 60 + "\n")
                self.alt_motorlar_hazir = True
                time.sleep(1.5)

            # --- AŞAMA 2: DÜŞMAN RADARINA GİRİŞ (70. km) ---
            if kalan_mesafe <= self.radar_siniri and not self.radar_tespiti:
                print("\n" + "!!! KIRMIZI ALARM !!!".center(60, " "))
                print(f"MESAFE: {gosterge_mesafesi} km")
                print(">> Düşman Hava Savunma (Demir Kubbe) radarına girildi.")
                print(">> Düşman radarı ana füzeye kilitlendi. Önleyici roket fırlatıldı!")
                print("!!!" * 20 + "\n")
                self.radar_tespiti = True
                time.sleep(1.5)

            # --- AŞAMA 3: TAKTİKSEL AYRILMA VE FORMASYON (65. km) ---
            if kalan_mesafe <= self.ayrilma_mesafesi and not self.ayrilma_gerceklesti:
                print("\n" + "+++ TAKTİKSEL MANEVRA: AYRILMA ONAYLANDI +++".center(60, " "))
                print(f"MESAFE: {gosterge_mesafesi} km")
                print(">> 1. Pnömatik itici motorlar (Ejection Motors) çalıştırıldı.")
                print(f">> 2. Dış kabuk parçalandı. {self.alt_fuze_sayisi} adet '{self.alt_fuze_isim}' şiddetle dışarı itildi.")
                print(f">> 3. UÇUŞ BİLGİSAYARI: {self.formasyon_yari_capi} metre aralıklı 'Ölüm Çemberi' (Circular) formasyonu sağlandı.")
                print(f">> 4. ELEKTRONİK HARP: '{self.ana_fuze_isim}' Ana motoru {self.ana_motor_durumu}. Sahte hedef olarak itkiye devam ediyor!")
                print(">> RADAR DURUMU: Düşman radarı şokta. Ekrandaki hedef sayısı aniden 9'a çıktı!")
                print("+" * 60 + "\n")
                self.ayrilma_gerceklesti = True
                time.sleep(2)

            # Standart seyir bildirimini terminali boğmamak için sadece belirli aralıklarla yazdır (her 100 km'de bir ve son 60 km'de sürekli)
            if gosterge_mesafesi % 100 == 0 or gosterge_mesafesi < 65:
                 print(f"Seyir halinde... Hedefe kalan mesafe: {gosterge_mesafesi:.1f} km")

            time.sleep(0.04) # Simülasyon hızı

            # --- HEDEFE VARIŞ ---
            if kalan_mesafe <= 0:
                print("\n" + " HEDEF İMHA EDİLDİ ".center(60, "X"))
                print(f">> Düşman hava savunması sahte ana gövde '{self.ana_fuze_isim}' peşine düştü.")
                print(f">> {self.alt_fuze_sayisi} adet '{self.alt_fuze_isim}' çember formasyonunda hedefi başarıyla vurdu.")
                print("X" * 60)
                break

# Sistemi Başlatma Kodları
if __name__ == "__main__":
    fuze = NARSistemi()
    fuze.sistem_raporu_ver()
    fuze.ucusu_baslat()