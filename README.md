# Веб-приложение Encost Dash
Это веб-приложение, построенное с использованием Plotly Dash, предназначенное для визуализации данных из базы данных SQLite. Приложение включает в себя раздел общей информации, круговую диаграмму и диаграмму Ганта.

## Установка
Клонируйте репозиторий:

git clone https://github.com/ваше_имя_пользователя/encost-dash-app.git
## Установите необходимые зависимости:
```bach
pip install -r requirements.txt
```
### Запустите приложение:
```bash
python app.py
```
## Использование
Запустите приложение, выполнив app.py.
Откройте веб-браузер и перейдите по адресу http://127.0.0.1:8050/.
Исследуйте данные с использованием выпадающего фильтра для выбора конкретных состояний.
## Структура
app.py: Основной файл приложения, содержащий веб-приложение Dash.
testDB.db: Файл базы данных SQLite с образцовыми данными.
requirements.txt: Список зависимостей Python.
## Компоненты
Карточка общей информации
Отображает общую информацию о выбранных или стандартных данных.

## Круговая диаграмма
Круговая диаграмма, отображающая распределение состояний.

## Диаграмма Ганта
Диаграмма Ганта, отображающая временную шкалу продолжительности состояний.

## Требования
Python 3.x
Dash
Dash Mantine Components
Plotly Express
Dash Extensions
