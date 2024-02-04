import sqlite3
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput


class LoginRegisterApp(App):
    def build(self):
        self.conn = sqlite3.connect("users.db")
        self.cursor = self.conn.cursor()

        self.cursor.execute(
            "CREATE TABLE IF NOT EXISTS users (username TEXT, password TEXT)"
        )
        self.conn.commit()

        self.layout = GridLayout(rows=4, cols=2)

        self.layout.add_widget(Label(text="Username:"))
        self.username_input = TextInput(multiline=False)
        self.layout.add_widget(self.username_input)

        self.layout.add_widget(Label(text="Password:"))
        self.password_input = TextInput(password=True, multiline=False)
        self.layout.add_widget(self.password_input)

        self.register_button = Button(text="Register", on_press=self.handle_register)
        self.layout.add_widget(self.register_button)

        self.login_button = Button(text="Login", on_press=self.handle_login)
        self.layout.add_widget(self.login_button)

        return self.layout

    def handle_register(self, instance):
        username = self.username_input.text
        password = self.password_input.text

        if self.validate_input(username, password):
            self.cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
            user = self.cursor.fetchone()
            if user:
                print("Такой пользователь уже есть!")
            else:
                self.cursor.execute("INSERT INTO users VALUES (?, ?)", (username, password))
                self.conn.commit()
                self.username_input.text = ''
                self.password_input.text = ''
                print("Регистрация успешна!")     
        else:
            print("Не все поля заполнены!")

    def handle_login(self, instance):
        username = self.username_input.text
        password = self.password_input.text

        if self.validate_input(username, password):
            self.cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
            user = self.cursor.fetchone()

            if user:
                print("Вы вошли!")
            else:
                print("Такого пользователя нет!")    
        else:
            print("Не все поля заполнены!")

    def validate_input(self, username, password):
        if username.strip() == '' or password.strip() == '':
            return False
        return True

    def on_stop(self):
        self.conn.close()


if __name__ == '__main__':
    LoginRegisterApp().run()