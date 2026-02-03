import os
import pickle

# --- AYARLAR ---
# Admin yapılacak oyuncunun adı buraya yazılı.
OYUNCU_ADI = "lolgamer"
# ---------------

# Betiğin çalıştığı klasördeki oyuncu dosyasının adını belirliyoruz.
oyuncu_dosyasi = OYUNCU_ADI + ".plr"

print(f"'{OYUNCU_ADI}' adlı oyuncu için admin yetkisi veriliyor...")
print(f"Hedef dosya: {oyuncu_dosyasi}")

# Dosyanın bu klasörde olup olmadığını kontrol edelim
if not os.path.exists(oyuncu_dosyasi):
    print(f"\nHATA: Bu klasörde '{oyuncu_dosyasi}' adında bir dosya bulunamadı!")
    print("Lütfen oyuna 'lolgamer' adıyla en az bir kere giriş yaptığınızdan emin olun.")
    input("\nKapatmak için Enter tuşuna basın...")
    exit()

try:
    # 1. Dosyayı okuma modunda aç ve tüm veriyi yükle
    with open(oyuncu_dosyasi, 'rb') as f:
        tum_veriler = pickle.load(f)

    # 2. Oyuncu verilerinin bulunduğu 'data' anahtarını al
    # Eğer 'data' anahtarı yoksa, boş bir sözlük oluştur
    oyuncu_verisi = tum_veriler.get('data', {})

    print("\n--- Önceki Yetkiler ---")
    print(f"Admin: {oyuncu_verisi.get('admin', 'Yok')}")
    print(f"Builder: {oyuncu_verisi.get('builder', 'Yok')}")
    print(f"Moderator: {oyuncu_verisi.get('moderator', 'Yok')}")
    
    # 3. Admin, builder ve moderator yetkilerini ekle veya güncelle
    # Sunucu kodu bu değerlerin 1 olmasını bekliyor
    oyuncu_verisi["admin"] = 1
    oyuncu_verisi["builder"] = 1
    oyuncu_verisi["moderator"] = 1

    # 4. Güncellenmiş oyuncu verisini ana yapıya geri koy
    tum_veriler['data'] = oyuncu_verisi

    # 5. Değiştirilmiş veriyi dosyaya geri yaz
    with open(oyuncu_dosyasi, 'wb') as f:
        pickle.dump(tum_veriler, f)

    print("\n--- Yeni Yetkiler ---")
    print(f"Admin: {oyuncu_verisi.get('admin', 'Hata!')}")
    print(f"Builder: {oyuncu_verisi.get('builder', 'Hata!')}")
    print(f"Moderator: {oyuncu_verisi.get('moderator', 'Hata!')}")
    
    print(f"\nBAŞARILI! '{OYUNCU_ADI}' adlı oyuncu artık tam yetkili bir admin.")

except Exception as e:
    print(f"\nBEKLENMEDİK BİR HATA OLUŞTU: {e}")
    print("Dosya bozuk olabilir veya okuma/yazma işlemi başarısız oldu.")
    print("Lütfen 'players' klasörünün yedeğini aldığınızdan emin olun.")

finally:
    # Kullanıcının mesajları okuyabilmesi için pencereyi açık tut
    input("\nİşlem tamamlandı. Kapatmak için Enter tuşuna basın...")