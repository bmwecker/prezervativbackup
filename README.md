# 🛡️ VPN Knowledge Backup — VLESS Reality + Cloudflare + Yandex Relay

> **Цель этого репозитория**: Полный бэкап знаний по настройке многоуровневого VPN для обхода блокировок РФ/ТСПУ. Содержит все конфиги, скрипты и пошаговые инструкции, необходимые для воспроизведения конфигурации с нуля.

## 📋 Оглавление

1. [Архитектура](#архитектура)
2. [Инфраструктура](#инфраструктура)
3. [Слои защиты](#слои-защиты)
4. [Быстрый старт](#быстрый-старт)
5. [Файлы конфигурации](#файлы-конфигурации)
6. [Скрипты](#скрипты)
7. [Известные проблемы и решения](#известные-проблемы-и-решения)

---

## Архитектура

Система использует **4 уровня защиты** с автоматическим переключением:

```
Layer 0: Устройство ──VLESS+Reality──► VPS Швеция ──► Интернет
          (Прямое подключение, маскировка под HTTPS Microsoft)

Layer 1: Устройство ──VLESS+WS──► Cloudflare CDN ──► VPS Швеция ──► Интернет
          (Запасной: если заблокирован IP сервера)

Layer 2: Устройство ──VLESS──► Yandex Cloud Moscow ──iptables──► VPS Швеция ──► Интернет
          (Обход белых списков: трафик идет через RU-инфраструктуру)

Layer 3: WARP (Cloudflare WireGuard) для специфических сервисов
          (Google, Claude, OpenAI — выход через другой IP)
```

---

## Инфраструктура

| Компонент | Значение |
|-----------|---------|
| **VPS (основной)** | `45.148.118.5` — Швеция (JustHost) |
| **VPS (relay)** | `93.77.162.76` — Москва (Yandex Cloud, Прерываемая VM) |
| **Домен** | `vpn2.unitysolution.online` → проксируется через Cloudflare |
| **Панель управления** | 3X-UI `https://45.148.118.5:31208/V0dEU3CRUVn1z3MgHn` |
| **Панель логин** | `iYdrvxh6Mg` / `mjK6Afc7yi` |
| **SSH ключ Yandex** | `ssh-key-1776104268300` (файл на Рабочем столе) |
| **SSH команда Yandex** | `ssh -i <key_file> prezervativ@93.77.162.76` |

---

## Слои защиты

### Layer 0: VLESS + XTLS-Reality (Основной)

**Клиентские приложения**: Happ, v2raytun (Android), NekoBox, Xray-core напрямую (Windows)

**VLESS-ссылка шаблон:**
```
vless://<UUID>@45.148.118.5:443?type=tcp&security=reality&flow=xtls-rprx-vision&fp=firefox&sni=www.microsoft.com&pbk=<publicKey>&sid=<shortId>#Layer0_Primary
```

**Параметры Reality (из test-xray.json):**
- Server: `45.148.118.5:443`
- UUID: `462877e4-2d3e-47a2-ba1c-efd4cbce14fe`
- Flow: `xtls-rprx-vision`
- SNI (маскировка): `www.microsoft.com`
- Fingerprint: `firefox`
- Public Key: `WmoRX8YHYK0wzDMyaZQip2rwz3-1P2SIRzbgU--QiGg`
- Short ID: `4cc90bb2dd`

### Layer 1: Cloudflare CDN (WebSocket)

**Параметры Inbound в 3X-UI:**
- Protocol: VLESS
- Port: 443
- Transport: WebSocket (ws)
- Security: TLS (сертификат от панели — `Set Cert from Panel`)
- Домен: `vpn2.unitysolution.online` (A-запись → `45.148.118.5`, оранжевое облако Cloudflare)
- Cloudflare SSL Mode: **Full** (не Full Strict!)

**VLESS-ссылка шаблон:**
```
vless://<UUID>@vpn2.unitysolution.online:443?type=ws&security=tls&path=%2F#Layer1_CDN
```

### Layer 2: Yandex Cloud Relay (Обход белых списков)

**Команды для настройки Yandex VM (выполнить после SSH):**
```bash
# Включить IP forwarding
sudo sysctl -w net.ipv4.ip_forward=1

# Переброс трафика с Yandex на Swedish VPS
sudo iptables -t nat -A PREROUTING -p tcp --dport 443 -j DNAT --to-destination 45.148.118.5:443
sudo iptables -t nat -A POSTROUTING -j MASQUERADE

# Сохранить правило навсегда (auto-start через 10 сек)
(sleep 10 && sudo iptables-save > /etc/iptables/rules.v4) &
```

**Подключение к Yandex VM:**
```bash
ssh -i C:\Users\PC\Desktop\ssh-key-1776104268300\ssh-key-1776104268300 prezervativ@93.77.162.76
```

**VLESS-ссылка (аналог Layer0, но IP = Yandex):**
```
vless://<UUID>@93.77.162.76:443?type=tcp&security=reality&flow=xtls-rprx-vision&fp=firefox&sni=www.microsoft.com&pbk=<publicKey>&sid=<shortId>#Layer2_YandexRelay
```

### Layer 3: WARP (Cloudflare WireGuard)

Встроен в Xray-core как отдельный `outbound`. Трафик к Google, Claude.ai, OpenAI, Netflix автоматически выходит через Cloudflare WARP (другой IP).

**Конфиги:** `new_xray_config.json`, `multi_warp_config.json`

---

## Быстрый старт (Windows)

### Вариант A: Запуск через BAT-файл (Xray-core напрямую)

1. Убедитесь, что `xray2\xray.exe` существует по пути:  
   `C:\Users\PC\.gemini\antigravity\playground\metallic-chromosphere\xray2\xray.exe`
2. Запустите `Start-VPN.bat` с Рабочего стола
3. Браузер должен автоматически получить системный прокси `127.0.0.1:2082`
4. Для Telegram Desktop: перейдите в Настройки → Расширенные → Тип подключения → SOCKS5 Proxy → `127.0.0.1:2081`

### Вариант B: Мобильный (Android)

Импортируйте VLESS-ссылку Layer0 в одно из приложений:
- **Happ** (рекомендуется)
- **v2raytun**
- **Hiddify** (если не работает — отключить MUX в настройках)

---

## Файлы конфигурации

| Файл | Описание |
|------|----------|
| `configs/test-xray.json` | Клиентский конфиг Xray для Windows (SOCKS5:2081 + HTTP:2082) |
| `configs/new_xray_config.json` | Серверный конфиг 3X-UI с WARP-маршрутизацией |
| `configs/multi_warp_config.json` | Конфиг для мульти-WARP (несколько пользователей → разные IP) |

---

## Скрипты

| Файл | Описание |
|------|----------|
| `scripts/Start-VPN.bat` | Запуск Xray + включение системного прокси Windows |
| `scripts/Stop-VPN.bat` | Остановка Xray + отключение прокси |
| `scripts/enable_sniffing.py` | Включение sniffing во всех Inbound через 3X-UI API |
| `scripts/update_3xui.py` | Добавление WARP в конфиг 3X-UI через API |
| `scripts/warp_gen.py` | Генерация новых WARP WireGuard ключей через Cloudflare API |
| `scripts/duck.sh` | Обновление DuckDNS (домен `prezervativ.duckdns.org`) |

---

## Известные проблемы и решения

### ❌ Hiddify зависает в цикле подключения
- **Причина**: Несовместимость MUX с VLESS-Reality
- **Решение**: Settings → Advanced → Multiplexing → OFF

### ❌ NekoBox зависает, интернет не работает
- **Причина**: Завис TUN-адаптер
- **Решение**: Task Manager → завершить NekoBox → `netsh winsock reset` → перезагрузка

### ❌ Telegram/WhatsApp не работает при включённом прокси
- **Причина**: Эти приложения игнорируют системный прокси Windows
- **Решение**: Hiddify в режиме TUN (запуск от Администратора) или вручную задать прокси в настройках приложения

### ❌ Layer2 Yandex перестал работать
- **Причина**: Прерываемая VM была остановлена Яндексом
- **Решение**: Зайти в консоль Yandex Cloud → запустить VM → снова выполнить iptables-команды

### ❌ NekoBox ошибка `geosite:ru in IP field`
- **Причина**: geosite-правила нельзя вставлять в поле IP
- **Решение**: Domain поле → `geosite:ru`, IP поле → `geoip:ru`

---

## 3X-UI API (для скриптов)

**Base URL**: `https://45.148.118.5:31208/V0dEU3CRUVn1z3MgHn`

```python
import requests, urllib3
urllib3.disable_warnings()
session = requests.Session()
login = session.post(f"{URL}/login", data={"username": "iYdrvxh6Mg", "password": "mjK6Afc7yi"}, verify=False)
# Затем используйте session для всех запросов
```

**Полезные эндпоинты:**
- `POST /login` — авторизация
- `POST /panel/inbound/list` — список inbound
- `POST /panel/inbound/update/{id}` — обновить inbound
- `GET /panel/setting/all` — получить все настройки (включая xrayTemplateConfig)
- `POST /panel/setting/update` — сохранить настройки
- `POST /panel/setting/restart` — перезапустить Xray

---

## Полезные ссылки

- [3X-UI GitHub](https://github.com/MHSanaei/3x-ui)
- [Xray-core Releases](https://github.com/XTLS/Xray-core/releases)
- [XTLS Reality Docs](https://github.com/XTLS/REALITY)
- [Cloudflare WARP Keys via API](https://developers.cloudflare.com/warp-client/)
