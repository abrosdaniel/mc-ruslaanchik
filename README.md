<h1 align="center">Приватный сервер Ruslaanchik</h1>
<p align="center">
  <img src="https://cdn.modrinth.com/data/DGnW8OhL/232d217065b0ff9353d18f0b6defb342d48bde35.png" alt="Ruslaanchik" width="100" height="100">
</p>
<div align="center">

[![Twitch](https://img.shields.io/badge/-Ruslaanchik-9146FF?logo=twitch&logoColor=white)](https://www.twitch.tv/ruslaanchik)
[![Telegram](https://img.shields.io/badge/-Ruslaanchik__gg-2CA5E0?logo=telegram&logoColor=white)](https://t.me/Ruslaanchik_gg)
[![DonationAlerts](https://img.shields.io/badge/-DonationAlerts-FF7900)](https://www.donationalerts.com/r/ruslaanchik)

</div>
<div align="center">
<table width="100%" cellspacing="0" cellpadding="0" border="0">
<tr>
<td width="50%" align="center" valign="top">

🚀 О сервере

**Minecraft:** 1.21.1  
**Модлоадер:** NeoForge 21.1.250  
**Сервер:** `mc-ruslaanchik.ebash.id`\
[📦 Скачать сборку](https://github.com/abrosdaniel/mc-ruslaanchik/releases/latest)

</td>
<td width="50%" align="center" valign="top">

🎟️ Проходка

Покупается за:

- Баллы канала на [Twitch](https://www.twitch.tv/ruslaanchik)
- Разовый донат на [DonationAlerts](https://www.donationalerts.com/r/ruslaanchik)

</td>
</tr>
</table>
</div>

<h4 align="center">Всё необходимое для игры на сервере Ruslaanchik:</h4>

<div align="center">
  
[🎮 Лаунчеры](#launchers) · [🧩 Моды](#mods) · [🛠️ Установка](#setup) · [🌐 Подключение](#connect) · [⚠️ Решение проблем](#troubleshooting)

</div>

---

<a name="launchers"></a>

## 🎮 Лаунчеры

- [Prism Launcher](https://prismlauncher.org)
- [Modrinth](https://modrinth.com/app)
- [CurseForge](https://www.curseforge.com/download/app)
- [GDLauncher](https://gdlauncher.com/)
- [MultiMC](https://multimc.org/#Download)
- [TLauncher](https://tlauncher.org/)

Выберите лаунчер с поддержкой **Minecraft 1.21.1 и NeoForge 21.1.250**.

<a name="mods"></a>

## 🧩 Моды

<div id="mod-list">

</div>

<a name="mod-list-end"></a>

> [!NOTE]
> В релиз включены обязательные и необязательные моды. Дополнительные клиентские моды разрешены, но их корректная работа не гарантируется.

<a name="setup"></a>

## 🛠️ Установка

| Вариант 1 — скачать сборку                                                                                                                                                                   | Вариант 2 — вручную по списку модов                                                                                                                                           |
| -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **1.** Откройте [последний релиз](https://github.com/abrosdaniel/mc-ruslaanchik/releases/latest) и скачайте подходящий файл сборки.                                                          | **1.** Создайте отдельную сборку **Minecraft 1.21.1 + NeoForge 21.1.250**.                                                                                                    |
| **2.** Импортируйте **Ruslaanchik-Prism.zip** в Prism / MultiMC или **Ruslaanchik.mrpack** (если есть в релизе) в лаунчер с поддержкой Modrinth.                                             | **2.** Скачайте все [обязательные моды](#mods) указанных версий для NeoForge и поместите их в папку `mods` вашей сборки или установите их через встроенный механизм лаунчера. |
| Если импорт недоступен: скачайте **Ruslaanchik-files.zip**, создайте сборку **Minecraft 1.21.1 + NeoForge 21.1.250** и скопируйте в её игровую папку содержимое папки `minecraft` из архива. | Необязательные моды из списка установите по желанию.                                                                                                                          |
| Необязательные моды из списка установите по желанию.                                                                                                                                         |                                                                                                                                                                               |

В готовую сборку включены **все моды из списка**, включая необязательные. В релизе скачивайте файлы **Ruslaanchik**, а не `Source code`.

> [!WARNING]
> **Не обновляйте Minecraft, NeoForge и моды самостоятельно** — дождитесь обновления списка администрацией.

<a name="connect"></a>

## 🌐 Подключение к серверу

1. Откройте `Сетевая игра → Добавить сервер`.
2. Если AuthLogic предложит настройку пароля, следуйте подсказкам и сохраните пароль.
3. Укажите название **Ruslaanchik** и адрес `mc-ruslaanchik.ebash.id`.
4. Нажмите **Готово** и подключитесь.
5. Для голосового чата разрешите доступ к микрофону и выберите его в меню **Plasmo Voice**. Клавишу открытия меню и передачи голоса можно посмотреть в настройках управления Minecraft.

> [!WARNING]
> После переустановки сборки пароль может понадобиться снова.
> Не используйте пароль от Microsoft и не передавайте другим свою папку `authlogic`.

<a name="troubleshooting"></a>

## ⚠️ Решение проблем

| Описание                                | Log                                                            | Решение                                                                                         |
| --------------------------------------- | -------------------------------------------------------------- | ----------------------------------------------------------------------------------------------- |
| Неверная версия игры или NeoForge       | `Incompatible client! Please use NeoForge 21.1.250`            | Проверьте версии Minecraft и NeoForge.                                                          |
| Отсутствие модов и зависимостей         | `Missing mods` / `Missing dependencies`                        | Сверьте список модов с нашим требуемым списком.                                                 |
| Нет доступа к серверу                   | `You are not whitelisted on this server`                       | Отправьте администрации свой игровой ник.                                                       |
| Ошибка входа AuthLogic или забыт пароль | -                                                              | Проверьте ник и пароль. Если забыли пароль - обратитесь к администрации.                        |
| Вылет при запуске                       | `Exit code 1`                                                  | Проверьте Java 21 и моды. Если не помогло - отправьте журнал ошибки администрации.              |
| Нехватка памяти                         | `OutOfMemoryError`                                             | Закройте лишние приложения и увеличьте лимит RAM, оставив память для системы.                   |
| Не удаётся подключиться                 | `Unknown host` / `Connection timed out` / `Connection refused` | Проверьте адрес сервера и интернет. Уточните, работает ли сервер.                               |
| Не работает голосовой чат               | -                                                              | Проверьте микрофон и разрешения ОС. Если Plasmo Voice не подключается - сообщите администрации. |

---

<h3 align="center">🎮 Ждём именно тебя на сервере стримера Ruslaanchik!</h3>
