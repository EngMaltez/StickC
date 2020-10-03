"""A 7-segment display Clock.

@author Miguel Maltez Jose
@date 20200923
"""
# from m5stack import M5Led
from m5stack import *
from m5ui import *
from uiflow import *
import network
import socket, struct
import time, machine

def connectToWifi(essid, password):
	"""Setup WiFi."""
	sta_if = network.WLAN(network.STA_IF)
	sta_if.active(True)
	lcd.font(lcd.FONT_Default)
	lcd.print("WiFi " + "active" if sta_if.active() else "inactive", 0,0, lcd.YELLOW)
	trycount = 0
	while not sta_if.isconnected():
		sta_if.connect(essid, password)
		lcd.print(".")
		time.sleep(2)
		trycount += 1
		if trycount > 10:
			break
	return sta_if

def getNTPTime(host = "pool.ntp.org"):
	"""Get time from Network Time Protocol."""
	## (date(2000, 1, 1) - date(1900, 1, 1)).days * 24*60*60
	NTP_DELTA = 3155673600
	NTP_QUERY = bytearray(48)
	NTP_QUERY[0] = 0x1B
	addr = socket.getaddrinfo(host, 123)[0][-1]
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	try:
		s.settimeout(1)
		res = s.sendto(NTP_QUERY, addr)
		msg = s.recv(48)
	finally:
		s.close()
	val = struct.unpack("!I", msg[40:44])[0]
	return val - NTP_DELTA

def updateRTC():
	"""Get NTP and set the RTC."""
	lt = getNTPTime() + 3600
	tm = time.localtime(lt)
	# machine.RTC().datetime((tm[0], tm[1], tm[2], tm[6] + 1, tm[3], tm[4], tm[5], 0))
	rtc.setTime(tm[0], tm[1], tm[2], tm[3], tm[4], tm[5])

class BatteryDisplay:
	def __init__(self):
		self.vbatt = 4.0
		self.ibatt = 0.0
		self.dirty = True
		self.color = lcd.WHITE
	def update(self):
		self.vbatt = axp.getBatVoltage()
		self.ibatt = axp.getBatCurrent()
		if axp.getChargeState():
			self.color = lcd.CYAN
		else:
			self.color = lcd.WHITE
	def render(self):
		lcd.font(lcd.FONT_Default)
		lcd.print("{:.2f}V".format(self.vbatt), lcd.RIGHT, 0, self.color)
		lcd.print("{:.0f}mA".format(self.ibatt), lcd.RIGHT, lcd.fontSize()[1], self.color)
	def isDirty(self):
		return self.dirty


class Clock:
	def __init__(self):
		lcd.font(lcd.FONT_7seg)
		lcd.attrib7seg(8, 2, True, lcd.GREEN)
		fs = lcd.fontSize()
		ss = lcd.screensize()
		self.ax, self.ay = 0, ss[1] - fs[1] - 1
		self.color = lcd.RED
		self.dirty = True
		self.time = 0, 0, 0
	def update(self):
		now = rtc.now()
		if now[3:6] != self.time:
			self.time = now[3:6]
			self.setDirty()
	def render(self):
		lcd.font(lcd.FONT_7seg)
		lcd.attrib7seg(8, 2, True, self.color)
		lcd.text(self.ax, self.ay, "{:2d}:{:02d}:{:02d}".format(*self.time), self.color)
		self.resetDirty()
	def setDirty(self):
		self.dirty = True
		M5Led.on()
	def resetDirty(self):
		self.dirty = False
		M5Led.off()
	def isDirty(self):
		return self.dirty

# Setup

lcd.setRotation(1)
lcd.font(lcd.FONT_Default)

year = rtc.now()[0]
if year < 2001:
	wifi = connectToWifi("wifiname", "wifipass")
	if wifi.active():
		updateRTC()
		wifi.active(False)
	time.sleep(1)

lcd.clear()
lcd.print("Clock-C1", 0,0)
lcd.print("{}-{}-{}".format(*rtc.now()[0:3]), 0, lcd.fontSize()[1], lcd.ORANGE)

clock = Clock()
batt = BatteryDisplay()

# Loop

while True:
	clock.update()
	batt.update()

	if clock.isDirty():
		clock.render()
	batt.render()
	wait_ms(100)
