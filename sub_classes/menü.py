from sub_classes.Hasta import Hastalar
from sub_classes.Doktor import Doktorlar
from sub_classes.Yönetici import Yoneticiler
from sub_classes.Personel import Personeller
import os

class Menu:
    def ana_menu(self):
        while True:
            print("""
    +----------------------------------+
    |            ANA MENÜ              |
    +----------------------------------+
    |  1 - Hasta Girişi                |
    |  2 - Doktor Girişi               |
    |  3 - Yönetici Girişi             |
    |  4 - Personel Girişi             |
    |  0 - Çıkış                       |
    +----------------------------------+
    """)

            secim = input("Seçiminizi yapın (0-4): ").strip()

            if secim == "1":
                self.hasta_menu()
            elif secim == "2":
                self.doktor_menu()
            elif secim == "3":
                yonetici = self.giris_yap_yonetici()  # Yoneticiler nesnesini döndürüyor
                if yonetici:
                    self.yonetici_islem_menusu(yonetici)
            elif secim == "4":
                self.giris_yap_Personel()
            elif secim == "0":
                print("Çıkış yapılıyor...")
                break
            else:
                print("Geçersiz seçim! Lütfen 0 ile 3 arasında bir değer girin.")



    #Danışman Menüsü
    
    def giris_yap_Personel(self):
        tc_no = input("TC No: ").strip()
        sifre = input("Şifre: ").strip()
        dosya_adi = "personel.txt"

        if os.path.exists(dosya_adi):
            with open(dosya_adi, "r", encoding="utf-8") as dosya:
                for satir in dosya:
                    ad, soyad, kayitli_tc_no, kayitli_sifre, gorev = satir.strip().split(",")
                    if tc_no == kayitli_tc_no and sifre == kayitli_sifre:
                        print(f"\nHoş geldiniz, {ad} {soyad}!")
                        Personel = Personeller(ad, soyad, kayitli_tc_no, kayitli_sifre, gorev)
                        self.Personel_islem_menusu(Personel)
                        return
        print("TC No veya Şifre hatalı!")
        
    
    def Personel_islem_menusu(self,Personel):
        while True:
            print("""
╔══════════════════════════════════╗
║          PERSONEL MENÜSÜ         ║
╠══════════════════════════════════╣
║  1 - Randevuları Güncelle        ║
║  2 - Randevu Onay/İptal          ║
║  3 - Randevuları Sil             ║
║  4 - Doktor Bilgileri            ║
║  5 - Hasta Bilgilerine Erişim    ║
║  6 - Doktor Takvimini Yönet      ║
║  0 - Ana Menüye Dön              ║
╚══════════════════════════════════╝
""")
            secim = input("Seçiminizi yapın (0-4): ").strip()
            if secim == "1":
                Personel.randevu_guncelle()
            elif secim == "2":
                Personel.bekleyen_randevulari_yonet()
            elif secim == "3":
                Personel.randevu_silme()
            elif secim == "4":
                Personel.doktor_bilgilerini_goruntule()
            elif secim == "5":
                Personel.hasta_bilgilerine_erişim()
            elif secim == "6":
                Personel.doktor_takvimlerini_yonet()
            elif secim == "0":
                print("Ana menüye dünülüyor...")
                break
            else:
                print("Geçersiz seçim! Lütfen 0 ile 4 arasında bir değer girin.")
            
    # Hasta Menüsü
    def hasta_menu(self):
        while True:
            print("""
╔════════════════════════════════╗
║          HASTA MENÜSÜ          ║
╠════════════════════════════════╣
║  1 - Giriş Yap                 ║
║  2 - Kayıt Ol                  ║
║  0 - Ana Menüye Dön            ║
╚════════════════════════════════╝
""")

            secim = input("Seçiminizi yapın (0-2): ").strip()

            if secim == "1":
                self.giris_yap_hasta()
            elif secim == "2":
                self.kayit_ol_hasta()
            elif secim == "0":
                print("Ana menüye dönülüyor...")
                break
            else:
                print("Geçersiz seçim! Lütfen 0 ile 2 arasında bir değer girin.")

    # Hasta girişi yapma
    def giris_yap_hasta(self):
        tc_no = input("TC No: ").strip()
        sifre = input("Şifre: ").strip()
        dosya_adi = "hastalar.txt"

        if os.path.exists(dosya_adi):
            with open(dosya_adi, "r", encoding="utf-8") as dosya:
                for satir in dosya:
                    ad, soyad, kayitli_tc_no, kayitli_sifre, tibbi_gecmis = satir.strip().split(",")
                    if tc_no == kayitli_tc_no and sifre == kayitli_sifre:
                        print(f"\nHoş geldiniz, {ad} {soyad}!")
                        hasta = Hastalar(ad, soyad, kayitli_tc_no, kayitli_sifre, tibbi_gecmis)
                        self.hasta_islem_menusu(hasta)
                        return
        print("TC No veya Şifre hatalı!")

    # Hasta kayıt olma
    def kayit_ol_hasta(self):
        yeni_hasta = Hastalar.veri_olustur()
        print("Kayıt işlemi başarılı!")

    # Hasta işlem menüsü
    def hasta_islem_menusu(self, hasta):
        while True:
            print("""
╔══════════════════════════════════╗
║       HASTA İŞLEM MENÜSÜ         ║
╠══════════════════════════════════╣
║  1 - Bilgileri Göster            ║
║  2 - Randevu Oluştur             ║
║  3 - Randevuları Görüntüle       ║
║  4 - Randevu İptal Et            ║
║  5 - Tıbbi Geçmişi Görüntüle     ║
║  0 - Ana Menüye Dön              ║
╚══════════════════════════════════╝
""")
            secim = input("Seçiminizi yapın (0-5): ").strip()

            if secim == "1":
                hasta.bilgileri_goster()
            elif secim == "2":
                hasta.randevu_olustur()
            elif secim == "3":
                hasta.randevulari_goruntule()
            elif secim == "4":
                hasta.randevu_iptal_et()
            elif secim == "5":
                hasta.tibbi_gecmisi_goruntuleme()
            elif secim == "0":
                print("Ana menüye dönülüyor...")
                break
            else:
                print("Geçersiz seçim! Lütfen 0 ile 5 arasında bir değer girin.")

    # Doktor Menüsü
    def doktor_menu(self):
        tc_no = input("Doktor TC No: ").strip()
        sifre = input("Şifre: ").strip()
        dosya_adi = "doktorlar.txt"

        if os.path.exists(dosya_adi):
            with open(dosya_adi, "r", encoding="utf-8") as dosya:
                for satir in dosya:
                    ad, soyad, kayitli_tc_no, kayitli_sifre, brans, calisma_saatleri = satir.strip().split(",")
                    if tc_no == kayitli_tc_no and sifre == kayitli_sifre:
                        print(f"\nHoş geldiniz, Dr. {ad} {soyad}!")
                        doktor = Doktorlar(ad, soyad, kayitli_tc_no, kayitli_sifre, brans, calisma_saatleri)
                        self.doktor_islem_menusu(doktor)
                        return
        print("TC No veya Şifre hatalı!")

    # Doktor işlem menüsü
    def doktor_islem_menusu(self, doktor):
        while True:
            print("""
╔════════════════════════════════╗
║         DOKTOR MENÜSÜ          ║
╠════════════════════════════════╣
║  1 - Bilgileri Göster          ║
║  2 - Randevuları Görüntüle     ║
║  3 - Boş Çalışma Saatleri      ║
║  4 - Tedavi İşlemleri          ║
║  5 - Tedavi Edilen Hasta Sayısı║
║  6 - Tarihe Göre Randevu List  ║
║  0 - Ana Menüye Dön            ║
╚════════════════════════════════╝
""")

            secim = input("Seçiminizi yapın (0-4): ").strip()

            if secim == "1":
                doktor.bilgileri_goster()
            elif secim == "2":
                doktor.takvim_goruntule()
            elif secim == "3":
                doktor.bos_saatleri_goruntule()
            elif secim == "4":                           
                while True:                                 
                        print("1. AmeliyatHane")
                        print("2. Poliklinik")
                        print("0. Çıkış")
                        secim = input("Seçiminizi yapın: ").strip()    
                        if secim == "1":
                            en_yakin_randevu = doktor.en_yakin_randevuyu_bul(tedavi_turu="Ameliyathane")
                            if en_yakin_randevu:
                                print("1. Ameliyat Et")
                                print("2. Ameliyat Etme")
                                secim = input("Seçiminizi yapın: ").strip()
                                if secim == "1":
                                    doktor.randevuyu_sil(dosya_adi="randevular.txt", randevu=en_yakin_randevu) 
                                else:
                                    print("Ameliyat yapılmadı.")
                            else:
                                print("Ameliyat yapılacak hasta bulunamadı.")            
                        elif secim == "2":
                            en_yakin_randevu = doktor.en_yakin_randevuyu_bul(tedavi_turu="Poliklinik")
                            if en_yakin_randevu:
                                print("1. Tedavi Et")
                                print("2. Tedavi Etme")
                                secim = input("Seçiminizi yapın: ").strip()
                                if secim == "1":
                                    doktor.randevuyu_sil(dosya_adi="randevular.txt", randevu=en_yakin_randevu) 
                                else:
                                    print("Tedavi yapılmadı.")
                            else:
                                print("Tedavi edilecek hasta bulunamadı.")
                        elif secim == "0":
                            break
                        else:
                            print("Geçersiz seçim, tekrar deneyin.")
            elif secim == "5":
                doktor.doktor_tedavi_sayisi()
            elif secim == "6":
                doktor.tarih_randevulari()
            elif secim == "0":
                print("Ana menüye dönülüyor...")
                break
            else:
               print("Geçersiz seçim! Lütfen 0 ile 3 arasında bir değer girin.")
    



    def giris_yap_yonetici(self):
        """Yöneticinin giriş işlemi."""
        tc_no = input("Yönetici TC No: ").strip()
        sifre = input("Yönetici Şifresi: ").strip()
        dosya_adi = "yoneticiler.txt"

        if os.path.exists(dosya_adi):
            with open(dosya_adi, "r", encoding="utf-8") as dosya:
                for satir in dosya:
                    ad, soyad, kayitli_tc_no, kayitli_sifre = satir.strip().split(",")
                    if tc_no == kayitli_tc_no and sifre == kayitli_sifre:
                        print(f"\nHoş geldiniz, {ad} {soyad}!")
                        return Yoneticiler(ad, soyad, kayitli_tc_no, kayitli_sifre)  # Yoneticiler nesnesi döndürülüyor
        print("TC No veya Şifre hatalı!")
        return None  # Hatalı girişte None döndürülüyor




    def yonetici_islem_menusu(self,yonetici):
        while True:
                print("""
    +----------------------------------+
    |          YÖNETİCİ MENÜSÜ         |
    +----------------------------------+
    |  1 - Hasta Bilgilerini Görüntüle |
    |  2 - Yeni Hasta Ekle             |
    |  3 - Hasta Sil                   |
    |  4 - Tüm Randevuları Görüntüle   |
    |  5 - Yeni Randevu Ekle           |
    |  6 - Randevu Sil                 |
    |  7 - Doktor Bilgilerini Görüntüle|
    |  8 - Yeni Doktor Ekle            |
    |  9 - Doktor Sil                  |
    |  0 - Ana Menüye Dön              |
    +----------------------------------+
    """)
                secim = input("Seçiminizi yapın (0-9): ").strip()

                if secim == "1":
                    yonetici.hastalari_goruntule()
                elif secim == "2":
                    yonetici.hasta_ekle()
                elif secim == "3":
                    tc_no = input("Silinecek hastanın TC No: ").strip()
                    yonetici.hasta_sil(tc_no)
                elif secim == "4":
                    yonetici.randevulari_goruntule()
                elif secim == "5":
                    yonetici.randevu_ekle()
                elif secim == "6":
                    tc_no = input("Silinecek randevunun Hasta TC No: ").strip()
                    yonetici.randevu_sil(tc_no)
                elif secim == "7":
                    yonetici.doktorlari_goruntule()
                elif secim == "8":
                    yonetici.doktor_ekle()
                elif secim == "9":
                    tc_no = input("Silinecek doktorun TC No: ").strip()
                    yonetici.doktor_sil(tc_no)
                elif secim == "0":
                    print("Ana menüye dönülüyor...")
                    break
                else:
                    print("Geçersiz seçim! Lütfen 0 ile 9 arasında bir değer girin.")

        

    