# Сервер Ruslaanchik

Адрес: `mc-ruslaanchik.ebash.id`. Minecraft 1.21.1, NeoForge 21.1.250, Java 21.

Клиентский список не является серверным пакетом: серверные моды и настройки устанавливаются отдельно администратором. Не копируйте все клиентские моды на сервер.

Серверная интеграция AntHub необязательна. При её использовании установите совместимый JAR и задайте в `config/anthub-server.toml`:

```toml
project = "https://github.com/abrosdaniel/mc-ruslaanchik"
serverId = "survival"
requiredPackVersion = "1.0.2"
# Замените значение на SHA-256 точных байтов опубликованного anthub.lock.json.
requiredLockSha256 = "REPLACE_WITH_PUBLISHED_LOCK_SHA256"
requireClient = false
handshakeTimeoutSeconds = 10
luckperms = false
```

После каждого развёртывания обновляйте version и hash согласно реально установленной серверной сборке. Публикация клиентского релиза не обновляет сервер. Включайте обязательный AntHub-клиент только после заполнения pin и проверки подключения.
