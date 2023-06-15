import random

def generateRandomColors(count):
    colors = []
    for _ in range(count):
        # Generate a random color in hexadecimal format
        color = '#' + ''.join(random.choices('0123456789ABCDEF', k=6))
        colors.append(color)
    
    return colors
