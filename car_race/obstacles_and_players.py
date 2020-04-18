import random
from blocks import Rectangle, Block

class ObstacleManager():
    def __init__(self, arena, max_obstacles, width, height, step_size, min_dist, max_dist):
        """
        Args:
            arena: An instance of Rectangle to represent the boundary of playground.
            max_obstaceles: Maximum number of obstacles that can be in the playground.(if None, no limit of max obstacles)
            step_size: Number of steps obstances move everytime step() is called
            min_dist/max_dist: Range of distance between any two obstacle in `y` direction
            width: width of obstacle
            height: height of obstacle
        """
        assert isinstance(arena, Rectangle), "Arena should be instance of Rectangle. Provided of type: {}".format(type(arena))
        
        self._arena = arena
        self._max_obstacles = max_obstacles
        self._step_size = step_size
        self._min_dist = min_dist
        self._max_dist = max_dist
        self._width = width
        self._height = height
        self._obstacles = []

    @property
    def obstacles(self):
        return self._obstacles

    def step(self):
        for obstacle in self._obstacles:
            obstacle.move_y(self._step_size)
        
        # If the last object move out of arena, remove it from list of obstacles
        if len(self._obstacles) > 0 and not self._obstacles[-1].inside(self._arena):
            self._obstacles = self._obstacles[:-1]

        # Add new obstacle if needed
        if self._should_add_new_obstacle():
            self._add_new_obstacle()

    def overlap_any_obstacle(self, block):
        for obstacle in self._obstacles:
            if obstacle.is_overlapping(block):
                return True
        return False

    def _should_add_new_obstacle(self):
        if self._max_obstacles is None or self._max_obstacles == -1 or \
           len(self._obstacles) < self._max_obstacles:
            if len(self._obstacles) == 0:
                # If no obstacle in arena, just add one
               return True
            if self._obstacles[0].top > self._min_dist:
                # We can add a new obstacle. If we deterministically add, then vertical distances will always be consistent/equal.
                # Let's add stocasticity and randomness.
                if random.randint(self._min_dist, self._max_dist) < self._obstacles[0].top:
                    return True
        return False

    def _add_new_obstacle(self):
        left = random.randint(0, self._arena.width - self._width)
        bottom = 1
        top = bottom - self._height
        right = left + self._width
        obstacle = Block.from_bbox_coordinate(left, top, right, bottom)
        self._obstacles.insert(0, obstacle)

    
class Player():
    def __init__(self, arena, width, height, step_size):
        bottom = arena.bottom
        top = arena.bottom - height
        left = arena.width // 2 - width //2
        right = left + width

        self._block = Block.from_bbox_coordinate(left, top, right, bottom, boundary=arena)
        self._step_size = step_size

    def step(self):
        self._block.move_x(self._step_size)
        
