class Color:

    def __init__(self, red: int, green: int, blue: int):
        self.red = red
        self.green = green
        self.blue = blue

    def __str__(self):
        return str(self.red) + "," + str(self.green) + "," + str(self.blue)

    @staticmethod
    def from_html_string(string: str):
        colors = tuple(int(string.lstrip('#')[i:i + 2], 16) for i in (0, 2, 4))
        return Color(colors[0], colors[1], colors[2])


BLACK = Color.from_html_string("#000000")
WHITE = Color.from_html_string("#ffffff")

RED = Color.from_html_string("#ff0000")
GREEN = Color.from_html_string("#00ff00")
BLUE = Color.from_html_string("#0000ff")

CYAN = Color.from_html_string("#00ffff")
MAGENTA = Color.from_html_string("#ff00ff")
YELLOW = Color.from_html_string("#ffff00")
