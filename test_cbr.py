# -*- coding: windows-1251 -*-
import time
from PIL import Image, ImageGrab
from selenium.webdriver.common.action_chains import ActionChains
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders
import os
from selenium.common.exceptions import NoSuchElementException
# webdriver для управления браузером
from selenium import webdriver

#Определим директорию пользователя
homepath = os.getenv('USERPROFILE')

#Функция отправки почты с вложением
def mail(mail_to, subject, filepath):
	mail_from = "testtest@gmail.com"
	password = '**********'
	smtp_server = "smtp.gmail.com" #Сервер SMTP получателя 
	mail_port = 465 #Порт для подключения к SMTP серверу через SSL

	# Подготовим вложение
	part = MIMEBase('application', "octet-stream")
	part.set_payload(open(filepath, "rb").read())
	encoders.encode_base64(part)
	part.add_header('Content-Disposition', "attachment; filename= %s" % os.path.basename(filepath))

	# Подготовим сообщение
	msg = MIMEMultipart()
	msg['Subject'] = subject
	msg['From'] = mail_from
	msg['To'] = mail_to
	msg.attach(part)

	# Отправим сообщение
	smtp = smtplib.SMTP_SSL(smtp_server, mail_port)
	smtp.login(mail_from, password)
	smtp.sendmail(mail_from, mail_to, msg.as_string())
	smtp.quit()        	

# Инициализируем драйвер браузера Chrome
driver = webdriver.Chrome()
#Развернем окно браузера
driver.maximize_window()

time.sleep(1)

#1. Зашли на сайт google.ru
driver.get("https://google.ru")

#2. Проверили, что появилось поле “поиск”
try:
	#3. Ввели в поле поиск значение Центральный банк РФ
	driver.find_element_by_name("q").send_keys("Центральный банк РФ")
	time.sleep(1)
	#4. Нажали на кнопку поиск в google
	driver.find_element_by_name("btnK").click()
except NoSuchElementException:
	print("На странице нет поля ввода поискового запроса или кнопки поиска")
	driver.quit()
	exit()

time.sleep(1)

#5. Нашли ссылку “cbr.ru”
urlcbr = driver.find_element_by_partial_link_text("www.cbr.ru")
time.sleep(1)
#6. Нажали на ссылку cbr.ru
urlcbr.click()

#Переключимся на новое окно и определим текущий url-адрес
window_after = driver.window_handles[1]
driver.switch_to_window(window_after)
url = driver.current_url

#7. Проверили, что открыт нужный сайт
if url[0:19] == "https://www.cbr.ru/":
	print("Мы на сайте ЦБ");
	time.sleep(1)
	#8. Нажали на ссылку Интернет-приемная
	driver.find_element_by_partial_link_text("Интернет-приемная").click()
	time.sleep(1)
	#9. Открыли раздел Написать благодарность
	driver.find_element_by_partial_link_text("Написать благодарность").click()
	time.sleep(1)
	#10. В поле Ваша благодарность ввели значение “случайный текст”
	driver.find_element_by_id("MessageBody").send_keys("Случайный текст")
	time.sleep(1)
	#11. Поставили галочку “Я согласен”
	driver.find_element_by_id("_agreementFlag").click()
	time.sleep(2)
	#12. Сделали скриншот и сохранили
	img = ImageGrab.grab()
	img.save(homepath + "\\screen1.jpg", "JPEG")
	time.sleep(2)
	#Проверяем существование файла со скриншотом
	if os.path.exists(homepath + "\\screen1.jpg"):
		#Отправляем первый скриншот на любую почту и удаляем файл
		mail("testtest@gmail.com", "Первое тестовое письмо", homepath + "\\screen1.jpg")
		os.remove(homepath + "\\screen1.jpg")
	else:
		print("Первый скриншот не найден")
	#13. Нажали на кнопку “Три полоски” #(Сверху слева, открывающая меню)
	driver.find_element_by_class_name("burger").click()
	time.sleep(1)
	#14. Нажали на раздел О сайте
	driver.find_element_by_partial_link_text("О сайте").click()
	#15. Нажали на ссылку предупреждение
	driver.find_element_by_link_text("Предупреждение").click()
	#16.  Запомнили текст предупреждения
	text_warning_ru = driver.find_element_by_id("content").text
	time.sleep(1)
	#17. Сменили язык страницы на en (сверху выбор есть)
	driver.find_element_by_link_text("EN").click()
	text_warning_en = driver.find_element_by_id("content").text
	#18. Проверили, что текст отличается от запомненного текста ранее
	if text_warning_ru != text_warning_en:
		print("Текст отличается, делаем скриншот и отправляем на почту")
		#19. Сделали скриншот сохранили в файл
		img = ImageGrab.grab()
		img.save(homepath + "\\screen2.jpg", "JPEG")
		time.sleep(2)
		#Проверяем существование файла со скриншотом
		if os.path.exists(homepath + "\\screen2.jpg"):
			#Отправляем первый скриншот на любую почту и удаляем файл
			mail("testtest@gmail.com", "Второе тестовое письмо", homepath + "\\screen2.jpg")
			os.remove(homepath + "\\screen2.jpg")
			print("Все шаги выполнены, Ура!!!)))")
		else:
			print("Первый скриншот не найден")
	else:
		print("Текст не изменился, что-то пошло не так(((") 
else:
	print("Ой, извините, мы ошиблись сайтом, выходим...");

time.sleep(2)
# Закроем окно браузера
driver.quit()
exit()
# project
