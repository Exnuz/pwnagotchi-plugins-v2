# Импорт библиотек
import logging
import pwnagotchi
import pwnagotchi.plugins as plugins
import pwnagotchi.ui.fonts as fonts
from pwnagotchi.ui.components import LabeledValue
from pwnagotchi.ui.view import BLACK

# Информация об авторе и версии
class MemTempHubv2(plugins.Plugin):
    __author__ = 'Exnuz'
    __version__ = '2.0.2'
    __license__ = 'GPL3'
    __description__ = 'A plugin that displays memory usage, CPU load, temperature, and frequency.'

    # Параметры для настройки в config.toml
    # main.plugins.memtemp_hub_v2.enabled = true
    # main.plugins.memtemp_hub_v2.scale = "celsius"
    # main.plugins.memtemp_hub_v2.fields = "mem,cpu,temp,freq"
    # main.plugins.memtemp_hub_v2.mem_position = "210,80"
    # main.plugins.memtemp_hub_v2.cpu_position = "210,87"
    # main.plugins.memtemp_hub_v2.temp_position = "210,94"
    # main.plugins.memtemp_hub_v2.freq_position = "210,101"

    # Разрешенные поля и поля по умолчанию
    ALLOWED_FIELDS = {
        'mem': 'mem_usage',
        'cpu': 'cpu_load',
        'temp': 'cpu_temp',
        'freq': 'cpu_freq',
    }
    DEFAULT_FIELDS = ['mem', 'cpu', 'temp', 'freq']

    # Логика загрузки плагина
    def on_loaded(self):
        logging.info('[MemTemp_Hub_v2] Plugin loaded.')

    # Получение использования памяти
    def mem_usage(self):
        try:
            return f'{int(pwnagotchi.mem_usage() * 100)}%'
        except Exception as e:
            logging.error(f'[MemTemp_Hub_v2] Error getting memory usage: {e}')
            return 'N/A'

    # Получение загрузки CPU
    def cpu_load(self):
        try:
            return f'{int(pwnagotchi.cpu_load() * 100)}%'
        except Exception as e:
            logging.error(f'[MemTemp_Hub_v2] Error getting CPU load: {e}')
            return 'N/A'

    # Получение температуры CPU
    def cpu_temp(self):
        try:
            scale = self.options.get('scale', 'celsius').lower()
            if scale == 'fahrenheit':
                temp = (pwnagotchi.temperature() * 9 / 5) + 32
                symbol = 'F'
            elif scale == 'kelvin':
                temp = pwnagotchi.temperature() + 273.15
                symbol = 'K'
            else:
                temp = pwnagotchi.temperature()
                symbol = 'C'
            return f'{temp:.1f}{symbol}'
        except Exception as e:
            logging.error(f'[MemTemp_Hub_v2] Error getting CPU temperature: {e}')
            return 'N/A'

    # Получение частоты CPU
    def cpu_freq(self):
        try:
            with open('/sys/devices/system/cpu/cpu0/cpufreq/scaling_cur_freq', 'rt') as fp:
                return f'{round(float(fp.readline()) / 1000000, 1)}'
        except Exception as e:
            logging.error(f'[MemTemp_Hub_v2] Error getting CPU frequency: {e}')
            return 'N/A'

    # Настройка интерфейса
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
                ui.add_element(f'memtemp_{field}', LabeledValue(
                    color=BLACK,
                    label=f'{field.lower()}:',  # Отображаем маленькими буквами
                    value='N/A',
                    position=position,
                    label_font=fonts.Small,
                    text_font=fonts.Small,
                    label_spacing=-1,  # Уменьшаем расстояние между названием и значением
                ))

        except Exception as e:
            logging.error(f'[MemTemp_Hub_v2] Error setting up UI: {e}')

    # Обновление элементов интерфейса
    def on_ui_update(self, ui):
        try:
            for field in self.fields:
                ui.set(f'memtemp_{field}', getattr(self, self.ALLOWED_FIELDS[field])())
        except Exception as e:
            logging.error(f'[MemTemp_Hub_v2] Error updating UI: {e}')

    # Очистка при выгрузке плагина
    def on_unload(self, ui):
        try:
            with ui._lock:
                for field in self.fields:
                    ui.remove_element(f'memtemp_{field}')
        except Exception as e:
            logging.error(f'[MemTemp_Hub_v2] Error unloading UI elements: {e}')
