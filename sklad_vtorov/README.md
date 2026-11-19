# Складской учёт — проект Второва Алексея

## Запуск в Windows (VS Code / PowerShell)

```powershell
py -m venv .venv
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
python manage.py makemigrations accounts catalog journal
python manage.py migrate
python manage.py createsuperuser
python manage.py load_demo
python manage.py runserver
```

Откройте http://127.0.0.1:8000/ и http://127.0.0.1:8000/admin/.

Для CMD вместо активации PowerShell используйте:
`.venv\Scripts\activate.bat`

## Модули
- `accounts` — профиль пользователя.
- `catalog` — категории, поставщики и товары.
- `journal` — поступления, списания и перемещения запасов.
- `reports` — главная страница и сводные показатели.
- `config` — настройки и маршруты Django.
- `journal_config` — настройки журналирования.

## Проверка
```powershell
python manage.py check
python manage.py test
```
