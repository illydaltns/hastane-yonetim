from base_classes.Kullanici import Kullanicilar
import os

class Personeller(Kullanicilar):
    def __init__(self, ad, soyad, tc_no, sifre,gorev):
        super().__init__(ad, soyad, tc_no, sifre)
        self.__gorev = gorev

    def get_gorev(self):
        return self.__gorev

    def bilgileri_dosyaya_yaz(self):
        dosya_adi = "personeller.txt"
        with open(dosya_adi, "a", encoding="utf-8") as dosya:
            dosya.write(f"{self.get_ad()},{self.get_soyad()},{self.get_tc_no()},{self.get_sifre()},{self.get_telefon()},{self.get_email()},{self.get_gorev()},{self.get_departman()}\n")
        print("Personel bilgileri dosyaya başarıyla eklendi.")
        
    def hasta_bilgilerine_erişim(self, dosya_adi="hastalar.txt"):
        """Seçilen hastanın bilgilerine erişen kod."""
        ad = input("Hasta Adı: ").strip()
        soyad = input("Hasta Soyadı: ").strip()

        try:
            with open(dosya_adi, "r", encoding="utf-8") as dosya:
                bulundu = False
                for satir in dosya:
                    parcalar = satir.strip().split(",")
                    
                    # 4 parçadan fazla veri varsa, sadece ilk 4'ünü al
                    if len(parcalar) > 4:
                        parcalar = parcalar[:4]  # İlk 4 parçayı al
                    
                    if len(parcalar) < 4:  # Eksik bilgi varsa geç
                        continue
                    
                    satir_ad, satir_soyad, tc_no, sifre = parcalar
                    if satir_ad.lower().strip() == ad.lower() and satir_soyad.lower().strip() == soyad.lower():
                        print(f"\nAd: {satir_ad}, Soyad: {satir_soyad}")
                        print(f"TC No: {tc_no}, Şifre: {sifre}")
                        bulundu = True
                        break

                if not bulundu:
                    print("Aranan hasta bulunamadı.")
        except FileNotFoundError:
            print(f"{dosya_adi} dosyası bulunamadı.")
        except Exception as e:
            print(f"Bir hata oluştu: {e}")
        

    def randevu_guncelle(self, dosya_adi="randevular.txt"):
        """Seçilen randevuyu güncelleyip randevular dosyasına kaydeden kod."""
        if not os.path.exists(dosya_adi):
            print("Randevular dosyası bulunamadı!")
            return

        # Dosyadan randevuları oku
        with open(dosya_adi, "r", encoding="utf-8") as dosya:
            randevular = dosya.readlines()

        if not randevular:
            print("Randevu listesi boş!")
            return

        print("\n=== Mevcut Randevular ===")
        for randevu in randevular:
            print(randevu.strip())

        # Kullanıcıdan güncellemek istediği randevuyu sor
        tc_no = input("\nHastanın TC No'su: ").strip()
        tarih = input("Randevu tarihi (YYYY-MM-DD): ").strip()
        saat = input("Randevu saati (HH:MM): ").strip()

        eski_randevu_bulundu = False

        yeni_randevular = []

        for randevu in randevular:
            randevu_bilgileri = randevu.strip().split(", ")

            if len(randevu_bilgileri) == 9:  # Format uygun mu?
                mevcut_tc_no = randevu_bilgileri[0]
                mevcut_tarih = randevu_bilgileri[6]
                mevcut_saat = randevu_bilgileri[7]

                if mevcut_tc_no == tc_no and mevcut_tarih == tarih and mevcut_saat == saat:
                    eski_randevu_bulundu = True
                    print("\nRandevu bulundu!")

                    yeni_doktor = input("Yeni doktor adı ve soyadı: ").strip().title()
                    yeni_branş = input("Doktorun Branşı: ").strip().title()
                    yeni_tarih = input("Yeni randevu tarihi (YYYY-MM-DD): ").strip()
                    yeni_saat = input("Yeni randevu saati (HH:MM): ").strip()
                    yeni_tedavi = input("Yeni tedavi bilgisi: ").strip().title()

                    yeni_randevu = f"{mevcut_tc_no}, {randevu_bilgileri[1]}, {randevu_bilgileri[2]}, {randevu_bilgileri[3]}, {yeni_doktor}, {yeni_branş}, {yeni_tarih}, {yeni_saat}, {yeni_tedavi}\n"
                    yeni_randevular.append(yeni_randevu)
                    print("Randevu güncellendi!")
                else:
                    yeni_randevular.append(randevu)
            else:
                yeni_randevular.append(randevu)

        if not eski_randevu_bulundu:
            print("Belirtilen bilgilere sahip bir randevu bulunamadı!")
            return

        # Güncellenen listeyi dosyaya yaz
        try:
            with open(dosya_adi, "w", encoding="utf-8") as dosya:
                dosya.writelines(yeni_randevular)
            print("\nRandevu listesi güncellendi!")
        except Exception as e:
            print(f"Dosya yazılırken bir hata oluştu: {e}")
            
    
    def randevu_silme(self, dosya_adi="randevular.txt"):
        """Seçilen randevuyu silme işlemini yapan kod."""
        if not os.path.exists(dosya_adi):
            print("Randevular dosyası bulunamadı!")
            return

        # Dosyadan randevuları oku
        with open(dosya_adi, "r", encoding="utf-8") as dosya:
            randevular = dosya.readlines()

        if not randevular:
            print("Randevu listesi boş!")
            return

        print("\n=== Mevcut Randevular ===")
        for i, randevu in enumerate(randevular, start=1):
            print(f"{i}. {randevu.strip()}")

        try:
            # Kullanıcıdan silmek istediği randevunun numarasını al
            secim = int(input("\nSilmek istediğiniz randevunun numarasını girin: ").strip())
            if secim < 1 or secim > len(randevular):
                print("Geçersiz bir seçim yaptınız!")
                return

            # Seçilen randevuyu sil
            silinen_randevu = randevular.pop(secim - 1)
            print(f"\nSilinen Randevu: {silinen_randevu.strip()}")

            # Güncellenen listeyi dosyaya yaz
            with open(dosya_adi, "w", encoding="utf-8") as dosya:
                dosya.writelines(randevular)
            print("\nRandevu başarıyla silindi ve dosya güncellendi!")

        except ValueError:
            print("Lütfen geçerli bir numara girin!")
        except Exception as e:
            print(f"Bir hata oluştu: {e}")
            
    def doktor_bilgilerini_goruntule(self,dosya_adi="Doktorlar.txt"):
        """Seçilen doktorun bilgilerini görüntüleyen kod."""
        ad = input("Doktorun Adı: ").strip()
        soyad = input("Doktorun Soyadı: ").strip()

        if not os.path.exists(dosya_adi):
            print(f"{dosya_adi} dosyası bulunamadı.")
            return

        with open(dosya_adi, "r", encoding="utf-8") as dosya:
            doktorlar = dosya.readlines()

        for doktor in doktorlar:
            doktor_bilgileri = doktor.strip().split(",")
            if len(doktor_bilgileri) == 6:
                doktor_ad, doktor_soyad, tc_no, sifre, brans, calisma_saatleri = doktor_bilgileri
                if doktor_ad.lower() == ad.lower() and doktor_soyad.lower() == soyad.lower():
                    print(f"\nDoktor Bilgileri:")
                    print(f"Ad: {doktor_ad}")
                    print(f"Soyad: {doktor_soyad}")
                    print(f"TC No: {tc_no}")
                    print(f"Branş: {brans}")
                    print(f"Çalışma Saatleri: {calisma_saatleri}")
                    return

        print("\nGirilen ad ve soyada uygun doktor bulunamadı.")
      
    def bekleyen_randevulari_yonet(self, bekleyen_dosya="bekleyenRandevu.txt", aktif_dosya="randevular.txt"):
        """Bekleyen randevulardan randevuyu seçip onayla/iptal işlemini yapıp randevulara ekleyen kod."""
        try:
            # Bekleyen randevuları oku
            with open(bekleyen_dosya, "r", encoding="utf-8") as dosya:
                randevular = [satir.strip() for satir in dosya if satir.strip()]

            print(f"Bekleyen randevular listesi: {randevular}")

            if not randevular:
                print("Bekleyen randevu bulunamadı.")
                return

            # Tarihe göre sıralama
            # Randevu formatı: TC, Ad, Soyad, TC No, Ad Soyad, Görev, Tarih, Saat, Tanı
            # Tarih ve saat, son iki kısımdır (6. ve 7. eleman)
            randevular.sort(key=lambda x: x.split(",")[6].strip() + " " + x.split(",")[7].strip())

            print("\nBekleyen Randevular:")
            for i, randevu in enumerate(randevular, start=1):
                print(f"{i}. {randevu}")

            # Kullanıcıdan seçim al
            while True:
                secim = input("\nBir randevu seçin (Numara girin, iptal için '0'): ").strip()

                if secim.lower() == '0':
                    print("İşlem iptal edildi.")
                    return

                try:
                    secim = int(secim)
                    # Seçim geçerli bir numara mı? Liste boyutunu kontrol et
                    if secim < 1 or secim > len(randevular):
                        print(f"Geçersiz seçim! Lütfen 1 ile {len(randevular)} arasında bir numara girin.")
                    else:
                        break  # Geçerli bir seçim yapılırsa, döngüden çık
                except ValueError:
                    print("Geçersiz giriş. Lütfen geçerli bir sayı girin.")

            # Seçilen randevuyu al
            secilen_randevu = randevular[secim - 1]

            print(f"\nSeçilen Randevu: {secilen_randevu}")
            secim = input("1. Onayla\n2. İptal \nSeçiminizi yapın: ").strip()

            if secim == '1':
                # randevular.txt'ye ekle
                with open(aktif_dosya, "a", encoding="utf-8") as dosya:
                    dosya.write(secilen_randevu + "\n")
                print("Randevu onaylandı ve aktif randevulara eklendi.")
            elif secim == '2':
                print("Randevu iptal edildi ve silinecek.")
            else:
                print("Geçersiz seçim. İşlem iptal edildi.")
                return

            # Bekleyen randevulardan sil
            randevular.remove(secilen_randevu)
            with open(bekleyen_dosya, "w", encoding="utf-8") as dosya:
                for randevu in randevular:
                    dosya.write(randevu + "\n")
            print("Bekleyen randevular güncellendi.")

        except Exception as e:
            print(f"Beklenmedik bir hata oluştu: {e}")
            
    def doktor_takvimlerini_yonet(self,dosya_adi="doktorlar.txt"):
        """Doktor bilgilerini çekip çalışma saatlerini düzenleyen kod"""
        try:
            # Dosyadan doktor bilgilerini oku
            with open(dosya_adi, "r", encoding="utf-8") as dosya:
                doktorlar = [satir.strip() for satir in dosya if satir.strip()]

            if not doktorlar:
                print("Doktor listesi boş.")
                return

            # Doktorları alfabetik sıraya göre sırala
            doktorlar.sort(key=lambda x: x.split(",")[0])  # İsme göre sırala

            print("\nDoktor Listesi (Alfabetik Sıralama):")
            for i, doktor in enumerate(doktorlar, start=1):
                doktor_bilgileri = doktor.split(",")
                print(f"{i}. {doktor_bilgileri[0]} {doktor_bilgileri[1]} - {doktor_bilgileri[4]} ({doktor_bilgileri[5]})")

            # Kullanıcıdan doktor seçimi al
            secim = input("\nBir doktor seçin (Numara girin, iptal için '0'): ").strip()

            if secim == '0':
                print("İşlem iptal edildi.")
                return

            try:
                secim = int(secim)
                if secim < 1 or secim > len(doktorlar):
                    print("Geçersiz seçim.")
                    return
            except ValueError:
                print("Geçersiz giriş.")
                return

            # Seçilen doktor bilgilerini al
            secilen_doktor = doktorlar[secim - 1]
            doktor_bilgileri = secilen_doktor.split(",")

            print(f"\nSeçilen Doktor: {doktor_bilgileri[0]} {doktor_bilgileri[1]}")
            print(f"Mevcut Çalışma Saatleri: {doktor_bilgileri[5]}")

            yeni_saatler = input("Yeni çalışma saatlerini girin (örn: 08:00-16:00): ").strip()
            if not yeni_saatler or "-" not in yeni_saatler:
                print("Geçersiz çalışma saatleri formatı.")
                return

            # Çalışma saatlerini güncelle
            doktor_bilgileri[5] = yeni_saatler
            doktorlar[secim - 1] = ",".join(doktor_bilgileri)

            # Güncellenmiş listeyi dosyaya yaz
            with open(dosya_adi, "w", encoding="utf-8") as dosya:
                dosya.write("\n".join(doktorlar) + "\n")

            print(f"{doktor_bilgileri[0]} {doktor_bilgileri[1]} çalışma saatleri başarıyla güncellendi.")
        except FileNotFoundError:
            print(f"{dosya_adi} dosyası bulunamadı.")
        except Exception as e:
            print(f"Bir hata oluştu: {e}")
