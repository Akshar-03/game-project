extends Node2D

var bullet_scene = preload("res://entites/bullet/bullet.tscn")
var speed:int = 300
var player_half_width=10
var shoot_time := 1.0
var shoot_counter := 0.0

func _ready():
	pass
func _process(delta):
	shoot_counter+=delta
	if Input.is_action_pressed("shoot")and shoot_counter>shoot_time:
		shoot_counter=0
		var bullet_instance=bullet_scene.instantiate()
		bullet_instance.position.y=position.y-10
		bullet_instance.position.x=position.x
		get_parent().get_node("bullets").add_child(bullet_instance)
		
	var direction = Input.get_action_strength("ui_right") - Input.get_action_strength("ui_left")
	position.x = clamp(
		position.x + direction * speed * delta,
		player_half_width,
		400 - player_half_width
	)
