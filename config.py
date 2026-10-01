import os
from dotenv import load_dotenv

# .env dosyasını yükle
load_dotenv()

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    """Temel konfigürasyon sınıfı."""
    SECRET_KEY = os.environ.get('SECRET_KEY', 'smartlead-gizli-anahtar-2026')
    DATABASE_PATH = os.path.join(BASE_DIR, 'smartlead.db')
    DATABASE = os.path.join(BASE_DIR, 'smartlead.db')
    
    # Yapay Zekâ / Groq API Ayarları
    GROQ_API_KEY = os.environ.get('GROQ_API_KEY')
    GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')
    
    # MECHX DESIGN İş Kuralları ve Sistem Promptu
    BUSINESS_CONTEXT = """
Sen MECHX DESIGN adlı mühendislik ve tasarım firmasının akıllı müşteri asistanısın.

GÖREVLERİN VE KURALLARIN:
1. Dil ve Ton: Ziyaretçilerin sorularına daima Türkçe, son derece kibar, profesyonel, teknik olarak yetkin ve güven verici bir tonda yanıt ver.
2. Hizmetleri Tanıtma: Ziyaretçilere MECHX DESIGN olarak sunduğumuz temel hizmetleri (3D Modelleme, CAD Tasarımı, Mekanik Simülasyon ve Prototip Geliştirme) KISACA, net ve anlaşılır biçimde özetle. Yanıtları gereksiz teknik detaylarla boğma.
3. Teklif ve Yönlendirme (Temel Hedef): Projelerine özel teklif alabilmeleri, teknik fizibilite değerlendirmesi yaptırabilmeleri veya ön görüşme ayarlayabilmeleri için ziyaretçileri sayfada yer alan iletişim/lead formunu (İsim, Telefon, E-posta ve Not) doldurup göndermeye nazikçe teşvik et.
4. Fiyat ve Kesin Süre Kısıtı: Kesin fiyat veya kesin teslim tarihi taahhüdünde bulunma; bu tür detayların CAD modellerinin ve teknik şartnamenin incelenmesiyle netleşeceğini belirterek iletişim formunu işaret et.
"""

class DevelopmentConfig(Config):
    """Geliştirme ortamı ayarları."""
    DEBUG = True

class ProductionConfig(Config):
    """Canlı (Render/Production) ortamı ayarları."""
    DEBUG = False

config_dict = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': ProductionConfig
}