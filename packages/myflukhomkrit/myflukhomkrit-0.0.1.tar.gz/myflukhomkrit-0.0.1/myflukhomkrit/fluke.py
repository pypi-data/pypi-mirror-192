class FluKhomkrit:
	"""
	คลาส FluKhomkrit คือ ข้อมูลของนายคมตู่
	ประกอบด้วยชื่อเพจ
	ชื่อยูทูป

	Examle
	#-------------------------
	fluk = FluKhomkrit()
	fluk.show_name()
	fluk.show_youtube()
	fluk.adout()
	#-------------------------
	"""
	def __init__(self):
		self.name = 'คุณคมตู่'
		self.page = 'https://web.facebook.com/khomkit.fook'

	def show_name(self):
		print(f'สวัสดีฉันชื่อ {self.name}')

	def show_youtube(self):
		print('https://www.youtube.com/watch?v=O8YqI8IwFk4')

	def adout(self):
		text = """
		กกกกกกกกกกกกกกกกกกกกกกกกกกกกกกกกกกกกกกก
		ขขขขขขขขขขขขขข 'ฟลุ๊ค' ขขขขขขขขขขขขขขขข
		คคคคคคคคคคคคคคคคคคคคคคคคคคคคคคคคคคคคคคค
		งงงงงงงงงงงงงงงงงงงงงงงงงงงงงงงงงงงงงงงงงงงงงงงงงงงงงงงงง
		"""
		print(text)

if __name__ == '__main__':
	fluk = FluKhomkrit()
	fluk.show_name()
	fluk.show_youtube()
	fluk.adout()