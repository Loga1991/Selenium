import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@pytest.fixture(autouse=True)
def testing():
   pytest.driver = webdriver.Chrome()
# Переходим на страницу авторизации
   pytest.driver.get('http://petfriends.skillfactory.ru/login')

   yield

# Авторизация на сайте
def test_show_my_pets():

   # Вводим email
   pytest.driver.implicitly_wait(5)  # неявное ожидание
   pytest.driver.find_element(By.ID, 'email').send_keys('lozhkinagv@gmail.com')

   # Вводим пароль
   pytest.driver.find_element(By.ID, 'pass').send_keys('1234')

   # Входим в аккаунт
   WebDriverWait(pytest.driver, 3).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[type="submit"]'))) # явное ожидание
   pytest.driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()

   assert pytest.driver.find_element(By.CSS_SELECTOR, "h1").text == "PetFriends"
   pytest.driver.maximize_window()

   # Переходим на страницу пользователя
   pytest.driver.find_element(By.CSS_SELECTOR, '[href="/my_pets"]').click()

   images = pytest.driver.find_elements(By.CSS_SELECTOR, '.card-deck .card-img-top')  # определяем фото
   names = pytest.driver.find_elements(By.CSS_SELECTOR, '.card-deck .card-title')  # определяем имя
   descriptions = pytest.driver.find_elements(By.CSS_SELECTOR, '.card-deck .card-text')  # определяем вид и возраст

   try:

      for i in range(len(names)):  # перебираем все элементы

         assert images[i].get_attribute('src') != ''  # проверка наличия фото питомца (путь, указанный в атрибуте src, не пустой)
         assert names[i].text != ''  # проверка наличия имени питомца
         assert descriptions[i].text != ''  # проверяем, что не пустое, хотя в любом случае есть запятая
         assert ', ' in descriptions[i]  # убеждаемся в наличии запятой
         parts = descriptions[i].text.split(", ")  # разделяем строку на части
         assert len(parts[0]) > 0  # проверка наличия в первой части вида питомца
         assert len(parts[1]) > 0  # проверка наличия во второй части возраста питомца
   except AssertionError:
      print('Нет фото, имени, или возраста у одной из карточек питомца')

   #Задание 25.3.1

   # 1. Присутствуют все питомцы
   pet_count = pytest.driver.find_elements(By.CSS_SELECTOR, ".\\.col-sm-4.left")  # сохраняем в кол-во питомцев в счётчике с экранированием точки \\
   pets = pytest.driver.find_elements(By.CSS_SELECTOR, '.table.table-hover tbody tr')  # сохраняем в переменную карточки питомцев
   number = pet_count[0].text.split('\n')  # разбиваем строку по символу '\n' (первая строка "Питомцев: 3")
   number = number[1].split(' ')  # разделяем строку по пробелу и выбирает 2 элемент ("3")
   number = int(number[1])  # переводим в целое число
     # разделяем строку пробелами, выбираем 2 элемент, переводим в целое
   number_of_pets = len(pets) # количество карточек питомцев
   if number == number_of_pets:
      print("Число питомцев в таблице с совпадает с данными пользователя")

   else:
      print("Error")

   # 2. Хотя бы у половины питомцев есть фото
   images = pytest.driver.find_elements(By.CSS_SELECTOR, '.table.table-hover img')  # определяем карточки с фото
   number_of_images = len(images)  # количество карточек питомцев с фото
   print("Всего фото питомцев =", number_of_images)

   assert number_of_images >= number_of_pets / 2  # проверка количества карточек питомцев с фото (больше или равно кол-ву питомцев)

   # 3. У всех питомцев есть имя, возраст и порода
   pet_data = pytest.driver.find_elements(By.CSS_SELECTOR, '.table.table-hover tbody tr')  # определяем все данные питомцев
   try:
      for i in range(len(pet_data)):  # Перебираем все данные из pet_data
         data_pet = pet_data[i].text.replace('\n', '')  # удаляем \n (переходы на новую строку)
         split_data_pet = data_pet.split(' ')  # разделяем строку по пробелу
         result = len(split_data_pet)  # количество элементов в получившемся списке
         assert result == 3  # проверяем, что в каждой строке td есть значение
   except AssertionError:
      print("Нет фото, имя, возраста, или породы  по крайней мере у одной из карточек питомца")

   # 4. У всех питомцев разные имена
   names = pytest.driver.find_elements(By.CSS_SELECTOR, '.table.table-hover tbody tr td')  # определяем все имена питомцев
   list_names_of_my_pets = []  # создаем список для хранения имен питомцев
   try:
      for i in range(len(names)):  # перебираем все элементы в списке names
         list_names_of_my_pets.append(names[i].text)  # сохраняем в список list_names_of_my_pets

      set_pet_data = set(list_names_of_my_pets)  # преобразовываем список в множество, что бы исключить дубликаты
      assert len(list_names_of_my_pets) == len(set_pet_data)  # проверяем, что количество имен в списке
      # list_names_of_my_pets равно кол-ву множества set_pet_data
   except AssertionError:
      print("Есть одинаковые имена питомцев")

   # 5. В списке нет повторяющихся питомцев
   set_data = []  # создаем множество для хранения элементов в списке
   keys = 0  # счетчик карточек питомцев
   for i in range(len(pet_data)):  # перебираем все элементы в списке pet_data
      split_data_pet = pet_data[i].text.split("\n").pop(0)  # удаляем '×', разделяем строку по переносу
      set_data.append(split_data_pet)
      keys += 1  # счетчик ключей

   set_data = set(set_data)  # преобразовываем множество в множество, что бы исключить дубликаты
   print("Если убрать повторяющиеся имена, всего питомцев =", len(set_data))  # выводим количество элементов в списке set_data
   try:
      assert len(set_data) == keys  # проверяем, что количество элементов в списке set_data равно кол-ву ключей
   except AssertionError:
      print("В списке есть повторяющиеся питомцы")

   pytest.driver.quit()