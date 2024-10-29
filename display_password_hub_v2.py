# Импорт библиотек
import logging
import os
import pwnagotchi.plugins as plugins
import pwnagotchi.ui.fonts as fonts
from pwnagotchi.ui.components import LabeledValue
from pwnagotchi.ui.view import BLACK

# Информация об авторе и версии
class DisplayPasswordHubv2(plugins.Plugin):
    __author__ = 'Exnuz'
    __version__ = '2.0.0'
    __license__ = 'GPL3'
    __description__ = 'Plugin to display hacked network SSID and password screen'
    
    # Параметры для настройки в config.toml
    # main.plugins.display_password_hub_v2.enabled = true
    # main.plugins.display_password_hub_v2.ssid_position = "0,91"
    # main.plugins.display_password_hub_v2.password_position = "0,101"

    def on_loaded(self):
        logging.info("[DisplayPassword_HUB_v2] Plugin loaded.")

    def get_last_network_and_password(self):
        try:
            last_line_command = 'tail -n 1 /root/handshakes/wpa-sec.cracked.potfile'
            last_line = os.popen(last_line_command).read().rstrip()
            
            if last_line:
                parts = last_line.split(':')
                if len(parts) >= 4:
                    ssid = parts[2]
                    password = parts[3]
                    return ssid, password
                else:
                    return "SSID not found", "Password not found"
            else:
                return "SSID not found", "Password not found"
        except Exception as e:
            logging.error(f'[DisplayPassword_HUB_v2] Error getting last SSID and password: {e}')
            return 'N/A', 'N/A'

    # Настройка интерфейса с поддержкой различных экранов
    def on_ui_setup(self, ui):
        try:
            # Получение позиций из конфигурации
            ssid_pos_str = self.options.get('ssid_position', '0,91')
            password_pos_str = self.options.get('password_position', '0,97')
            
            ssid_position = tuple(map(int, ssid_pos_str.split(',')))
            password_position = tuple(map(int, password_pos_str.split(',')))

            # Проверка экрана и корректировка позиций
            if ui.is_waveshare_v1():
                ssid_position = (50, 91)
                password_position = (50, 101)
            elif ui.is_waveshare_v2():
                ssid_position = (60, 91)
                password_position = (60, 101)
            elif ui.is_waveshare_v3():
                ssid_position = (70, 91)
                password_position = (70, 101)
            elif ui.is_waveshare_v4():
                ssid_position = (80, 91)
                password_position = (80, 101)

            # Добавление элементов на интерфейс
            ui.add_element('display_ssid', LabeledValue(
                color=BLACK,
                label='', # Пустая метка, можно добавить "SSID:" если нужно
                value='',
                position=ssid_position,
                label_font=fonts.Bold,
                text_font=fonts.Small
            ))
            ui.add_element('display_password', LabeledValue(
                color=BLACK,
                label='', # Пустая метка, можно добавить "Пароль:" если нужно
                value='',
                position=password_position,
                label_font=fonts.Bold,
                text_font=fonts.Small
            ))
        except Exception as e:
            logging.error(f'[DisplayPassword_HUB_v2] Error when setting up the interface: {e}')

    def on_ui_update(self, ui):
        try:
            ssid, password = self.get_last_network_and_password()
            ui.set('display_ssid', ssid)
            ui.set('display_password', password)
        except Exception as e:
            logging.error(f'[DisplayPassword_HUB_v2] Error during update UI: {e}')

    def on_unload(self, ui):
        try:
            with ui._lock:
                ui.remove_element('display_ssid')
                ui.remove_element('display_password')
        except Exception as e:
            logging.error(f'[DisplayPassword_HUB_v2] Error when unloading elements UI: {e}')
