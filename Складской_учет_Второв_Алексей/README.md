# Информационная система «Складской учёт»
**Выполнил: Второв Алексей**

Учебное Django-приложение для ведения номенклатуры, категорий, поставщиков, складских остатков и движений товаров. Включает Django Admin, REST API и сводный отчёт.

## Требования
- Python 3.10 или новее
- pip
- браузер

По умолчанию используется SQLite, поэтому для первого запуска PostgreSQL не требуется. Настройки можно расширить под PostgreSQL отдельно.

## Установка в Windows (PowerShell)
```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```
Откройте:
- Админ-панель: http://127.0.0.1:8000/admin/
- API: http://127.0.0.1:8000/api/
- Товары: http://127.0.0.1:8000/api/products/
- Категории: http://127.0.0.1:8000/api/categories/
- Поставщики: http://127.0.0.1:8000/api/suppliers/
- Движения: http://127.0.0.1:8000/api/movements/
- Сводка: http://127.0.0.1:8000/api/reports/summary/

## Запуск тестов
```powershell
python manage.py test
```
## Правила учёта
Движение `IN` увеличивает остаток, `OUT` уменьшает. Нельзя списать больше товара, чем есть на складе. Операция изменения остатка и запись движения выполняются атомарно.
