import pygame
import pygame_widgets
from pygame_widgets.slider import Slider
from pygame_widgets.textbox import TextBox
from graph.graph import SpringMassGraph


def load_sliders(screen):
    """Load pygame_widgets sliders for UI."""
    gravity_slider = Slider(
        screen, 600, 50, 100, 10, min=0, max=0.2, step=0.005
    )
    gravity_slider.setValue(0.02)
    gravity_output = TextBox(
        screen, 720, 45, 40, 25, fontSize=20
    )

    friction_slider = Slider(
        screen, 600, 80, 100, 10, min=0, max=0.2, step=0.005
    )
    friction_slider.setValue(0.02)
    friction_output = TextBox(
        screen, 720, 75, 40, 25, fontSize=20
    )

    spring_slider = Slider(
        screen, 600, 110, 100, 10, min=0, max=0.2, step=0.005
    )
    spring_slider.setValue(0.02)
    spring_output = TextBox(
        screen, 720, 105, 40, 25, fontSize=20
    )

    return (
        friction_slider,
        friction_output,
        gravity_slider,
        gravity_output,
        spring_slider,
        spring_output,
    )


def load_slider_textboxes():
    """Load pygame textboxes for sliders."""
    comic_sans = pygame.font.SysFont('Comic Sans MS', 15)
    gravity_text = comic_sans.render('Gravity', False, (0, 0, 0))
    friction_text = comic_sans.render('Friction', False, (0, 0, 0))
    spring_text = comic_sans.render('Spring Tension', False, (0, 0, 0))
    return (gravity_text, friction_text, spring_text)


def update_sliders(graph: SpringMassGraph, gravity_slider, friction_slider, spring_slider,
                   gravity_output, friction_output, spring_output, ev):
    """Update sliders and change graph attributes."""
    # update slider and graph attributes
    gravity = gravity_slider.getValue()
    friction = friction_slider.getValue()
    spring = spring_slider.getValue()

    graph.gravity = gravity
    graph.friction = friction
    graph.spring_constant = spring

    gravity_output.setText(gravity_slider.getValue())
    pygame_widgets.update(ev)
    friction_output.setText(friction_slider.getValue())
    pygame_widgets.update(ev)
    spring_output.setText(spring_slider.getValue())
    pygame_widgets.update(ev)


def draw_slider_text(screen, gravity_text, friction_text, spring_text):
    """Draw text for slider descriptions."""
    screen.blit(gravity_text, (540, 45))
    screen.blit(friction_text, (535, 75))
    screen.blit(spring_text, (490, 105))
