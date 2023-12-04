# Import necessary libraries
import pygame
import OpenGL.GL as GL
import OpenGL.GLU as GLU
from rubik import Rubik  # Assuming the Rubik class is defined in a separate file named 'rubik.py'

def main():
    # Initialize Rubik's Cube with a scale factor of 2
    rubik = Rubik(2)

    # Define dictionary for rotating the entire cube based on arrow key inputs
    rotate_cube = {pygame.K_UP: (0, -1), pygame.K_DOWN: (0, 1), pygame.K_LEFT: (1, -1), pygame.K_RIGHT: (1, 1)}

    # Define dictionary for animating and rotating individual slices based on number key inputs
    rotate_slc = {
        pygame.K_1: (0, 0, 1), pygame.K_2: (0, 1, -1), pygame.K_3: (0, 2, 1),
        pygame.K_4: (1, 0, 1), pygame.K_5: (1, 1, 1), pygame.K_6: (1, 2, 1),
        pygame.K_7: (2, 0, 1), pygame.K_8: (2, 1, 1), pygame.K_9: (2, 2, 1)
    }

    # Initialize rotation angles and cube rotation flags
    ang_x, ang_y = 0, 0
    rot_cube = [0, 0]
    animate = False
    rotate_start = None
    rotating = False
    animate_ang = 0
    zoom_factor = 1.0
    animate_speed = 5
    rotate = (0, 0, 0)
    running = True

    # Main game loop
    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                # Check for arrow key input to rotate the entire cube
                if event.key in rotate_cube:
                    value = rotate_cube[event.key]
                    rot_cube[value[0]] = value[1]
                # Check for number key input to animate and rotate individual slices
                if not animate and event.key in rotate_slc:
                    animate = True
                    rotate = rotate_slc[event.key]
            if event.type == pygame.KEYUP:
                # Reset cube rotation when arrow key is released
                if event.key in rotate_cube:
                    rot_cube = [0, 0]
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    rotating = True
                    rotate_start = pygame.mouse.get_pos()
                elif event.button == 4:  # Scroll up
                    zoom_factor -= 0.1
                elif event.button == 5:  # Scroll down
                    zoom_factor += 0.1
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    rotating = False
            if event.type == pygame.MOUSEMOTION and rotating:
                # Calculate the rotation angles based on mouse movement
                rotate_delta = pygame.mouse.get_pos()[0] - rotate_start[0], pygame.mouse.get_pos()[1] - rotate_start[1]
                ang_x += rotate_delta[1] * 0.2  # Adjust the scaling factor as needed
                ang_y += rotate_delta[0] * 0.2
                rotate_start = pygame.mouse.get_pos()

        # Update rotation angles based on arrow key input
        ang_x += rot_cube[0] * 2
        ang_y += rot_cube[1] * 2

        # Set the OpenGL modelview matrix
        GL.glMatrixMode(GL.GL_MODELVIEW)
        GL.glLoadIdentity()
        GL.glTranslatef(0, 0, -40 * zoom_factor)
        GL.glRotatef(ang_y, 0, 1, 0)
        GL.glRotatef(ang_x, 1, 0, 0)

        # Clear the screen and set background color
        GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)
        GL.glClearColor(0, 0, 0, 1)

        # Perform animation if active
        if animate:
            if animate_ang >= 90:
                # Update cube slices after completing the animation
                for cube in rubik.cubes:
                    cube.update(*rotate)
                animate = False
                animate_ang = 0

        # Draw each cube in the Rubik's Cube
        for cube in rubik.cubes:
            cube.draw(cube.polygons, animate, animate_ang, *rotate)

        # Update animation angle if active
        if animate:
            animate_ang += animate_speed

        # Update the display
        pygame.display.flip()
        pygame.time.wait(10)

if __name__ == '__main__':
    # Initialize pygame and set up display
    pygame.init()
    display = (1080, 720)
    pygame.display.set_mode(display, pygame.DOUBLEBUF | pygame.OPENGL)
    pygame.display.set_caption("Directional arrows to rotate the cube, keys from 1 to 9 to rotate each faces")

    # Enable depth testing and set up the perspective projection matrix
    GL.glEnable(GL.GL_DEPTH_TEST)
    GL.glMatrixMode(GL.GL_PROJECTION)
    GLU.gluPerspective(45, (display[0] / display[1]), 1, 100.0)

    # Start the main game loop
    main()

    # Quit pygame when the game loop exits
    pygame.quit()
