import os
import subprocess
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput
from kivy.clock import Clock


class LogAndProcessMonitor(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', padding=10, spacing=10, **kwargs)

        # Верхняя панель управления
        btn_layout = BoxLayout(size_hint_y=None, height=50, spacing=10)
        
        self.btn_logs = Button(text="Показать Logcat", on_press=self.get_logcat)
        self.btn_procs = Button(text="Процессы (PS)", on_press=self.get_processes)
        self.btn_clear = Button(text="Очистить", on_press=self.clear_output)
        
        btn_layout.add_widget(self.btn_logs)
        btn_layout.add_widget(self.btn_procs)
        btn_layout.add_widget(self.btn_clear)
        self.add_widget(btn_layout)

        # Поле вывода логов
        self.output = TextInput(
            readonly=True, 
            multiline=True, 
            font_size=12,
            background_color=(0.1, 0.1, 0.1, 1),
            foreground_color=(0, 1, 0, 1)
        )
        self.add_widget(self.output)

        # Статус-бар
        self.status = Label(text="Готов к работе", size_hint_y=None, height=30)
        self.add_widget(self.status)

    def run_command(self, command):
        try:
            result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=5)
            return result.stdout if result.stdout else result.stderr
        except Exception as e:
            return f"Ошибка выполнения: {str(e)}"

    def get_logcat(self, instance):
        self.status.text = "Чтение Logcat..."
        # Чтем последние 100 строк лога
        output_text = self.run_command("logcat -d -t 100")
        self.output.text = output_text if output_text else "Не удалось получить Logcat (требуются права/ADB)."
        self.status.text = "Logcat обновлен"

    def get_processes(self, instance):
        self.status.text = "Получение списка процессов..."
        # Выполняем команду ps для просмотра процессов
        output_text = self.run_command("ps -A || ps")
        self.output.text = output_text if output_text else "Не удалось получить список процессов."
        self.status.text = "Список процессов обновлен"

    def clear_output(self, instance):
        self.output.text = ""
        self.status.text = "Очищено"


class MonitorApp(App):
    def build(self):
        self.title = "Process & Log Monitor"
        return LogAndProcessMonitor()


if __name__ == "__main__":
    MonitorApp().run()
