# README.md - Система управления складом товаров

## Описание проекта

Система управления складом товаров - это desktop-приложение с графическим интерфейсом для ведения учета товаров на складе. Приложение поддерживает авторизацию пользователей, разграничение прав доступа, добавление и удаление товаров, поиск по каталогу.

### Основные возможности

- **Авторизация и регистрация пользователей**
  - Вход по логину и паролю
  - Регистрация новых пользователей
  - Вход без регистрации (режим гостя)

- **Управление товарами (для администратора)**
  - Добавление новых товаров
  - Удаление существующих товаров
  - Просмотр всех товаров

- **Поиск и фильтрация**
  - Поиск товаров по названию
  - Поиск по артикулу

- **Ролевая модель**
  - Администратор - полный доступ
  - Менеджер - доступ только на просмотр
  - Гость - доступ только на просмотр

## Технологии

- Python 3.9+
- ttkbootstrap - стилизованные виджеты
- SQLite - база данных
- hashlib - хеширование паролей

## Структура проекта



Dem/
├── main.py # Главный файл приложения
├── config.py # Конфигурация (настройки БД, роли)
├── database.py # Работа с подключением к БД
├── models.py # Создание таблиц и моделей данных
├── auth.py # Авторизация и регистрация
├── products.py # CRUD операции с товарами
├── admin_panel.py # Форма добавления товара
├── database/ # Папка с файлом базы данных
│ └── app.db # SQLite база данных (создается автоматически)
└── requirements.txt # Зависимости проекта




## Установка и запуск на новом ПК

### 1. Установка Python

Скачайте и установите Python 3.9 или новее с [официального сайта](https://www.python.org/downloads/)

**При установке ОБЯЗАТЕЛЬНО отметьте галочку "Add Python to PATH"**

Проверьте установку:
```powershell
python --version
pip --version
```

# Перейдите в папку проекта
cd "C:\Users\%USERNAME%\Desktop\Dem GPT"

# Создание виртуального окружения
python -m venv venv

# Активация виртуального окружения (Windows)
venv\Scripts\activate

# Для macOS/Linux:
# source venv/bin/activate



# Убедитесь, что виртуальное окружение активно

# Установка из requirements.txt
pip install -r requirements.txt

# Или установка вручную
pip install ttkbootstrap



# Обычный запуск
python main.py

# Или с указанием кодировки
python -X utf8 main.py





Команды для сборки EXE (если нужно)
Установка PyInstaller


```pip install pyinstaller```



Сборка в один EXE файл


# Простая сборка
pyinstaller --onefile --windowed --name "WarehouseApp" main.py

еслм не работает то

py -m PyInstaller --onefile --windowed --name "WarehouseApp" main.py

# Расширенная сборка (с иконкой и без консоли)
pyinstaller --onefile --windowed --icon=app.ico --name "СкладТоваров" main.py

# Сборка с добавлением всех зависимостей
pyinstaller --onefile --windowed --add-data "database;database" --name "WarehouseApp" main.py



Очистка после сборки

# Удаление временных файлов сборки
rmdir /s /q build
rmdir /s /q __pycache__
del *.spec


Обновление зависимостей

pip install --upgrade ttkbootstrap


Запуск с отладкой
# Показывает полный стек ошибок
python -m pdb main.py


Очистка кэша
# Удаление всех __pycache__ папок
for /d /r . %d in (__pycache__) do @if exist "%d" rd /s /q "%d"



Настройка базы данных по умолчанию

При первом запуске автоматически создаются:

    Таблица users - пользователи системы

    Таблица roles - роли (Администратор, Менеджер)

    Таблица products - товары

    Таблица categories - категории (зарезервировано)

Учетная запись администратора по умолчанию:

    Логин: admin

    Пароль: admin

Скрипты для быстрого запуска
Создайте файл start.bat для Windows:


@echo off
cd /d "%~dp0"
if not exist "venv\Scripts\python.exe" (
    echo Creating virtual environment...
    python -m venv venv
    call venv\Scripts\activate
    pip install -r requirements.txt
) else (
    call venv\Scripts\activate
)
python main.py
pause


py -m PyInstaller --onefile --windowed --name "WarehouseApp" main.py


py -m pip install ttkbootstrap

py -m pip install pyinstaller

py -m pip install mysql-connector-python


