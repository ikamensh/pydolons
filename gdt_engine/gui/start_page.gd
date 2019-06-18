extends Node2D
var demo_level = preload("res://src/ui/world/demo_level.tscn")
# Declare member variables here. Examples:
# var a = 2
# var b = "text"

# Called when the node enters the scene tree for the first time.
func _ready():
	pass # Replace with function body.

# Called every frame. 'delta' is the elapsed time since the previous frame.
#func _process(delta):
#	pass


func _on_settings_but_pressed():
	self.hide()
	$"/root/settings_page".show()
	pass # Replace with function body.


func _on_start_but_pressed():
	self.hide()
	get_tree().change_scene_to(self.demo_level)
	pass # Replace with function body.
