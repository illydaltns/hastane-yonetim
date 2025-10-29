from base_classes.Kullanici import Kullanicilar
from datetime import datetime, timedelta
import os

class Doktorlar(Kullanicilar):
    def __init__(self, ad, soyad, tc_no, sifre, brans, calisma_saatleri):
        super().__init__(ad, soyad, tc_no, sifre)
        self.__brans = brans
        self.__calisma_saatleri = calisma_saatleri
        self.randevular = []  # Randevular listesi
        self.ozgecmis = []    # Özgeçmiş bilgileri
        self.yorumlar = []    # Yorumlar listesi

    # Getter ve Setter metodları
    def get_brans(self):
        return self.__brans
    
    def set_brans(self, yeni_brans):
        self.__brans = yeni_brans

    def get_calisma_saatleri(self):
        return self.__calisma_saatleri
    
    def set_calisma_saatleri(self, yeni_calisma_saatleri):
        self.__calisma_saatleri = yeni_calisma_saatleri


     # Abstract metodun uygulanması
    def bilgileri_dosyaya_yaz(self, dosya_adi="Doktorlar.txt"):
        # with open(dosya_adi, "a", encoding="utf-8") as dosya:
        #     dosya.write(f"{self.get_ad()},{self.get_soyad()},{self.get_tc_no()},{self.get_sifre()},{self.get_brans()},{self.get_calisma_saatleri()}\n")
        pass
    
    def takvim_goruntule(self, dosya_adi="randevular.txt"):
        """Doktorun takvimindeki randevuları dosyadan çekip görüntüler."""
        if not os.path.exists(dosya_adi):
            print(f"{dosya_adi} dosyası bulunamadı.")
            return

        with open(dosya_adi, "r", encoding="utf-8") as dosya:
            randevular = dosya.readlines()

        # Doktorun TC kimlik numarasına göre randevuları filtrele
        doktor_randevulari = [randevu.strip() for randevu in randevular if self.get_tc_no() in randevu]

        if not doktor_randevulari:
            print(f"{self.get_ad()} {self.get_soyad()} için takvimde randevu bulunmamaktadır.")
        else:
            print(f"\n{self.get_ad()} {self.get_soyad()} Takvimi:")
            for i, randevu in enumerate(doktor_randevulari, start=1):
                print(f"{i}. {randevu}")

    # Boş çalışma saatlerini görüntüleme
    def bos_saatleri_goruntule(self):
        """Doktorun boş saatlerini görüntüleyen kod."""
        print(f"\n{self.get_ad()} için boş saatler:")
        dolu_saatler = {randevu['saat'] for randevu in self.randevular}
        baslangic, bitis = map(lambda x: int(x.strip().split(":")[0]), self.__calisma_saatleri.split("-"))
        for saat in range(baslangic, bitis):
            saat_str = f"{saat:02}:00"
            if saat_str not in dolu_saatler:
                print(f"- {saat_str}")
                
    def en_yakin_randevuyu_bul(self, dosya_adi="randevular.txt", tedavi_turu="Poliklinik"):
        """Randevuyu bulup seçtikten sonra tedavi/ameliyat edip etmemesini sağlayan kod."""
        doktor_adi = f"{self.get_ad()} {self.get_soyad()}"
        if not os.path.exists(dosya_adi):
            print(f"{dosya_adi} dosyası bulunamadı.")
            return None

        try:
            with open(dosya_adi, "r", encoding="utf-8") as dosya:
                randevular = dosya.readlines()

            doktor_randevulari = []
            for randevu in randevular:
                randevu = randevu.strip()
                if not randevu:
                    continue  # Boş satırları atla

                # Randevuyu virgüle göre ayır
                randevu_bilgileri = randevu.split(", ")
                if len(randevu_bilgileri) != 9:
                    print(f"Hatalı format: {randevu}")
                    continue

                hasta_tc, hasta_ad, hasta_soyad, _, randevu_doktor, brans, tarih, saat, hastalik = randevu_bilgileri

                # Doktor adı eşleşmesi
                if randevu_doktor.lower() == doktor_adi.lower():
                    # Tedavi türüne göre filtreleme
                    if tedavi_turu == "Ameliyathane" and hastalik.lower() == "ameliyat":
                        doktor_randevulari.append((f"{tarih} {saat}", randevu, hasta_tc, f"{hasta_ad} {hasta_soyad}"))
                    elif tedavi_turu == "Poliklinik" and hastalik.lower() != "ameliyat":
                        doktor_randevulari.append((f"{tarih} {saat}", randevu, hasta_tc, f"{hasta_ad} {hasta_soyad}"))

            if doktor_randevulari:
                # En yakın randevuyu bulma
                doktor_randevulari.sort(key=lambda x: datetime.strptime(x[0], "%Y-%m-%d %H:%M"))
                en_yakin_randevu = doktor_randevulari[0]
                print(f"\nEn yakın {tedavi_turu} randevusu: {en_yakin_randevu[1]}")
                return en_yakin_randevu[1]  # Randevuyu geri döndür
            else:
                print(f"{doktor_adi} için herhangi bir randevu bulunamadı.")
                return None

        except Exception as e:
            print(f"Beklenmedik bir hata oluştu: {e}")
            return None
           
    def randevuyu_sil(self, dosya_adi, randevu):
        """Seçilen randevuyu silip geçmiş randevular dosyasına kaydeden kod."""
        try:
            with open(dosya_adi, "r", encoding="utf-8") as dosya:
                randevular = dosya.readlines()

            # Silinecek randevuyu bulup dosyadan çıkarma ve geçmiş randevulara ekleme
            with open(dosya_adi, "w", encoding="utf-8") as dosya, open("gecmisrandevular.txt", "a", encoding="utf-8") as gecmis_dosya:
                for r in randevular:
                    if r.strip() != randevu.strip():
                        dosya.write(r)
                    else:
                        gecmis_dosya.write(r)
                        print(f"Randevu silindi ve geçmişe kaydedildi: {randevu}")

        except Exception as e:
            print(f"Randevu silinirken hata oluştu: {e}")
            
    def doktor_tedavi_sayisi(doktor, gecmis_randevular_dosya="gecmisrandevular.txt"):
        """Seçilen doktorun tedavi ettiği kaç tane hasta varsa döndüren kod."""
        try:
            # Eğer doktor bir Doktorlar nesnesiyse TC'sini al
            if isinstance(doktor, Doktorlar):
                doktor_tc_no = doktor.get_tc_no()
            elif isinstance(doktor, str):
                doktor_tc_no = doktor  # Direkt string TC No gelirse
            else:
                print("Geçersiz doktor parametresi.")
                return 0

            if not os.path.exists(gecmis_randevular_dosya):
                print(f"{gecmis_randevular_dosya} dosyası bulunamadı.")
                return 0

            with open(gecmis_randevular_dosya, "r", encoding="utf-8") as dosya:
                randevular = [satir.strip() for satir in dosya if satir.strip()]

            # Doktorun TC'sine göre filtreleme
            doktor_randevulari = [randevu for randevu in randevular if doktor_tc_no in randevu]

            tedavi_sayisi = len(doktor_randevulari)
            print(f"Doktor TC No: {doktor_tc_no}, Tedavi Sayısı: {tedavi_sayisi}")
            return tedavi_sayisi

        except Exception as e:
            print(f"Bir hata oluştu: {e}")
            return 0
        
    def tarih_randevulari(self, dosya_adi="randevular.txt"):
        """doktorun girdiği tarihteki randevuları listeler."""
        doktor_adi = f"{self.get_ad()} {self.get_soyad()}"

        if not os.path.exists(dosya_adi):
            print(f"{dosya_adi} dosyası bulunamadı.")
            return

        # Tarihi kullanıcıdan al
        tarih = input("Tarih girin (YYYY-AA-GG formatında): ").strip()

        try:
            # Girilen tarihi kontrol et
            datetime.strptime(tarih, "%Y-%m-%d")
        except ValueError:
            print("Hatalı tarih formatı! Lütfen YYYY-AA-GG formatında bir tarih girin.")
            return

        with open(dosya_adi, "r", encoding="utf-8") as dosya:
            randevular = [satir.strip() for satir in dosya if tarih in satir and doktor_adi in satir]

        if randevular:
            print(f"\n{self.get_ad()} {self.get_soyad()} için {tarih} tarihindeki randevular:")
            for randevu in randevular:
                print(f"- {randevu}")
        else:
            print(f"{self.get_ad()} {self.get_soyad()} için {tarih} tarihli randevu bulunmamaktadır.")
