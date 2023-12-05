import pygame
import OpenGL.GL as GL

# Create a dictionary of colors using the named colors from pygame
COLORS = {key: tuple(value[:3]) for key, value in pygame.color.THECOLORS.items()}

class Cube(object):
    # Define pairs of indices representing edges of the cube
    edges = ((0, 1), (0, 3), (0, 4), (2, 1), (2, 3), (2, 7), (6, 3), (6, 4), (6, 7), (5, 1), (5, 4), (5, 7))

    # Define ordered sets of indices forming polygons (quadrilaterals) of the cube
    polygons = ((0, 1, 2, 3), (3, 2, 7, 6), (6, 7, 5, 4), (4, 5, 1, 0), (1, 5, 7, 2), (4, 0, 3, 6))

    # Define coordinates of vertices representing the cube in 3D space
    vertices = (
        (1, -1, -1), (1, 1, -1), (-1, 1, -1), (-1, -1, -1),
        (1, -1, 1), (1, 1, 1), (-1, -1, 1), (-1, 1, 1)
    )
    # Define colors for each face of the cube
    colors = (COLORS["blue"], COLORS["red"], COLORS["green"], (1, 0.5, 0), COLORS["orange"], COLORS["white"])

    def __init__(self, ident: tuple, n: int, scale: int) -> None:
        # Initialize Cube object with position, size, and rotation parameters
        self.n = n
        self.scale = scale
        self.current = [*ident]
        self.rot = [[1 if i == j else 0 for i in range(3)] for j in range(3)]

    def is_affected(self, axis: int, slc: int):
        # Check if the cube is affected by a rotation on a specific axis and slice
        return self.current[axis] == slc

    def update(self, axis: int, slc: int, dr: int):
        # Update the cube's rotation based on the provided axis, slice, and direction
        if not self.is_affected(axis, slc):
            return

        i = (axis + 1) % 3
        j = (axis + 2) % 3
        for k in range(3):
            self.rot[k][i], self.rot[k][j] = -self.rot[k][j] * dr, self.rot[k][i] * dr

        self.current[i], self.current[j] = (
            self.current[j] if dr < 0 else self.n - 1 - self.current[j],
            self.current[i] if dr > 0 else self.n - 1 - self.current[i])

    def transform_matrix(self):
        # Compute the transformation matrix for the cube
        s_a = [[s * self.scale for s in a] for a in self.rot]
        s_t = [(p - (self.n - 1) / 2) * 2 * self.scale for p in self.current]
        return [*s_a[0], 0, *s_a[1], 0, *s_a[2], 0, *s_t, 1]

    def draw(self, surf, animate, angle, axis, slc, dr):
        # Draw the cube with OpenGL based on provided parameters
        GL.glPushMatrix()
        if animate and self.is_affected(axis, slc):
            GL.glRotatef(angle * dr, *[1 if i == axis else 0 for i in range(3)])
        GL.glMultMatrixf(self.transform_matrix())

        # Draw the faces of the cube
        GL.glBegin(GL.GL_QUADS)
        for i in range(len(surf)):
            GL.glColor3fv(Cube.colors[i])
            for j in surf[i]:
                GL.glVertex3fv(Cube.vertices[j])
        GL.glEnd()

        # Draw the edges of the cube
        GL.glEnable(GL.GL_LINE_SMOOTH)
        GL.glLineWidth(3)
        GL.glDisable(GL.GL_LINE_SMOOTH)

        GL.glBegin(GL.GL_LINES)
        GL.glColor3fv((0, 0, 0))
        for edge in Cube.edges:
            for vertex in edge:
                GL.glVertex3fv(Cube.vertices[vertex])
        GL.glEnd()
        GL.glPopMatrix()

class Rubik:
    def __init__(self, scale):
        # Initialize the Rubik's Cube with the specified scale
        self.n = 3
        cr = range(self.n)
        self.scale = scale
        self.cubes = self.init_cube(cr)

    def init_cube(self, cr):
        # Initialize the individual cubes within the Rubik's Cube
        cubes = []
        for z in cr:
            for y in cr:
                for x in cr:
                    cubes.append(Cube((x, y, z), self.n, self.scale))
        return cubes
