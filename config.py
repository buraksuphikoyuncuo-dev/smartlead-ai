import os
from dotenv import load_dotenv

# .env dosyasındaki değişkenleri sisteme yükler
load_dotenv()

class Config:
    """Temel ayar sınıfı - Tüm modüller ayarları buradan okur."""
    SECRET_KEY = os.environ.get('SECRET_KEY', 'varsayilan-anahtar')
    DATABASE_URL = os.environ.get('DATABASE_URL', 'smartlead.db')
    GROQ_API_KEY = os.environ.get('GROQ_API_KEY', '')
    AI_PROVIDER = os.environ.get('AI_PROVIDER', 'groq')
    CORS_ORIGINS = os.environ.get('CORS_ORIGINS', '*')

    # Yapay zekânın kimliği ve işletme kuralları
    BUSINESS_CONTEXT = os.environ.get(
        'BUSINESS_CONTEXT',
        """Sen MECHX Design mühendislik ve mekanik tasarım ofisinin akıllı müşteri asistanısın.
Görevlerin:
1. Ziyaretçilere 3D modelleme, CAD tasarımı, mekanik simülasyon ve prototip geliştirme hizmetlerimizi tanıtmak.
2. Ziyaretçilerin sorularına daima Türkçe, kibar, profesyonel ve güven verici bir tonda yanıt vermek.
3. Projelerine teklif alabilmeleri veya ön görüşme ayarlayabilmeleri için onları ad, telefon ve proje detayı bırakmaya nazikçe yönlendirmek.
Fiyat tekliflerini doğrudan verme; iletişim bilgilerini aldığında uzman ekibimizin 24 saat içinde dönüş yapacağını belirt."""
    )

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False

# Uygulama fabrikasının ortam seçebilmesi için sözlük yapısı
config_dict = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}