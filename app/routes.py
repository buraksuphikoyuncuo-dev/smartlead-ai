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
@api_bp.route('/sohbet', methods=['POST'])
def sohbet():
    """Kullanıcıdan gelen mesajı yapay zekâ servisine iletir."""
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

@api_bp.route('/leads', methods=['POST'])
def yeni_lead():
    """Yeni bir müşteri adayı kaydeder."""
    veri = request.get_json() or {}
    isim = veri.get('isim', '').strip()
    telefon = veri.get('telefon', '').strip()
    mesaj = veri.get('mesaj', '').strip()

    # İsim ve telefon zorunludur
    if not isim or not telefon:
        return jsonify({"basari": False, "hata": "İsim ve telefon alanları zorunludur."}), 400

    try:
        yeni_id = lead_ekle(isim=isim, telefon=telefon, mesaj=mesaj)
        return jsonify({
            "basari": True,
            "mesaj": "Kaydınız başarıyla alındı.",
            "lead_id": yeni_id
        }), 201
    except Exception as e:
        return jsonify({"basari": False, "hata": f"Veritabanı hatası: {str(e)}"}), 500

@api_bp.route('/leads', methods=['GET'])
def lead_listesi():
    """Tüm müşteri adaylarını döndürür."""
    try:
        kayitlar = tum_leadler()
        return jsonify({"basari": True, "data": kayitlar}), 200
    except Exception as e:
        return jsonify({"basari": False, "hata": f"Veritabanı hatası: {str(e)}"}), 500