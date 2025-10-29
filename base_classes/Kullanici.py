from abc import ABC, abstractmethod

class Kullanicilar(ABC):
    def __init__(self, ad, soyad, tc_no, sifre):
        self.__ad = ad
        self.__soyad = soyad
        self.__tc_no = tc_no
        self.__sifre = sifre

    @abstractmethod
    def bilgileri_goster(self):
        """Kullanıcı bilgilerini göstermek için soyut metot."""
        pass

    @abstractmethod
    def bilgileri_dosyaya_yaz(self):
        """Kullanıcı bilgilerini dosyaya yazmak için soyut metot."""
        pass

    def get_ad(self):
        return self.__ad
    
    def set_ad(self,yeni_ad):
        self.__ad=yeni_ad
    
    def get_soyad(self):
        return self.__soyad
    
    def set_soyad(self,yeni_soyad):
        self.__soyad=yeni_soyad

    def get_tc_no(self):
        return self.__tc_no
    
    def set_tc_no(self,yeni_tc_no):
        self.__tc_no=yeni_tc_no

    def get_sifre(self):
        return self.__sifre
    
    def set_sifre(self,yeni_sifre):
        self.__sifre=yeni_sifre

    
    def bilgileri_goster(self):
        print(f"Ad: {self.__ad}")
        print(f"Soyad: {self.__soyad}")
        print(f"TC No: {self.__tc_no}")

    def giris_yap(self, tc_no, sifre):
        if self.__tc_no == tc_no and self.__sifre == sifre:
            print("Giriş başarılı.")
            return True
        else:
            print("Giriş başarısız. TC No veya şifre yanlış.")
            return False
        

    