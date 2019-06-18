extends Node2D

var RESOLUTIONS = [Vector2(1280, 720),
                   Vector2(1360, 768),
                   Vector2(1366, 768),
                   Vector2(1440, 900),
                   Vector2(1536, 864),
                   Vector2(1600, 900),
                   Vector2(1680, 1050),
                   Vector2(1920, 1200),
                   Vector2(1920, 1080),
                   Vector2(2560, 1080),
                   Vector2(2560, 1440),
                   Vector2(3440, 1440),
                   Vector2(3840, 2160)]

func _ready():
	self.hide()
	$but_container.rect_position.x = (get_viewport().size.x - $but_container.rect_min_size.x)/2
	$but_container.rect_position.y = (get_viewport().size.y  - $but_container.rect_min_size.y)/2
	if $"/root/TheUI".user_cfg.config.get_value("display", "window/size/fullscreen"):
		$but_container/full_scr_but.pressed = true
	for v in self.RESOLUTIONS:
		$but_container/ItemList.add_item(str(v))
	pass # Replace with function body.


func _on_back_but_pressed():
	self.hide()
	$"/root/start_page".show()
	pass # Replace with function body.


func _on_ItemList_item_selected(index):
	$"/root/TheUI".set_user_size(self.RESOLUTIONS[index])


func _on_full_scr_but_toggled(button_pressed):
	$"/root/TheUI".user_cfg.config.set_value("display", "window/size/fullscreen", button_pressed)


func _on_save_but_pressed():
	$"/root/TheUI".user_cfg.saveSetting()	
