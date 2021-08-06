<p align="center">
  <img src="/assets/images/logo/Logo@0,3x.png?raw=true" alt="Repository logo"/>
</p>

<span align="center">
  
  # Информация вашего Mac в HomeKit

</span>

<img src="/other/turn_on.gif" align="right" alt="Turn on">

Вы можете интегрировать некоторые показатели Вашего Mac в [Apple HomeKit](https://www.apple.com/ios/home/) через мост [Homebridge](https://homebridge.io) в виде датчиков. Скрипт предоставляет доступ к информации Вашего Mac через Web API. Данный проект также можно использовать для других интеграций. 

## Установка и запуск
1. Установите последнюю версию [Python 3](https://www.python.org/downloads/). 
2. [Скачайте](https://github.com/AlexMishakov/info-mac/releases/) программу и запустите. 

Программа работает в фоновом режиме, поэтому проверить её работу можно в мониторинге системы. 

## Автозапуск
Откройте `Системные настройки` > `Пользователи и группы` > `Обьекты входа` и добавьте данное приложение через `+`. Программа будет автоматически запускаться после перезагрузки системы.  

## Как использовать
Вы можете открыть в браузере ссылку `http://<your_mac_ip>:7777` и посмотреть все возможные адреса. 

| Адрес                | Описание                                             |
| -------------------- | ---------------------------------------------------- |
| `/sleep_mode/status` | Отображает состояние монитора значениями `0` или `1` |
| `/sleep_mode/log`    | Показывает логи состояния монитора                   |
| `/battery/status`    | Отображает уровень заряда вашего Mac в процентах     |
| `/stop`              | Сервер останавливается                               |

Далее идет настройка Homebridge. Для каждого плагина показана своя настройка. Можно посмотреть пример конфигурации.

### Состояние монитора
**Плагин:** [homebridge-http-contact-sensor](https://github.com/cyakimov/homebridge-http-contact-sensor)
```
"accessories": [ {
    "accessory": "ContactSensor",
    "name": "MacBook Display",
    "pollInterval": 500,
    "statusUrl": "http://<your_mac_ip>:7777/sleep_mode/status"
} ]
```
`pollInterval` - периодичность проверки датчика в милисекундах
### Заряд батареи
**Плагин:** [homebridge-http-ambient-light-sensor](https://github.com/QuickSander/homebridge-http-ambient-light-sensor)
```
"accessories": [ {
    "accessory": "HttpAmbientLightSensor",
    "name": "MacBook battery",
    "getUrl": "http://<your_mac_ip>:7777/battery/status",
    "minValue": 0,
    "maxValue": 100
} ]
```

## TODO
- [x] Спящий режим
- [ ] Пробудить Mac
- [x] Информация о зарядке
- [ ] Информация о температуре
- [ ] Выбор порта
- [ ] Поддержка Windows