# Diploma Project


# Использовано:

* Python 3.11
* Django
* Django REST Framework
* PostgreSQL
* Redis
* Celery
* Docker
* Docker Compose

---

# Структура проекта

```
diploma
│
├ backend/                # основное приложение
├ config/                 # настройки 
├ backend/management/     
├ phones_shop.yaml        # файл с товарами для импорта
├ docker-compose.yml
├ Dockerfile
├ requirements.txt
└ manage.py
```



# Запуск проекта

## 1. Клонировать репозиторий

```
git clone https://github.com/NinaKoroleva/diploma_new.git
cd diploma
```

---

## 2. Запуск контейнеров

```
docker-compose up -d --build
```


---

## 3. Применить миграции

```
docker-compose exec web python manage.py migrate
```

---

## 4. Создать администратора

```
docker-compose exec web python manage.py createsuperuser
```

Ввод email и пароль администратора.

---

## 5. Загрузка товаров

В проекте есть файл `phones_shop.yaml` с примерами товаров.

Импорт выполняется командой:

```
docker-compose exec web python manage.py import_goods phones_shop.yaml
```

После этого товары появятся в базе данных.

---

# Доступ 

После запуска проект доступен по адресу:

```
http://localhost:8000
```

На сервере:

```
http://130.49.150.20:8000
```

---



# Админ панель

Админка доступна по адресу:

```
http://localhost:8000/admin
```

Через неё можно:

* управлять пользователями
* просматривать товары
* просматривать заказы
* управлять магазинами

---

# Пример запроса

Получить список товаров:

```
GET /products
```

Ответ:

```json
[
  {
    "id": 1,
    "name": "iPhone 15",
    "price": 1200
  }
]
```

---

