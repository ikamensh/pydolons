extends VBoxContainer


# Declare member variables here. Examples:
# var a = 2
# var b = "text"

# Called when the node enters the scene tree for the first time.
func _ready():
	self.rect_position.x = (get_viewport().size.x - self.rect_min_size.x)/2
	self.rect_position.y = (get_viewport().size.y  - self.rect_min_size.y)/2
	pass # Replace with function body.

# Called every frame. 'delta' is the elapsed time since the previous frame.
#func _process(delta):
#	pass


func _on_exit_but_pressed():
	get_tree().quit()

func _on_settings_but_pressed():
#	var next = preload("res://gui/settings_page.tscn")
#	get_tree().change_scene_to(next)
	pass # Replace with function body.


func _on_stop_but_pressed():
	pass # Replace with function body.
