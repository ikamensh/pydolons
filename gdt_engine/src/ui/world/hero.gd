extends Sprite

# Declare member variables here. Examples:
# var a = 2
# var b = "text"

# Called when the node enters the scene tree for the first time.
func _ready():
	pass # Replace with function body.

# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(delta):
	if Input.is_action_just_pressed("ui_down"):
		self.position.y += 128
	if Input.is_action_just_pressed("ui_up"):
		self.position.y -= 128
	if Input.is_action_just_pressed("ui_left"):
		self.position.x -= 128
	if Input.is_action_just_pressed("ui_right"):
		self.position.x += 128
	pass
