# SQLAlchemy kütüphanelerini ve veritabanı işlemleri için gereken sınıfları import ediyoruz
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, Session

# Ortam değişkenlerini (örneğin .env dosyasından) okumak için
import os
from dotenv import load_dotenv

# .env dosyasını yükle
load_dotenv()

# .env dosyasındaki DATABASE_URL değişkenini alıyoruz
DATABASE_URL = os.getenv("DATABASE_URL")

# SQLAlchemy ile veritabanı motorunu oluşturuyoruz
engine = create_engine(DATABASE_URL)

# SessionLocal, her HTTP isteği için bağımsız bir veritabanı oturumu yaratmakta kullanılır
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

# Base sınıfı, tüm modellerin (tabloların) kalıtım alacağı temel sınıftır
Base = declarative_base()

# 🚀 Veritabanı bağlantısını sağlayacak dependency fonksiyonu
def get_db():
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()
