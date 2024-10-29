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
    __version__ = '2.0.3'
    __license__ = 'GPL3'
    __description__ = 'Plugin to display hacked network SSID and password screen'

    # Параметры для настройки в config.toml
    # main.plugins.display_password_hub_v2.enabled = true
    # main.plugins.display_password_hub_v2.fields = "ssid,password"
    # main.plugins.display_password_hub_v2.ssid_label = "SSID"
    # main.plugins.display_password_hub_v2.password_label = "Pass"
    # main.plugins.display_password_hub_v2.ssid_position = "40,94"
    # main.plugins.display_password_hub_v2.password_position = "40,101"

    ALLOWED_FIELDS = {
        'ssid': 'get_last_network_and_password',
        'password': 'get_last_network_and_password'
    }
    DEFAULT_FIELDS = ['ssid', 'password']
    
    DEFAULT_LABELS = {
        'ssid': 'SSID',
        'password': 'Password'
    }

    DEFAULT_POSITIONS = {
        'ssid': '40,94',  # Значение по умолчанию для SSID
        'password': '40,101'  # Значение по умолчанию для пароля
    }

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

    # Настройка интерфейса (без проверки типов экранов)
    def on_ui_setup(self, ui):
        try:
            # Получение списка полей из конфигурации
            self.fields = self.options.get('fields', ','.join(self.DEFAULT_FIELDS)).split(',')
            self.fields = [x.strip() for x in self.fields if x.strip() in self.ALLOWED_FIELDS.keys()]

            # Добавление элементов на интерфейс
            for field in self.fields:
                # Получение позиций для каждого поля с учетом значений по умолчанию
                position_str = self.options.get(f'{field}_position', self.DEFAULT_POSITIONS[field])
                position = tuple(map(int, position_str.split(',')))

                # Получение названий из конфигурации
                label = self.options.get(f'{field}_label', self.DEFAULT_LABELS[field])

                # Добавление элемента на интерфейс
                ui.add_element(f'display_{field}', LabeledValue(
                    color=BLACK,
                    label=label,  # Устанавливаем название из конфигурации
                    value='N/A',
                    position=position,
                    label_font=fonts.Bold,
                    text_font=fonts.Small,
                    label_spacing=0,  # Уменьшаем расстояние между названием и значением
                ))

        except Exception as e:
            logging.error(f'[DisplayPassword_HUB_v2] Error setting up UI: {e}')

    def on_ui_update(self, ui):
        try:
            ssid, password = self.get_last_network_and_password()
            ui.set('display_ssid', ssid)
            ui.set('display_password', password)
        except Exception as e:
            logging.error(f'[DisplayPassword_HUB_v2] Error updating UI: {e}')

    def on_unload(self, ui):
        try:
            with ui._lock:
                for field in self.fields:
                    ui.remove_element(f'display_{field}')
        except Exception as e:
            logging.error(f'[DisplayPassword_HUB_v2] Error unloading UI elements: {e}')
