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
# webdriver ��� ���������� ���������
from selenium import webdriver

#��������� ���������� ������������
homepath = os.getenv('USERPROFILE')

#������� �������� ����� � ���������
def mail(mail_to, subject, filepath):
	mail_from = "testtest@gmail.com"
	password = '**********'
	smtp_server = "smtp.gmail.com" #������ SMTP ���������� 
	mail_port = 465 #���� ��� ����������� � SMTP ������� ����� SSL

	# ���������� ��������
	part = MIMEBase('application', "octet-stream")
	part.set_payload(open(filepath, "rb").read())
	encoders.encode_base64(part)
	part.add_header('Content-Disposition', "attachment; filename= %s" % os.path.basename(filepath))

	# ���������� ���������
	msg = MIMEMultipart()
	msg['Subject'] = subject
	msg['From'] = mail_from
	msg['To'] = mail_to
	msg.attach(part)

	# �������� ���������
	smtp = smtplib.SMTP_SSL(smtp_server, mail_port)
	smtp.login(mail_from, password)
	smtp.sendmail(mail_from, mail_to, msg.as_string())
	smtp.quit()        	

# �������������� ������� �������� Chrome
driver = webdriver.Chrome()
#��������� ���� ��������
driver.maximize_window()

time.sleep(1)

#1. ����� �� ���� google.ru
driver.get("https://google.ru")

#2. ���������, ��� ��������� ���� ������
try:
	#3. ����� � ���� ����� �������� ����������� ���� ��
	driver.find_element_by_name("q").send_keys("����������� ���� ��")
	time.sleep(1)
	#4. ������ �� ������ ����� � google
	driver.find_element_by_name("btnK").click()
except NoSuchElementException:
	print("�� �������� ��� ���� ����� ���������� ������� ��� ������ ������")
	driver.quit()
	exit()

time.sleep(1)

#5. ����� ������ �cbr.ru�
urlcbr = driver.find_element_by_partial_link_text("www.cbr.ru")
time.sleep(1)
#6. ������ �� ������ cbr.ru
urlcbr.click()

#������������ �� ����� ���� � ��������� ������� url-�����
window_after = driver.window_handles[1]
driver.switch_to_window(window_after)
url = driver.current_url

#7. ���������, ��� ������ ������ ����
if url[0:19] == "https://www.cbr.ru/":
	print("�� �� ����� ��");
	time.sleep(1)
	#8. ������ �� ������ ��������-��������
	driver.find_element_by_partial_link_text("��������-��������").click()
	time.sleep(1)
	#9. ������� ������ �������� �������������
	driver.find_element_by_partial_link_text("�������� �������������").click()
	time.sleep(1)
	#10. � ���� ���� ������������� ����� �������� ���������� �����
	driver.find_element_by_id("MessageBody").send_keys("��������� �����")
	time.sleep(1)
	#11. ��������� ������� �� ��������
	driver.find_element_by_id("_agreementFlag").click()
	time.sleep(2)
	#12. ������� �������� � ���������
	img = ImageGrab.grab()
	img.save(homepath + "\\screen1.jpg", "JPEG")
	time.sleep(2)
	#��������� ������������� ����� �� ����������
	if os.path.exists(homepath + "\\screen1.jpg"):
		#���������� ������ �������� �� ����� ����� � ������� ����
		mail("testtest@gmail.com", "������ �������� ������", homepath + "\\screen1.jpg")
		os.remove(homepath + "\\screen1.jpg")
	else:
		print("������ �������� �� ������")
	#13. ������ �� ������ ���� ������� #(������ �����, ����������� ����)
	driver.find_element_by_class_name("burger").click()
	time.sleep(1)
	#14. ������ �� ������ � �����
	driver.find_element_by_partial_link_text("� �����").click()
	#15. ������ �� ������ ��������������
	driver.find_element_by_link_text("��������������").click()
	#16.  ��������� ����� ��������������
	text_warning_ru = driver.find_element_by_id("content").text
	time.sleep(1)
	#17. ������� ���� �������� �� en (������ ����� ����)
	driver.find_element_by_link_text("EN").click()
	text_warning_en = driver.find_element_by_id("content").text
	#18. ���������, ��� ����� ���������� �� ������������ ������ �����
	if text_warning_ru != text_warning_en:
		print("����� ����������, ������ �������� � ���������� �� �����")
		#19. ������� �������� ��������� � ����
		img = ImageGrab.grab()
		img.save(homepath + "\\screen2.jpg", "JPEG")
		time.sleep(2)
		#��������� ������������� ����� �� ����������
		if os.path.exists(homepath + "\\screen2.jpg"):
			#���������� ������ �������� �� ����� ����� � ������� ����
			mail("testtest@gmail.com", "������ �������� ������", homepath + "\\screen2.jpg")
			os.remove(homepath + "\\screen2.jpg")
			print("��� ���� ���������, ���!!!)))")
		else:
			print("������ �������� �� ������")
	else:
		print("����� �� ���������, ���-�� ����� �� ���(((") 
else:
	print("��, ��������, �� �������� ������, �������...");

time.sleep(2)
# ������� ���� ��������
driver.quit()
exit()
# project
