extends Node2D

var direction:int = 0
var speed:int = 300
var player_half_width:int=20
func _ready():
	pass
	
func _process(delta):
	if Input.is_action_pressed("left"):
		direction = -1
	elif Input.is_action_pressed("right"):
		direction = 1
	else:
		direction = 0
	#var screen_width = get_viewport_rect().size.x	
	position.x=clamp(position.x+direction*speed*delta,player_half_width,220-player_half_width)
