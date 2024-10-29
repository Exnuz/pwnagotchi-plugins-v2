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
    __version__ = '2.0.2'
    __license__ = 'GPL3'
    __description__ = 'Plugin to display hacked network SSID and password screen'

    # Параметры для настройки в config.toml
    # main.plugins.display_password_hub_v2.enabled = true
    # main.plugins.display_password_hub_v2.fields = "ssid,password"
    # main.plugins.display_password_hub_v2.ssid_position = "0,91"
    # main.plugins.display_password_hub_v2.password_position = "0,97"

    ALLOWED_FIELDS = {
        'ssid': 'get_last_network_and_password',
        'password': 'get_last_network_and_password'
    }
    DEFAULT_FIELDS = ['ssid', 'password']

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
            # Получение списка полей из конфигурации
            self.fields = self.options.get('fields', ','.join(self.DEFAULT_FIELDS)).split(',')
            self.fields = [x.strip() for x in self.fields if x.strip() in self.ALLOWED_FIELDS.keys()]

            # Добавление элементов на интерфейс
            for field in self.fields:
                # Получение позиций для каждого поля
                position_str = self.options.get(f'{field}_position', '0,0')
                position = tuple(map(int, position_str.split(',')))

                # Добавление элемента на интерфейс
                ui.add_element(f'display_{field}', LabeledValue(
                    color=BLACK,
                    label=f'{field.lower()}:',  # Отображаем маленькими буквами
                    value='N/A',
                    position=position,
                    label_font=fonts.Bold,
                    text_font=fonts.Small,
                    label_spacing=-1,  # Уменьшаем расстояние между названием и значением
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
