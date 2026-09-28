import os
import requests
from config import Config

class AIServiceError(Exception):
    """Yapay zekâ servisi hataları için özel hata sınıfı."""
    pass

class AIService:
    def __init__(self):
        self.api_key = Config.GROQ_API_KEY
        self.model = "llama-3.3-70b-versatile"
        self.endpoint = "https://api.groq.com/openai/v1/chat/completions"

    def _sistem_talimati_al(self):
        """İşletme kimlik metnini Config'den okur."""
        return Config.BUSINESS_CONTEXT

    def yanit_uret(self, mesaj, gecmis=None):
        """
        Kullanıcı mesajını ve geçmişi Groq'a gönderip yanıt alır.
        """
        # API anahtarı girilmemişse sistemin çökmesini engeller (Demo Modu)
        if not self.api_key:
            return "Demo Modu: Yapay zekâ servis anahtarı tanımlanmadığı için sistem deneme modundadır. Lütfen bizimle iletişime geçiniz."

        if gecmis is None:
            gecmis = []

        # Groq mesaj listesi sırası: 1. Sistem Kimliği, 2. Geçmiş Konuşma, 3. Yeni Mesaj
        messages = [
            {"role": "system", "content": self._sistem_talimati_al()}
        ]

        # Geçmiş mesajları ekle
        for item in gecmis:
            messages.append(item)

        # Yeni kullanıcı mesajını ekle
        messages.append({"role": "user", "content": mesaj})

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": 0.7
        }

        try:
            response = requests.post(self.endpoint, json=payload, headers=headers, timeout=20)
            
            if response.status_code != 200:
                raise AIServiceError(f"Groq API hatası (Kod {response.status_code}): {response.text}")
            
            data = response.json()
            return data["choices"][0]["message"]["content"]

        except requests.exceptions.RequestException as e:
            raise AIServiceError(f"Yapay zekâ servisine bağlanılamadı: {str(e)}")

# Proje boyunca tek bir servis nesnesi kullanılır (Singleton)
ai_service = AIService()