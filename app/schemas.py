# FastAPI'nin veri doğrulama kütüphanesi Pydantic'ten temel sınıfları alıyoruz
from pydantic import BaseModel, EmailStr
from datetime import datetime
# Kullanıcı oluşturma sırasında alınacak veriyi tanımlayan sınıf
class UserCreate(BaseModel):
    name: str                 # Kullanıcının adı
    email: EmailStr           # E-posta (otomatik olarak geçerli e-posta formatını kontrol eder)
    password: str             # Şifre (şimdilik hash'siz)
    role: str                 # Kullanıcı rolü: 'student', 'instructor', 'admin'

class UserOut(BaseModel):
    id: int
    name: str
    email: EmailStr
    role: str

    class Config:
        orm_mode = True  # SQLAlchemy objesini JSON'a çevirmeyi sağlar


# Kurs oluşturmak için kullanılacak giriş modeli
class CourseCreate(BaseModel):
    title: str
    description: str
    created_by: int  # User ID (eğitmen)

# Kurs görüntüleme için çıkış modeli
class CourseOut(BaseModel):
    id: int
    title: str
    description: str
    created_by: int

    class Config:
        orm_mode = True  # SQLAlchemy objesi JSON'a çevrilsin


class QuestionCreate(BaseModel):
    title: str
    content: str
    user_id: int
    course_id: int

class QuestionOut(BaseModel):
    id: int
    title: str
    content: str
    user_id: int
    course_id: int
    created_at: datetime

    class Config:
        orm_mode = True

from datetime import datetime

# Yanıt oluşturma (POST) için
class AnswerCreate(BaseModel):
    content: str
    question_id: int
    user_id: int

# Yanıtı dışa dönerken (GET) kullanılacak model
class AnswerOut(BaseModel):
    id: int
    content: str
    question_id: int
    user_id: int
    created_at: datetime

    class Config:
        from_attributes = True


