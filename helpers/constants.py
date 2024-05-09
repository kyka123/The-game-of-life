from models.cell_size import CellSize
from models.rule import Rule

# THEME
ALIVE_CELL_COLOR: tuple[float, float, float] = (254/255, 254/255, 254/255)
BOARD_BG_COLOR: tuple[float, float, float] = (40/255, 40/255, 39/255)
THEME_STYLE: str = "Dark"
PRIMARY_PALETTE: str = 'Green'

# TEXTS
APP_TITLE: str = 'Gra w życie'

# LISTS
cell_sizes = [
    CellSize(size=10, name="Mała"),
    CellSize(size=50, name="Średnia"),
    CellSize(size=100, name="Duża"),
]

# DEFAULTS
DEFAULT_CELL_SIZE = cell_sizes[0]
DEFAULT_RULE = Rule(left='23', right='3')
DEFAULT_SPEED_PER_SECOND: float = 5.0
DEFAULT_WINDOW_SIZE: tuple[int, int] = (1000, 800)

