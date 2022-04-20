import colors
import random
import numpy as np
import copy

cube_colors = []

num_points = 4 * 6 * 27
num_cubes = 27

animation = False
moving = []


def generate():
	global cube_colors
	points = []
	n = 0
	for i in range(3):
		for j in range(3): 	
			for k in range(3):
				x = i*0.2 - 0.3 	
				y = j*0.2 - 0.3 	
				z = k*0.2 - 0.3
				cube_colors.append(get_cube_colors(i,j,k))
				n += 1
				points += create_mini_cube(x,y,z)
	return np.array(points)

def cube(x,y,z):
	return 9*x + 3*y + z

top = 0
bottom = 1
front = 2
back = 3
left = 4
right = 5

def create_mini_cube(x,y,z):
	points = []

	#Top
	points.append((x    , y, z    ))
	points.append((x+0.2, y, z    ))
	points.append((x    , y, z+0.2))
	points.append((x+0.2, y, z+0.2))

	#Bottom
	points.append((x    , y+0.2, z    ))
	points.append((x+0.2, y+0.2, z    ))
	points.append((x    , y+0.2, z+0.2))
	points.append((x+0.2, y+0.2, z+0.2))

	#Front
	points.append((x    , y    , z))
	points.append((x+0.2, y    , z))
	points.append((x    , y+0.2, z))
	points.append((x+0.2, y+0.2, z))

	#Back
	points.append((x    , y    , z+0.2))
	points.append((x+0.2, y    , z+0.2))
	points.append((x    , y+0.2, z+0.2))
	points.append((x+0.2, y+0.2, z+0.2))
	
	#Left
	points.append((x,y    , z    ))
	points.append((x,y+0.2, z    ))
	points.append((x,y    , z+0.2))
	points.append((x,y+0.2, z+0.2))

	#Right
	points.append((x+0.2,y    , z    ))
	points.append((x+0.2,y+0.2, z    ))
	points.append((x+0.2,y    , z+0.2))
	points.append((x+0.2,y+0.2, z+0.2))

	return points

def move_colors_white():
	global cube_colors
	new_colors = copy.deepcopy(cube_colors)
	new_colors[cube(0,0,0)][left] = cube_colors[cube(0,0,2)][left]
	new_colors[cube(0,0,0)][top] = cube_colors[cube(0,0,2)][back]
	new_colors[cube(0,0,0)][front] = cube_colors[cube(0,0,2)][top]

	new_colors[cube(0,0,1)][left] = cube_colors[cube(0,1,2)][left]
	new_colors[cube(0,0,1)][top] = cube_colors[cube(0,1,2)][back]

	new_colors[cube(0,0,2)][left] = cube_colors[cube(0,2,2)][left]
	new_colors[cube(0,0,2)][back] = cube_colors[cube(0,2,2)][bottom]
	new_colors[cube(0,0,2)][top] = cube_colors[cube(0,2,2)][back]

	new_colors[cube(0,1,2)][left] = cube_colors[cube(0,2,1)][left]
	new_colors[cube(0,1,2)][back] = cube_colors[cube(0,2,1)][bottom]

	new_colors[cube(0,2,2)][left] = cube_colors[cube(0,2,0)][left]
	new_colors[cube(0,2,2)][bottom] = cube_colors[cube(0,2,0)][front]
	new_colors[cube(0,2,2)][back] = cube_colors[cube(0,2,0)][bottom]

	new_colors[cube(0,2,1)][left] = cube_colors[cube(0,1,0)][left]
	new_colors[cube(0,2,1)][bottom] = cube_colors[cube(0,1,0)][front]

	new_colors[cube(0,2,0)][left] = cube_colors[cube(0,0,0)][left]
	new_colors[cube(0,2,0)][front] = cube_colors[cube(0,0,0)][top]
	new_colors[cube(0,2,0)][bottom] = cube_colors[cube(0,0,0)][front]

	new_colors[cube(0,1,0)][left] = cube_colors[cube(0,0,1)][left]
	new_colors[cube(0,1,0)][front] = cube_colors[cube(0,0,1)][top]

	cube_colors = new_colors

def move_white():
	global animation
	global moving
	animation = True
	moving = []
	for y in range(3):
		for z in range(3):
			moving.append(cube(0,y,z))
	return move_colors_white	

	
	

def get_cube_colors(x,y,z):
	top    = colors.blue   if y == 0 else colors.black
	bottom = colors.orange if y == 2 else colors.black
	front  = colors.red    if z == 0 else colors.black
	back   = colors.green  if z == 2 else colors.black
	left   = colors.white  if x == 0 else colors.black
	right  = colors.yellow if x == 2 else colors.black
	return [top,bottom,front,back,left,right]

	
