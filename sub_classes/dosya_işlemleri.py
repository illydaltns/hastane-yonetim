# Belirtilen veri türüne göre ilgili dosyaya veriyi ekler veya yeniden yazar.
    # Parametreler:
    # - veri_turu: Yazılacak verinin türü ('hasta', 'randevu', 'doktor', 'personel')
    # - veri: Yazılacak veri içeriği
    # - mode: Dosya modu ('a' -> ekleme, 'w' -> yeniden yazma)
    
def dosya_işlemleri(veri_turu, veri, mode='a'):
    
    dosya_yollari = {
        "hasta": "hastalar.txt",
        "randevu": "randevular.txt",
        "doktor": "doktorlar.txt",
        "personel": "personel.txt"
    }

    dosya_yolu = dosya_yollari.get(veri_turu)

    if not dosya_yolu:
        print("Geçersiz veri türü.")
        return

    try:
        with open(dosya_yolu, mode, encoding='utf-8') as dosya:
            if isinstance(veri, list):
                dosya.writelines([line + '\n' for line in veri])
            else:
                dosya.write(veri + '\n')
            print(f"{veri_turu.capitalize()} verisi başarıyla {dosya_yolu} dosyasına yazıldı ({'Ekleme' if mode == 'a' else 'Yeniden yazma'}).")
    except Exception as e:
        print(f"{dosya_yolu} dosyasına yazma hatası: {e}")

    