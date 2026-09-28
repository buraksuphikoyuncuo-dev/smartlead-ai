import os
from app import create_app

# Ortam değişkenine göre uygulamayı başlat
env_name = os.environ.get('FLASK_ENV', 'development')
app = create_app(env_name)

if __name__ == '__main__':
    # 5000 portunda uygulamayı çalıştır
    app.run(host='0.0.0.0', port=5000)