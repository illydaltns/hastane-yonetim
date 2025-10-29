from base_classes.Kullanici import Kullanicilar
import os

class Yoneticiler(Kullanicilar):
    def _init_(self, ad, soyad, tc_no, sifre, dosya_adi="yoneticiler.txt"):
        super()._init_(ad, soyad, tc_no, sifre)
        self.dosya_adi = dosya_adi

    def bilgileri_dosyaya_yaz(self):
        try:
            with open(self.dosya_adi, "a", encoding="utf-8") as dosya:
                dosya.write(f"{self.get_ad()},{self.get_soyad()},{self.get_tc_no()},{self.get_sifre()}\n")
            print("Yönetici bilgileri başarıyla dosyaya yazıldı.")
        except Exception as e:
            print(f"Yönetici bilgileri yazılamadı: {str(e)}")

    def giris_yap(self):
        tc_no = input("Yönetici TC No: ").strip()
        sifre = input("Yönetici Şifresi: ").strip()

        if not os.path.exists(self.dosya_adi):
            print(f"{self.dosya_adi} dosyası bulunamadı.")
            return False

        try:
            with open(self.dosya_adi, "r", encoding="utf-8") as dosya:
                yoneticiler = dosya.readlines()

            for yonetici in yoneticiler:
                kayit_ad, kayit_soyad, kayit_tc, kayit_sifre = yonetici.strip().split(",")

                if kayit_tc == tc_no and kayit_sifre == sifre:
                    print(f"Hoş geldiniz, {kayit_ad} {kayit_soyad}")
                    return True

            print("Hatalı TC No veya şifre.")
            return False

        except Exception as e:
            print(f"Hata: Giriş yapılamadı. {str(e)}")
            return False

    def hastalari_goruntule(self):
        dosya_adi = "hastalar.txt"
        if not os.path.exists(dosya_adi):
            print(f"{dosya_adi} dosyası bulunamadı.")
            return

        try:
            with open(dosya_adi, "r", encoding="utf-8") as dosya:
                hastalar = dosya.readlines()
                if not hastalar:
                    print("Hiç hasta bulunmamaktadır.")
                    return
                for hasta in hastalar:
                    try:
                        ad, soyad, tc_no, sifre, tibbi_gecmis = hasta.strip().split(",")
                        print(f"Ad: {ad}, Soyad: {soyad}, TC No: {tc_no}, Tıbbi Geçmiş: {tibbi_gecmis}")
                    except ValueError:
                        print(f"Hatalı format: {hasta.strip()}")
        except Exception as e:
            print(f"Hata: Hastalar listelenemedi. {str(e)}")

    def hasta_ekle(self):
        print("Yeni bir hasta ekleniyor...")
        ad = input("Hasta Adı: ")
        soyad = input("Hasta Soyadı: ")
        tc_no = input("Hasta TC No: ")
        sifre = input("Hasta Şifresi: ")
        tibbi_gecmis = input("Tıbbi Geçmiş: ")

        try:
            with open("hastalar.txt", "a", encoding="utf-8") as dosya:
                dosya.write(f"{ad},{soyad},{tc_no},{sifre},{tibbi_gecmis}\n")
            print(f"{ad} {soyad} başarıyla eklendi!")
        except Exception as e:
            print(f"Hasta eklenirken hata oluştu: {e}")

    def hasta_sil(self, tc_no):
        self.dosya_sil("hastalar.txt", tc_no)

    def randevulari_goruntule(self):
        dosya_adi = "randevular.txt"
        if not os.path.exists(dosya_adi):
            print(f"{dosya_adi} dosyası bulunamadı.")
            return

        try:
            with open(dosya_adi, "r", encoding="utf-8") as dosya:
                randevular = dosya.readlines()
                if not randevular:
                    print("Hiç randevu bulunmamaktadır.")
                    return
                for randevu in randevular:
                    print(randevu.strip())
        except Exception as e:
            print(f"Hata: Randevular listelenemedi. {str(e)}")

    def randevu_ekle(self):
        tarih = input("Randevu tarihi (GG-AA-YYYY): ")
        saat = input("Randevu saati (HH:MM): ")
        tc_no = input("Hasta TC No: ")
        doktor = input("Doktor adı: ")

        randevu_bilgisi = f"Tarih: {tarih}, Saat: {saat}, Hasta TC: {tc_no}, Doktor: {doktor}\n"
        
        try:
            with open("randevular.txt", "a", encoding="utf-8") as dosya:
                dosya.write(randevu_bilgisi)
            print("Randevu başarıyla eklendi.")
        except Exception as e:
            print(f"Randevu eklenirken hata oluştu: {e}")

    def randevu_sil(self, tc_no):
        self.dosya_sil("randevular.txt", tc_no)

    def dosya_okuma(self, dosya_adi):
        if not os.path.exists(dosya_adi):
            print(f"{dosya_adi} dosyası bulunamadı.")
            return

        try:
            with open(dosya_adi, "r", encoding="utf-8") as dosya:
                veriler = dosya.readlines()
                if not veriler:
                    print(f"Hiç veri bulunmamaktadır: {dosya_adi}")
                    return
                for veri in veriler:
                    print(veri.strip())
        except Exception as e:
            print(f"{dosya_adi} dosyası okunamadı: {e}")

    def dosya_sil(self, dosya_adi, tc_no):
        if not os.path.exists(dosya_adi):
            print(f"{dosya_adi} dosyası bulunamadı.")
            return

        try:
            with open(dosya_adi, "r", encoding="utf-8") as dosya:
                veriler = dosya.readlines()

            yeni_veriler = [veri for veri in veriler if tc_no.strip() not in veri]

            if len(veriler) == len(yeni_veriler):
                print(f"TC numarası {tc_no} ile eşleşen bir veri bulunamadı.")
                return

            with open(dosya_adi, "w", encoding="utf-8") as dosya:
                dosya.writelines(yeni_veriler)

            print(f"TC numarası {tc_no} olan veri başarıyla silindi.")

        except Exception as e:
            print(f"Veri silinemedi: {e}")


    def doktorlari_goruntule(self):
        dosya_adi = "Doktorlar.txt"
        if not os.path.exists(dosya_adi):
            print(f"{dosya_adi} dosyası bulunamadı.")
            return

        try:
            with open(dosya_adi, "r", encoding="utf-8") as dosya:
                doktorlar = dosya.readlines()
                if not doktorlar:
                    print("Hiç doktor bulunmamaktadır.")
                    return
                print("\nDoktor Listesi:")
                for doktor in doktorlar:
                    ad, soyad, tc_no, sifre, brans, calisma_saatleri = doktor.strip().split(",")
                    print(f"Ad: {ad}, Soyad: {soyad}, TC No: {tc_no}, Branş: {brans}, Çalışma Saatleri: {calisma_saatleri}")
        except Exception as e:
            print(f"Hata: Doktorlar listelenemedi. {str(e)}")

    def doktor_ekle(self):
        print("Yeni bir doktor ekleniyor...")
        ad = input("Doktor Adı: ").strip()
        soyad = input("Doktor Soyadı: ").strip()
        tc_no = input("Doktor TC No: ").strip()
        sifre = input("Doktor Şifresi: ").strip()
        brans = input("Doktor Branşı: ").strip()
        calisma_saatleri = input("Çalışma Saatleri (Örn: 09:00-17:00): ").strip()

        dosya_adi = "doktorlar.txt"
        try:
            with open(dosya_adi, "a", encoding="utf-8") as dosya:
                dosya.write(f"{ad},{soyad},{tc_no},{sifre},{brans},{calisma_saatleri}\n")
            print(f"Dr. {ad} {soyad} başarıyla eklendi!")
        except Exception as e:
            print(f"Doktor eklenirken hata oluştu: {str(e)}")

    def doktor_sil(self, tc_no):
        dosya_adi = "doktorlar.txt"
        
        if not os.path.exists(dosya_adi):
            print(f"{dosya_adi} dosyası bulunamadı.")
            return

        try:
            with open(dosya_adi, "r", encoding="utf-8") as dosya:
                doktorlar = dosya.readlines()

            yeni_doktorlar = [doktor for doktor in doktorlar if not doktor.strip().split(",")[2] == tc_no.strip()]

            if len(doktorlar) == len(yeni_doktorlar):
                print(f"TC numarası {tc_no} ile eşleşen bir doktor bulunamadı.")
                return

            with open(dosya_adi, "w", encoding="utf-8") as dosya:
                dosya.writelines(yeni_doktorlar)

            print(f"TC numarası {tc_no} olan doktor başarıyla silindi.")

        except Exception as e:
            print(f"Doktor silinemedi: {e}")