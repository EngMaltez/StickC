"""Display alignment test.

@date 20200919
"""

def display_7seg_test(string, dist, width, outline=True):
	"""Seven segment N digit display test."""
	lcd.setRotation(1)
	lcd.font(lcd.FONT_Default)
	lcd.print("7-segment", 0,0)

	lcd.font(lcd.FONT_7seg)
	lcd.attrib7seg(dist, width, outline, lcd.GREEN)
	fs = lcd.fontSize()
	for x in range(0,160, fs[0]+2):
		lcd.rect(x ,80-fs[1], fs[0], fs[1], lcd.MAGENTA)
	lcd.text(0, 80-fs[1], string, lcd.RED)

	lcd.font(lcd.FONT_Default)
	lcd.print("\n{}".format(fs), 0, 0)
	counter = 0
	while True:
		lcd.print("{:.2f} V".format(axp.getBatVoltage()), lcd.RIGHT, 0)
		lcd.print("{}".format(counter), lcd.RIGHT, lcd.fontSize()[1])
		counter += 1
		wait_ms(500)

# 5 digits of 7-seg
# display_7seg_test("12:34", 16, 3)
# 8 digits of 7-seg
# display_7seg_test("12:34:56", 8, 2)
# 10 digits of 7-seg
display_7seg_test("2020-09-19", 7, 1, False)
