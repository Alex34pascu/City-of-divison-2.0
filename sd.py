import pickle as pi
import os

# Bu fonksiyonların dosya sisteminde nerede olduğunu bilmediğim için,
# os modülündeki temel fonksiyonları kullanacak şekilde basitleştirdim.
# Orijinal kodunuzda "file_directories" ve "Miscellaneous" vardı.
# Eğer bu modüller elinizde varsa ve özel bir işlevsellik sağlıyorsa,
# bu kısımları orijinaline göre düzenleyebilirsiniz.

def file_exists(filename):
    return os.path.exists(filename)

def file_get_contents(filename, mode="rb"):
    with open(filename, mode) as f:
        return f.read()

def file_put_contents(filename, data, mode="wb"):
    with open(filename, mode) as f:
        f.write(data)

class savedata(object):
    def __init__(self, filename):
        self.fn = filename
        self.dic = dict()

    def exists(self, what):
        return what in self.dic

    def add(self, item, value):
        self.dic[item] = value

    def read(self, item):
        if self.exists(item) == False:
            return None # Değeri bulamazsa None döndürsün
        else:
            return self.dic[item]

    def readn(self, item):
        if self.exists(item) == False:
            return None
        else:
            return int(self.dic[item])

    def readf(self, item):
        if self.exists(item) == False:
            return None
        else:
            return float(self.dic[item])

    def save(self):
        pd = pi.dumps(self.dic)
        file_put_contents(self.fn, pd, "wb")

    def load(self):
        if file_exists(self.fn) == False:
            return ""
        try:
            content = file_get_contents(self.fn, "rb")
            if content:
                self.dic = pi.loads(content)
        except (pi.UnpicklingError, EOFError):
            # Dosya boş veya bozuksa, sözlüğü boş olarak bırak
            self.dic = dict()
            return ""

# --- YENİ EKLENEN FONKSİYONLAR ---

def get(item, filename, default=None):
    """
    Belirtilen dosyadan bir öğeyi okur. Bulamazsa varsayılan değeri döndürür.
    Bu fonksiyon, diğer modüllerin sd.get() şeklinde çağırması için eklendi.
    """
    s = savedata(filename)
    s.load()
    value = s.read(item)
    if value is None:
        return default
    return value

def save(item, value, filename):
    """
    Belirtilen dosyaya bir öğeyi kaydeder.
    Bu fonksiyon, diğer modüllerin sd.save() şeklinde çağırması için eklendi.
    """
    s = savedata(filename)
    s.load() # Var olan verileri yükle ki üzerine yazılsın
    s.add(item, value)
    s.save()