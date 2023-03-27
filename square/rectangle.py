def rectangle(width: float, height: float) -> str:
    area = width * height
    perimeter = 2 * (width + height)
    if width == height:
        return "Square"
    else:
        return f"Rectangle with area {area:.2f} and perimeter {perimeter:.2f}"
    
