﻿# Тесты для чата и виджетов

Этот репозиторий содержит тесты для функциональности чат-бота и виджетов на сайте. Тесты написаны с использованием Python, Playwright и Allure, а также запускаются в контейнере Docker.

## Структура проекта

Проект включает два типа тестов:
1. **Backend тесты** — для API, который управляет чат-сообщениями.
2. **Frontend тесты** — для проверки чата-виджета  на главной странице сайта.

### Backend тесты
Тесты проверяют:
- Создание сообщений с неверными значениями в `session-id` и `payload`.
- Получение сообщений с случайным значением `session-id`.
- Создание и получение сообщений с ответами от бота.

### Frontend тесты
Тесты проверяют:
- Видимость и кликабельность кнопки чата на главной странице.
- Ввод текста в чат-виджет и получение ответов от бота, как с кнопками, так и без.
- Ввод данных в форму с именем и почтой.
- Адаптивность окна чата в зависимости от разрешения экрана.

## Требования

- **Python** 3.12
- **Playwright** 1.49.1
- **Docker** для контейнеризации
- **Allure** для генерации отчетов

## Установка

1. Клонировать репозиторий:

```
git clone https://github.com/defaultftxuser/AutoTests.git
cd <папка с репозиторием>
```
2. Поднять контейнер:
```
   docker compose up
```
1. Посмотреть отчет:
```
allure serve allure-results
```
