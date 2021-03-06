import pigpio
import time

PWM_serwo = 16
PWM_frequency = 500

position_1 = 470
position_2 = 650
neutral = 340
range = 1000


class Dropper:
	def __init__(self,logger):
		self._logger = logger
		self.position = 0

		self.pi = pigpio.pi()

		print("setup")
		self.setup()
		self.close()

	def setup(self):
		self.pi.set_PWM_frequency(PWM_serwo, PWM_frequency)
		self.pi.set_PWM_range(PWM_serwo, range)
		self.pi.set_PWM_dutycycle(PWM_serwo, neutral)

	def set_position(self, pos):
		self.pi.set_PWM_dutycycle(PWM_serwo, pos)

	def open(self):
		self.set_position(600)

	def close(self):
		self.set_position(neutral)

	def drop(self):
		self.log("drop marker")
		if self.position == 0:
			self.set_position(position_1)
			self.log("first marker")
		else:
			self.log("drop second marker")
			self.set_position(position_2)
			self.open()
			time.sleep(1)
			#self.close()
			self.pi.stop()

		self.position+=1

	def log(self, msg):
		if self._logger:
			self._logger.log(msg)

	


if __name__ == "__main__":
	#if not self.pi.connected:
	#	exit()
	dropper = Dropper(None)
	dropper.drop()
	time.sleep(4)

	dropper.drop()

	#time.sleep(1)

	#print("pos 1")
	#dropper.set_position(position_1)

	#time.sleep(1)

	#print("pos2")
	#dropper.set_position(position_2)

	#time.sleep(1)
	#print("stop")
	#dropper.set_position(600)

	#time.sleep(1)
	#dropper.open()
	#time.sleep(1)
	#dropper.close()

	#dropper.pi.stop()

