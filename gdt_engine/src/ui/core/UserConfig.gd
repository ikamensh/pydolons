extends Object

var DEFAULT_CONFIG = ConfigFile.new()
var config:ConfigFile = ConfigFile.new()
var conf_path = "user://sttings.conf"

func _init():
	self.setUpDeafultConfig()

func readSetting():
	var err = self.config.load(self.conf_path)
	if err == OK:
		print("read user settings")
	else:
		print("create new user settings")
		self.config = self.DEFAULT_CONFIG
		err = self.config.save(self.conf_path)
		if err != OK:
			print("d'ont create new user settings")
		
func saveSetting():
	var err = self.config.save(self.conf_path)
	if err == OK:
		print("save settings")
	else:
		print("D'ont save settings")
	

func setUpDeafultConfig():
	self.DEFAULT_CONFIG.set_value("display", "window/size/width", 1280)
	self.DEFAULT_CONFIG.set_value("display", "window/size/height", 720)
	self.DEFAULT_CONFIG.set_value("display", "window/size/fullscreen", true)