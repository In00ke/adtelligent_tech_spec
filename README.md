# FavQs API Tests

Автотесты для [FavQs API](https://favqs.com/api/).

## Структура проекта

```
├── api/
│   ├── client.py          # базовый HTTP клиент
│   ├── error_codes.py     # коды ошибок API
│   └── user_api.py        # методы User API
├── models/
│   ├── user.py            # модели данных
│   └── response.py        # модели ответов
├── tests/
│   ├── conftest.py        # фикстуры pytest
│   └── test_user.py       # тесты
├── utils/
│   ├── assertions.py      # хелперы для проверок
│   └── logger.py          # логирование
├── config.py              # конфигурация
├── pytest.ini             # настройки pytest
└── requirements.txt       # зависимости
```

## Конфигурация

Создать файл `.env` в корне проекта:

```env
FAVQS_API_KEY=your_api_key_here
FAVQS_BASE_URL=https://favqs.com/api
```

Или задать переменные окружения.

## Запуск тестов

```bash
# только smoke тесты
pytest -m smoke

# только regression тесты
pytest -m regression

# конкретный класс
pytest tests/test_user.py::TestUserCreation

# конкретный тест
pytest tests/test_user.py::TestUserCreation::test_create_and_verify
```

## Allure отчёты

```bash
# запуск с генерацией отчёта
pytest --alluredir=allure-results

# открыть отчёт
allure serve allure-results
```

## Тестовые сценарии

| Класс | Описание |
|-------|----------|
| `TestUserCreation` | Создание пользователя |
| `TestUserCreationNegative` | Негативные сценарии создания |
| `TestUserCreationBoundary` | Граничные значения |
| `TestUserUpdate` | Обновление профиля |
| `TestUserRetrieval` | Получение данных пользователя |
| `TestSession` | Авторизация (login/logout) |
