Внутри каждого плагина содержится блок кода для настройки параметров отображения.
Незабудьте добавитьих в config.toml, это позволяет указать позиции элементов времени и даты и т.д...

# Описание плагинов
1. clock_hub_v2.py

Плагин для отображения текущего времени и даты на экране вашего Pwnagotchi.
```
main.plugins.clock_hub_v2.enabled = true
main.plugins.clock_hub_v2.time_position = "50,60"
main.plugins.clock_hub_v2.date_position = "50,70"
```

2. display_password_hub_v2.py

Этот плагин отображает SSID и пароли недавно взломанных сетей полученных с [Wpa-Sec](https://wpa-sec.stanev.org).
```
main.plugins.display_password_hub_v2.enabled = true
main.plugins.display_password_hub_v2.ssid_position = "0,91"
main.plugins.display_password_hub_v2.password_position = "0,101"
```
3. memtemp_hub_v2.py

Плагин, отображает использование памяти, загрузку CPU, температуру и частоту процессора. 
```

main.plugins.memtemp_hub_v2.enabled = true
main.plugins.memtemp_hub_v2.scale = "celsius"
main.plugins.memtemp_hub_v2.fields = "mem,cpu,temp,freq"
main.plugins.memtemp_hub_v2.mem_position = "210,80"
main.plugins.memtemp_hub_v2.cpu_position = "210,87"
main.plugins.memtemp_hub_v2.temp_position = "210,94"
main.plugins.memtemp_hub_v2.freq_position = "210,101"
main.plugins.memtemp_hub_v2.time_position = "50,60"
main.plugins.memtemp_hub_v2.date_position = "50,70"
```

## Установка и настройка

Вы можете вписать данный репозиторий в config.toml:
```
main.custom_plugin_repos = [
    "https://github.com/evilsocket/pwnagotchi-plugins-contrib/archive/master.zip",
    "https://github.com/jayofelony/pwnagotchi-torch-plugins/archive/master.zip",
    "https://github.com/tisboyo/pwnagotchi-pisugar2-plugin/archive/master.zip",
    "https://github.com/nullm0ose/pwnagotchi-plugin-pisugar3/archive/master.zip",
    "https://github.com/Sniffleupagus/pwnagotchi_plugins/archive/master.zip",
    "https://github.com/NeonLightning/pwny/archive/master.zip",
    "https://github.com/marbasec/UPSLite_Plugin_1_3/archive/master.zip",
    "https://github.com/Exnuz/pwnagotchi-plugins-v2/archive/heads/master.zip", #<-- Наш репозиторий
]
```
Обратите внимание что в config.toml не должно быть повторов!

Узнать список и версии всех плагинов:
```pwnagotchi plugins list```

С помощью команд можете скачать и обновить все плагины которые настроены на устройстве:
```
pwnagotchi plugins update
pwnagotchi plugins upgrade
```

Включить плагины можно как через WebUi, так и через команды:
```
pwnagotchi plugins install 'Название плагина'
pwnagotchi plugins enable 'Название плагина'
```


* Присоединяйтесь к нам!
Если вам интересны обсуждения и нужна помощь по Pwnagotchi, присоединяйтесь к нашей группе в Telegram: [Pwnagotchi](https://t.me/pwnagotchi)
