import subprocess
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.codeinput import CodeInput
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput


class MonitorApp(App):
    def build(self):
        layout = BoxLayout(orientation="vertical", padding=10, spacing=10)

        # Поле для ввода произвольной команды
        self.cmd_input = TextInput(
            hint_text="Введите shell-команду (например: ping -c 3 8.8.8.8)",
            multiline=False,
            size_hint_y=0.1,
        )
        layout.add_widget(self.cmd_input)

        # Панель с быстрыми кнопками
        btn_layout = BoxLayout(size_hint_y=0.1, spacing=5)

        btn_run = Button(text="Выполнить")
        btn_run.bind(on_press=self.execute_custom_cmd)

        btn_ifconfig = Button(text="ifconfig / ip a")
        btn_ifconfig.bind(
            on_press=lambda instance: self.run_command("ip a || ifconfig")
        )

        btn_ping = Button(text="Ping Google")
        btn_ping.bind(
            on_press=lambda instance: self.run_command("ping -c 3 8.8.8.8")
        )

        btn_layout.add_widget(btn_run)
        btn_layout.add_widget(btn_ifconfig)
        btn_layout.add_widget(btn_ping)
        layout.add_widget(btn_layout)

        # Область для вывода консольного лога
        self.output_area = CodeInput(
            text="Готов к работе...\n",
            readonly=True,
            size_hint_y=0.8,
        )
        layout.add_widget(self.output_area)

        return layout

    def execute_custom_cmd(self, instance):
        cmd = self.cmd_input.text.strip()
        if cmd:
            self.run_command(cmd)

    def run_command(self, command):
        self.output_area.text = f"$ {command}\nВыполнение...\n"
        try:
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=10,
            )
            stdout = result.stdout.strip()
            stderr = result.stderr.strip()

            output = ""
            if stdout:
                output += stdout + "\n"
            if stderr:
                output += f"[STDERR]\n{stderr}\n"
            if not output:
                output = "Команда выполнена без вывода.\n"

            self.output_area.text = f"$ {command}\n\n{output}"
        except subprocess.TimeoutExpired:
            self.output_area.text = (
                f"$ {command}\n\nОшибка: Превышено время ожидания (10 сек)."
            )
        except Exception as e:
            self.output_area.text = f"$ {command}\n\nОшибка выполнения: {str(e)}"


if __name__ == "__main__":
    MonitorApp().run()
