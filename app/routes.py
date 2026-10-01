from flask import Blueprint, request, jsonify, render_template
from app.database import lead_ekle, tum_leadler
from app.services.ai_service import ai_service, AIServiceError

# İki ayrı Blueprint tanımlıyoruz: Biri sayfalar, diğeri API için
pages_bp = Blueprint('pages', __name__)
api_bp = Blueprint('api', __name__)

# --- SAYFA ROTALARI ---
@pages_bp.route('/')
def ana_sayfa():
    """Ziyaretçi karşılama sayfasını gösterir."""
    return render_template('index.html')

@pages_bp.route('/dashboard')
def dashboard():
    """Yönetici panelini gösterir."""
    return render_template('dashboard.html')

# --- API ROTALARI ---
@api_bp.route('/sohbet', methods=['POST', 'OPTIONS'])
def sohbet():
    """Kullanıcıdan gelen mesajı yapay zekâ servisine iletir."""
    if request.method == 'OPTIONS':
        return ('', 204)

    veri = request.get_json() or {}
    mesaj = veri.get('mesaj', '').strip()
    gecmis = veri.get('gecmis', [])

    if not mesaj:
        return jsonify({"basari": False, "hata": "Mesaj alanı boş bırakılamaz."}), 400

    try:
        cevap = ai_service.yanit_uret(mesaj=mesaj, gecmis=gecmis)
        return jsonify({"basari": True, "cevap": cevap}), 200
    except AIServiceError as e:
        return jsonify({"basari": False, "hata": str(e)}), 503

@api_bp.route('/leads', methods=['GET', 'POST', 'OPTIONS'])
def leads_yonetimi():
    """Müşteri adaylarını kaydeder veya listeler."""
    # CORS ön kontrol isteği (Browser Preflight)
    if request.method == 'OPTIONS':
        return ('', 204)

    # 1. YENİ KAYIT EKLEME (POST)
    if request.method == 'POST':
        veri = request.get_json() or {}
        isim = veri.get('isim', '').strip()
        telefon = veri.get('telefon', '').strip()
        eposta = veri.get('eposta', '').strip()
        feedback = veri.get('feedback', '').strip()
        mesaj = veri.get('mesaj', '').strip()

        # İsim ve telefon zorunludur
        if not isim or not telefon:
            return jsonify({"basari": False, "hata": "İsim ve telefon alanları zorunludur."}), 400

        try:
            # Not: Veritabanı fonksiyonunuz ek alanları alacak şekilde parametrelere aktarılır
            yeni_id = lead_ekle(isim=isim, telefon=telefon, eposta=eposta, feedback=feedback, mesaj=mesaj)
            return jsonify({
                "basari": True,
                "mesaj": "Kaydınız başarıyla alındı.",
                "lead_id": yeni_id
            }), 201
        except TypeError:
            # Eğer database.py henüz eposta/feedback parametresi almıyorsa geriye dönük uyumluluk:
            yeni_id = lead_ekle(isim=isim, telefon=telefon, mesaj=mesaj)
            return jsonify({
                "basari": True,
                "mesaj": "Kaydınız başarıyla alındı.",
                "lead_id": yeni_id
            }), 201
        except Exception as e:
            return jsonify({"basari": False, "hata": f"Veritabanı hatası: {str(e)}"}), 500

    # 2. KAYITLARI LİSTELEME (GET)
    try:
        kayitlar = tum_leadler()
        return jsonify({
            "basari": True,
            "leads": kayitlar,
            "data": kayitlar
        }), 200
    except Exception as e:
        return jsonify({"basari": False, "hata": f"Veritabanı hatası: {str(e)}"}), 500