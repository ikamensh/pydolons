extends Node
const UserConfig = preload("res://src/ui/core/UserConfig.gd")

var user_cfg = UserConfig.new()
var user_size = Vector2()


func _ready():
	self.user_cfg.readSetting()
	if not self.user_cfg.config.get_value("display", "window/size/fullscreen"):
		self.user_size.x = self.user_cfg.config.get_value("display", "window/size/width")
		self.user_size.y = self.user_cfg.config.get_value("display", "window/size/height")
		OS.window_fullscreen = false
		OS.set_window_size(self.user_size)
	else:
		OS.window_fullscreen = true

func set_user_size(size:Vector2):
	self.user_size.x = size.x
	self.user_size.y = size.y
	self.user_cfg.config.set_value("display", "window/size/width", size.x)
	self.user_cfg.config.set_value("display", "window/size/height", size.y)
	
