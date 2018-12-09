# Гайд по запуску:

Запускаем elastic:
```
cd backend && docker-compose up --build
```
Книги могут подгружаться в двух режимах: локально и парсить сайт.
Все зависит от конфигурации `importer.py`. docker-compose настроен на локальный импорт книг из папки `./backend/data`. Книги должны храниться в файлах `[0-9]*.json` и содеражить численные индексы.
Индексатор при подключении к elastic'у проверяет наличие индекса книг, и в случае отсутствия начинает импорт.

Попытаться стянуть все книги в локальную папку:
```
python importer.py --local ./datafolder --export 32
```

Локально запулить книги в elastic:
```
python importer.py --offline --local ./data --host localhost 32
```

Обойти сайт и стянуть книги в elastic:
```
python importer.py --local ./data --host localhost 32
```

