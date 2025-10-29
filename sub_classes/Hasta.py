from base_classes.Kullanici import Kullanicilar
from datetime import datetime
import os

class Hastalar(Kullanicilar):
    def __init__(self, ad, soyad, tc_no, sifre, tibbi_gecmis, dosya_adi="hastalar.txt"):
        super().__init__(ad, soyad, tc_no, sifre)
        self.__tibbi_gecmis = ""
        self.dosya_adi = dosya_adi
        self.tibbi_gecmis_dosya = f"randevular_{tc_no}.txt"


    # Getter ve Setter metodları
    def get_tibbi_gecmis(self):
        return self.__tibbi_gecmis

    def set_tibbi_gecmis(self, yeni_tibbi_gecmis):
        self.__tibbi_gecmis = yeni_tibbi_gecmis

    @classmethod
    def tum_hastalari_listele(cls, dosya_adi="hastalar.txt"):
        """Dosyadaki tüm hastaları listeler."""
        if not os.path.exists(dosya_adi):
            print(f"{dosya_adi} dosyası bulunamadı.")
            return

        print("\nKayıtlı Hastalar:")
        with open(dosya_adi, "r", encoding="utf-8") as dosya:
            hastalar = dosya.readlines()

        if not hastalar:
            print("Dosyada kayıtlı hasta bulunmamaktadır.")
            return

        for i, hasta in enumerate(hastalar, start=1):
            print(f"{i}. {hasta.strip()}")

    # Kullanıcıdan hasta bilgilerini alarak bir Hastalar nesnesi oluşturur
    @staticmethod
    def veri_olustur():
        ad = input("Hasta Adı: ")
        soyad = input("Hasta Soyadı: ")
        tc_no = input("Hasta TC No: ")
        sifre = input("Hasta Şifre: ")
        

        yeni_hasta = Hastalar(ad, soyad, tc_no, sifre, tibbi_gecmis="")
        yeni_hasta.bilgileri_dosyaya_yaz()
        return yeni_hasta

    def bilgileri_dosyaya_yaz(self, mod="a"):
        """
        Hasta bilgilerini dosyaya yazar.
        
        Parametreler:
        - mod="a": Dosyanın sonuna ekler (append modu).
        - mod="w": Dosyanın üzerine yazar (write modu).
        """
        with open(self.dosya_adi, mod, encoding="utf-8") as dosya:
            dosya.write(f"{self.get_ad()},{self.get_soyad()},{self.get_tc_no()},{self.get_sifre()},{self.get_tibbi_gecmis()}\n")
        
        if mod == "a":
            print("Hasta bilgileri dosyaya başarıyla eklendi.")
        elif mod == "w":
            print("Hasta bilgileri dosyaya başarıyla yazıldı.")


    # Bilgileri ekrana yazdırma
    def bilgileri_goster(self):
        """Soyut metodu uygulayan alt sınıf."""
        print("\nHasta Bilgileri:")
        print(f"Ad: {self.get_ad()}")
        print(f"Soyad: {self.get_soyad()}")
        print(f"TC No: {self.get_tc_no()}")
        print(f"Şifre: {self.get_sifre()}")


    # Hasta bilgilerini string formatında döner
    def bilgileri_string_yap(self):
        return f"{self.get_ad()}, {self.get_soyad()}, {self.get_tc_no()}, {self.get_sifre()}, {self.get_tibbi_gecmis()}"



    def randevu_olustur(self, doktorlar_dosya_adi="doktorlar.txt", randevular_dosya_adi="bekleyenRandevu.txt"):
            """Doktorlar listesinden seçim yaparak randevu oluşturur."""

            # Doktorlar listesini göster
            if not os.path.exists(doktorlar_dosya_adi):
                print(f"{doktorlar_dosya_adi} dosyası bulunamadı.")
                return

            with open(doktorlar_dosya_adi, "r", encoding="utf-8") as dosya:
                doktorlar = dosya.readlines()

            if not doktorlar:
                print("Doktor bilgisi bulunmamaktadır.")
                return

            print("\n--- Doktor Listesi ---")
            for i, doktor in enumerate(doktorlar, start=1):
                ad, soyad, tc_no, sifre, brans, calisma_saatleri = doktor.strip().split(",")
                print(f"{i}. Dr. {ad} {soyad} - Branş: {brans} - Çalışma Saatleri: {calisma_saatleri}")

            # Kullanıcıdan doktor seçmesini iste
            while True:
                secim = input("\nRandevu için bir doktor seçin (numara girin): ").strip()
                if secim.isdigit() and 1 <= int(secim) <= len(doktorlar):
                    secim_index = int(secim) - 1
                    secilen_doktor = doktorlar[secim_index].strip().split(",")
                    doktor_adi = f"{secilen_doktor[0]} {secilen_doktor[1]}"
                    doktor_tc = secilen_doktor[2]
                    brans = secilen_doktor[4]
                    calisma_saatleri = secilen_doktor[5]
                    break
                else:
                    print("Geçersiz seçim! Lütfen listedeki numaralardan birini girin.")

            # Çalışma saatlerini al
            baslangic_saati, bitis_saati = calisma_saatleri.split("-")
            baslangic_saati = datetime.strptime(baslangic_saati.strip(), "%H:%M")
            bitis_saati = datetime.strptime(bitis_saati.strip(), "%H:%M")

            # Kullanıcıdan randevu tarihi ve saati al
            tarih = input("Randevu Tarihi (YYYY-MM-DD): ").strip()

            while True:
                saat = input("Randevu Saati (HH:MM): ").strip()
                try:
                    randevu_saati = datetime.strptime(saat, "%H:%M")
                    if baslangic_saati <= randevu_saati <= bitis_saati:
                        break
                    else:
                        print(f"Geçersiz saat! Lütfen {calisma_saatleri} arasında bir saat girin.")
                except ValueError:
                    print("Geçersiz saat formatı! Lütfen HH:MM formatında bir saat girin.")

            hastalik_durumu = input("Hastalık Durumu: ").strip()

            # Randevu bilgisi oluştur
            randevu_bilgisi = f"{doktor_tc}, {doktor_adi}, {brans}, {tarih}, {saat}, {hastalik_durumu}"

            # Randevuyu dosyaya ekle
            with open(randevular_dosya_adi, "a", encoding="utf-8") as dosya:
                dosya.write(f"{self.get_tc_no()}, {self.get_ad()}, {self.get_soyad()}, {randevu_bilgisi}\n")

            # Tıbbi geçmişe hastalık durumunu ekle
            if self.__tibbi_gecmis:
                self.__tibbi_gecmis += f"; {hastalik_durumu}"
            else:
                self.__tibbi_gecmis = hastalik_durumu

            # Bilgi mesajı
            print(f"\nRandevu başarıyla oluşturuldu:\n{doktor_adi} - {tarih} {saat} - {hastalik_durumu}")

            
    # Kullanıcıya kendi randevularını listeler ve seçilen randevuyu iptal eder
    def randevu_iptal_et(self, dosya_adi="randevular.txt"):
        try:
            with open(dosya_adi, "r", encoding="utf-8") as dosya:
                randevular = dosya.readlines()

            # Kullanıcının randevularını filtrele
            kullanici_randevulari = [r for r in randevular if r.startswith(f"{self.get_tc_no()},")]

            if not kullanici_randevulari:
                print("Bu kullanıcıya ait randevu bulunmamaktadır.")
                return

            print("\nMevcut Randevularınız:")
            for i, randevu in enumerate(kullanici_randevulari, start=1):
                print(f"{i}. {randevu.strip()}")

            secim = input("\nİptal etmek istediğiniz randevunun numarasını girin: ").strip()

            if secim.isdigit():
                secim_index = int(secim) - 1

                if 0 <= secim_index < len(kullanici_randevulari):
                    iptal_edilen_randevu = kullanici_randevulari.pop(secim_index)

                    # Seçilen randevuyu tüm randevular listesinden kaldır
                    randevular.remove(iptal_edilen_randevu)

                    # Güncellenmiş randevu listesini dosyaya yeniden yaz
                    with open(dosya_adi, "w", encoding="utf-8") as dosya:
                        dosya.writelines(randevular)

                    print(f"\nRandevu başarıyla iptal edildi: {iptal_edilen_randevu.strip()}")
                else:
                    print("Geçersiz seçim. Lütfen listeden bir numara seçin.")
            else:
                print("Geçersiz giriş. Lütfen bir sayı girin.")

        except FileNotFoundError:
            print(f"{dosya_adi} dosyası bulunamadı.")
        except ValueError:
            print("Geçersiz giriş. Lütfen bir sayı girin.")


    def randevulari_goruntule(self):
        """Seçilen hastanın TC kimlik numarası ve şifresine göre randevularını dosyadan okur ve ekrana yazdırır."""
        dosya_adi = "randevular.txt"

        try:
            with open(dosya_adi, "r", encoding="utf-8") as dosya:
                randevular = dosya.readlines()

            # Hastanın TC kimlik numarasına ve şifresine göre filtrele
            kullanici_randevulari = [
                randevu for randevu in randevular
                if randevu.startswith(f"{self.get_tc_no()}, {self.get_ad()}, {self.get_soyad()}")
            ]

            if not kullanici_randevulari:
                print("Bu hastaya ait kayıtlı randevu bulunmamaktadır.")
                return

            print(f"\n{self.get_ad()} {self.get_soyad()} için Randevular:")
            for i, randevu in enumerate(kullanici_randevulari, start=1):
                print(f"{i}. {randevu.strip()}")

        except FileNotFoundError:
            print("Randevu dosyası bulunamadı. Henüz randevu oluşturulmamış.")

    def tibbi_gecmisi_goruntuleme(self, randevular_dosya_adi="gecmisrandevular.txt"):
        """Hastanın tıbbi geçmişini gecmisrandevular.txt dosyasından TC kimlik numarasına göre okuyarak detaylı şekilde görüntüler."""

        # Randevular dosyasının var olup olmadığını kontrol et
        if not os.path.exists(randevular_dosya_adi):
            print("\nRandevu dosyası bulunamadı. Henüz randevu oluşturulmamış.")
            return

        # Randevular dosyasını oku
        with open(randevular_dosya_adi, "r", encoding="utf-8") as dosya:
            randevular = dosya.readlines()

        # Hastanın TC kimlik numarasına göre filtrele
        hastaya_ait_randevular = [randevu for randevu in randevular if randevu.startswith(f"{self.get_tc_no()},")]

        # Tıbbi geçmişi ekrana yazdır
        if hastaya_ait_randevular:
            print(f"\n{self.get_ad()} {self.get_soyad()} için Tıbbi Geçmiş:")
            for i, randevu in enumerate(hastaya_ait_randevular, start=1):
                bilgiler = randevu.strip().split(", ")
                if len(bilgiler) >= 9:
                    doktor_ad = bilgiler[4]
                    doktor_bolum = bilgiler[5]
                    tarih = bilgiler[6]
                    saat = bilgiler[7]
                    hastalik_durumu = bilgiler[8]
                    print(f"{i}. Doktor: {doktor_ad}, Bölüm: {doktor_bolum}, Tarih: {tarih}, Saat: {saat}, Hastalık: {hastalik_durumu}")
                else:
                    print(f"{i}. Hatalı format: {randevu}")
        else:
            print(f"\n{self.get_ad()} {self.get_soyad()} için kayıtlı tıbbi geçmiş bulunmamaktadır.")

