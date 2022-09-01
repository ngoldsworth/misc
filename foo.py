primary_colors = [
    'red',
    'yellow',
    'blue'
]

secondary_colors = [
    'green',
    'orange',
    'violet'
]

user_color = input("Please enter a color: ")

# sanitize input
user_color = user_color.lower()

if user_color in primary_colors:
    color_type = 'primary' 
elif user_color in secondary_colors:
    color_type = 'seconday'
else:
    color_type = 'not a primary or secondary'

print( f'{user_color} is a {color_type} color')