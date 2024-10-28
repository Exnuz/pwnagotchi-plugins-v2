# Импорт библиотек
import logging
import datetime
import pwnagotchi
import pwnagotchi.plugins as plugins
import pwnagotchi.ui.fonts as fonts
from pwnagotchi.ui.components import LabeledValue
from pwnagotchi.ui.view import BLACK

# Информация об авторе и версии
class ClockHubv2(plugins.Plugin):
    __author__ = 'Exnuz'
    __version__ = '2.0.0'
    __license__ = 'GPL3'
    __description__ = 'Clock/Date for pwnagotchi'

    # Параметры для настройки в config.toml
    # main.plugins.clock_hub_v2.enabled = true
    # main.plugins.clock_hub_v2.time_position = "50,60"
    # main.plugins.clock_hub_v2.date_position = "50,70"

    # Логика загрузки плагина
    def on_loaded(self):
        logging.info('[Clock_HUB_v2] Plugin loaded.')

    # Функция обновления времени
    def update_time(self):
        try:
            now = datetime.datetime.now()
            date_str = now.strftime("%d/%m/%y")
            time_str = now.strftime("%H:%M:%S")
            return date_str, time_str
        except Exception as e:
            logging.error(f'[Clock-HUB] Error updating time: {e}')
            return 'N/A', 'N/A'

    # Настройка интерфейса (с поддержкой различных экранов)
    def on_ui_setup(self, ui):
        try:
            # Получение позиций из конфигурации с значениями по умолчанию
            time_pos = self.options.get('time_position', '50,60')
            date_pos = self.options.get('date_position', '50,70')
            
            # Конвертация позиций из строк в кортежи
            time_pos = tuple(map(int, time_pos.split(',')))
            date_pos = tuple(map(int, date_pos.split(',')))

            # Проверка экрана и установка позиций
            if ui.is_waveshare_1():
                time_pos = (50, 60)
                date_pos = (50, 70)
            elif ui.is_waveshare_2():
                time_pos = (60, 60)
                date_pos = (60, 70)
            elif ui.is_waveshare_3():
                time_pos = (70, 60)
                date_pos = (70, 70)
            elif ui.is_waveshare_4():
                time_pos = (80, 60)
                date_pos = (80, 70)
            else:
                time_pos = (00, 91)
                date_pos = (00, 101)       

            # Добавление элементов на интерфейс
            ui.add_element('clock_date', LabeledValue(
                color=BLACK,
                label='',
                value='-/-/-',
                position=date_pos,
                label_font=fonts.Small,
                text_font=fonts.Small
            ))
            ui.add_element('clock_time', LabeledValue(
                color=BLACK,
                label='',
                value='--:--:--',
                position=time_pos,
                label_font=fonts.Small,
                text_font=fonts.Small
            ))
        except Exception as e:
            logging.error(f'[Clock_HUB_v2] Error setting up UI: {e}')

    # Обновление элементов интерфейса
    def on_ui_update(self, ui):
        try:
            date_str, time_str = self.update_time()
            ui.set('clock_date', date_str)
            ui.set('clock_time', time_str)
        except Exception as e:
            logging.error(f'[Clock_HUB_v2] Error updating UI: {e}')

    # Очистка при выгрузке плагина
    def on_unload(self, ui):
        try:
            with ui._lock:
                ui.remove_element('clock_date')
                ui.remove_element('clock_time')
        except Exception as e:
            logging.error(f'[Clock_HUB_v2] Error unloading UI elements: {e}')
