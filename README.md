# calculator
## Принятые при работе условия
1.	Приложение округляет значения до сотых
2.	Приложение поддерживает работу с отрицательными числами, в том числе их ввод
3.	Приложение отображает число в экспоненциальной форме, если длина его целой части составляет более 20 знаков
4.	Приложение корректно обрабатывает числа (без погрешности), у которых длина целой части не превышает 20 знаков, выводя при этом число в обычном представлении
5.	Кнопка «RESET» сбрасывает как введённые в поля ввода числа, так и результат расчёта
6.	При делении на «0» приложение в результате расчёта выводит сообщение «Делить на «0» нельзя»
7.	Поворот экрана не влияет на введённые в поля ввода числа и на результат расчёта

## Инструкция по запуску автотестов
Автотесты были написаны на языке python.
Инструкция для Windows.
1.	Установить Appium 1.18.0 (ссылка для скачивания http://appium.io/ ), 
2.	Установить Appium-Python-Client 1.0.2 (инструкция по установке https://pypi.org/project/Appium-Python-Client/)
3.	Установить Python 3.8.0 (ссылка для скачивания https://www.python.org/downloads/ )
4.	Установить Selenium для Python (инструкция по установке https://habr.com/ru/post/248559/ )
5.	Установить Android SDK (https://developer.android.com/studio/index.html)
6.	Установить системную переменную ANDROID_SDK_ROOT и указать там путь к Android SDK (например C:\Users\str\AppData\Local\Android\sdk)
7.	Установить системную переменную JAVA_HOME и указать там путь к папке с Java (например C:\Program Files\Java\jdk-12.0.2)
8.	Настроить параметры устройства в словаре Desired Capabilities в соотвествии с документацией  (http://appium.io/docs/en/about-appium/getting-started/ ) (файл с кодом «calculator_Vasilevskaya.py» словарь desired_caps, строка 10)
Например:

```python
  desired_caps = {
    "deviceName": "my",  # вместо «my» можно вписать любое значение
    "platformName": "android", # название ОС устройства
    "platformVersion": "10", # номер версии ОС устройства
    "udid": "3173a32", # id тестируемого устройства
    "appPackage": "com.vbanthia.androidsampleapp", # не изменять
    "appActivity": "com.vbanthia.androidsampleapp.MainActivity"  # не изменять
  }
```
«udid»  можно узнать с помощью команды «adb devices»

9.	Запустить сервер Appium (кнопка «Start Server v1.18.0»)
10.	Подключить устройство, где будет тестироваться приложение
11.	На устройстве включить режим разработчика и включить режим отладки по USB
12.	Запустить тест «python calculator_Vasilevskaya_QA.py»


## Функции, которые проверяет автотест
1. Функция "Сложение", "Вычитание", "Умножение" и "Деление" (функция test)
2. Проверка работы кнопки "RESET" (функция resetTest)
3. Проверка неизменности введённых данных и результата расчёта после поворота экрана (функция rotateTest)
4. Проверка ввода пустых значений (функция testEmpty)
