
class Rectangle:
    """Class to represent a rectangle, with center coordinates and width/height"""

    def __init__(self, xc, yc, w, h):
        assert w > 0, "Width of rectangle should be > 0. Provided: {}".format(w)
        assert h > 0, "Height of rectangle should be > 0. Provided: {}".format(h)
        self._xc = xc
        self._yc = yc
        self._w = w
        self._h = h

    @staticmethod
    def from_width_height(width, height):
        return Rectangle.from_bbox_coordinate(0, 0, width, height)

    @staticmethod
    def from_bbox_coordinate(tlx, tly, brx, bry):
        assert brx > tlx, "brx({}) should be > tlx({})" .format(brx, tlx)
        assert bry > tly, "bry({}) should be > tly({})" .format(bry, tly)
        xc = (tlx + brx) / 2
        yc = (tly + bry) / 2
        w = brx - tlx
        h = bry - tly
        return Rectangle(xc, yc, w, h)

    @property
    def width(self):
        return self._w

    @property
    def height(self):
        return self._h
    
    @property
    def center_x(self):
        return self._xc
    
    @property
    def center_y(self):
        return self._yc
    
    @property
    def top(self):
        return self._yc - self._h/2

    @property
    def bottom(self):
        return self._yc + self._h/2

    @property
    def left(self):
        return self._xc - self._w/2

    @property
    def right(self):
        return self._xc + self._w/2
        
    @property
    def bbox(self):
        return {"tlx": self.left, "tly": self.top, "brx": self.right, "bry": self.bottom}

    def move_x(self, delta_x):
        """ Move itself in x direction """
        self._xc = self._xc + delta_x
        return self
    
    def move_y(self, delta_y):
        """ Move itself in y direction """
        self._yc = self._yc + delta_y
        return self

    def new_moved_rectangle(self, delta_x=0, delta_y=0):
        """ Returns a new rectangle moved by (delta_x, delta_y). Does not move itself"""
        return Rectangle(self._xc + delta_x, self._yc + delta_y, self._w, self._h)

    def is_overlapping(self, other):
        """ Returns boolean (True/False) whether two rectangles overlap """
        assert isinstance(other, Rectangle), "Other should be an instance of Rectangle"
        dist_center_x = abs(self._xc - other._xc)
        dist_center_y = abs(self._yc - other._yc)
        if dist_center_x > self._w + other._w:
            return False
        if dist_center_y > self._h + other._h:
            return False
        return True

    def contains(self, other):
        """Return True/False whether this rectangle contains another rectangle. boundary overlap is allowed """
        assert isinstance(other, Rectangle), "Other should be an instance of Rectangle"
        self_bbox = self.bbox
        other_bbox = other.bbox
        if (self_bbox["tlx"] <= other_bbox["tlx"] and self_bbox["brx"] >= other_bbox["brx"] and
           self_bbox["tly"] <= other_bbox["tly"] and self_bbox["bry"] >= other_bbox["bry"]):
           return True
        return False

    def inside(self, other):
        """Returns True/False whether this rectangle is inside another rectangle """
        assert isinstance(other, Rectangle), "Other should be an instance of Rectangle"
        return other.contains(self)

    def __str__(self):
        bbox = self.bbox
        return "Rectangle:  TopLeft: ({tlx}, {tly})      BottomRight: ({brx}, {bry})".format(
                tlx=bbox["tlx"], tly=bbox["tly"], brx=bbox["brx"], bry=bbox["bry"])


class Block(Rectangle):
    """ Is a type of rectangle with notion of a boundary. Block can be moved just like a rectangle in x-y direction.
        If the rectangle has a boundary, block cannot be moved out of boundary. So if a block reaches a boundary, it 
        cannot move any further outside of boundary.

        Also stores meta(dict) to store any information related to block
    """
    def __init__(self, xc, yc, h, w, meta=None, boundary=None):
        assert isinstance(boundary, (type(None), Rectangle)),\
            "boundary should be: (None, Rectangle). Provided: {}".format(type(boundary))
        super().__init__(xc, yc, h, w)
        self._meta = meta
        self._boundary = boundary

    @staticmethod
    def from_width_height(width, height, meta=None, boundary=None):
        return Block.from_bbox_coordinate(0, 0, width, height, meta, boundary)

    @staticmethod
    def from_bbox_coordinate(tlx, tly, brx, bry, meta=None, boundary=None):
        assert brx > tlx, "brx({}) should be > tlx({})" .format(brx, tlx)
        assert bry > tly, "bry({}) should be > tly({})" .format(bry, tly)
        xc = (tlx + brx) / 2
        yc = (tly + bry) / 2
        w = brx - tlx
        h = bry - tly
        return Block(xc, yc, w, h, meta, boundary)

    def move_x(self, delta_x):
        if self._boundary is None:
            self._move_x(delta_x)
        else:
            new_rectangle = self.new_moved_rectangle(delta_x, 0)
            if new_rectangle.inside(boundary):
                self._move_x(delta_x)

    def move_y(self, delta_y):
        if self._boundary is None:
            self._move_y(delta_y)
        else:
            new_rectangle = self.new_moved_rectangle(delta_y, 0)
            if new_rectangle.inside(boundary):
                self._move_y(delta_y)
        return self

    def _move_x(self, delta_x):
        super().move_x(delta_x)

    def _move_y(self, delta_y):
        super().move_y(delta_y)

    def __str__(self):
        return super().__str__()


if __name__ == "__main__":
    boundary = Rectangle.from_width_height(10, 30)
    block_no_boundary = Block.from_width_height(5, 7, boundary=None)
    block_boundary = Block.from_width_height(5, 7, boundary=boundary)

    print("boundary: {}".format(boundary))
    for i in range(20):
        block_no_boundary.move_x(1)
        block_boundary.move_x(1)
        print("Noboundary: {}".format(str(block_no_boundary.center_x)))
        print("boundaryboundary: {}".format(str(block_boundary.center_x)))
        print("\n\n")
    
    # print(r)
    