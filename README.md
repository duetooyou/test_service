# test-service

Сервис на FastAPI с PostgreSQL и Redis, использующий [dishka](https://github.com/reagento/dishka) как IoC-контейнер.

## Почему dishka, а не FastAPI Depends

- Зависимости не привязаны к фреймворку — сервисный слой ничего не знает о FastAPI и легко переиспользуется в воркерах, CLI и тестах
- Scope (APP, REQUEST) декларируется явно рядом с провайдером, а не размазывается по lifespan и глобальным переменным
- Граф зависимостей валидируется при старте контейнера, а не в рантайме на первом запросе
- Для тестов достаточно передать другой провайдер в контейнер, без патчинга глобального app.dependency_overrides

## Пример использования

```python
@fastapi_app.get('/')
@inject
async def healthcheck(
        session: FromDishka[AsyncSession],
        redis_client: FromDishka[Redis]
) -> str:
    return 'hello'
```

`AsyncSession` и `Redis` приходят из dishka-контейнера автоматически — хендлер ничего не знает о том, как они создаются и закрываются.

## Что можно улучшить

- Вынести хендлеры из `main.py` в отдельный роутер и подключать их через `include_router`
- Добавить healthcheck-эндпоинт с реальной проверкой соединений к PostgreSQL и Redis
- Добавить миграции через Alembic и запускать их автоматически при старте контейнера
- Вынести uvicorn-конфиг (host, port, reload) из Dockerfile в отдельный `uvicorn.toml` или переменные окружения
- Добавить `depends_on` с `condition: service_healthy` в docker-compose, чтобы app не стартовал раньше чем поднимутся БД
- Покрыть провайдеры unit-тестами — подменить `ConfigProvider` тестовым и проверить что контейнер собирается без ошибок
- Использовать uv в качестве пакетного менеджера (скорость, безопасность, совместимость)
- Применить разделение слоев приложения и src layout для репозитория
## Запуск

### Без Docker

```bash
cp .env.example .env
poetry install
uvicorn app.main:fastapi_app --reload
```

### Docker

```bash
cp .env.example .env
docker compose --env-file .env up -d --build
```

## Остановка

```bash
docker compose down
```
