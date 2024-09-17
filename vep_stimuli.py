from psychopy_visionscience.radial import RadialStim
from psychopy import visual, core, event

# Create a window
win = visual.Window([800, 600], monitor="testMonitor", units="deg", color=(0, 0, 0))

# Create radial gratings for left and right hemifields
grating_left  = RadialStim(win, tex='sqrXsqr', radialCycles=8, angularCycles=16, size=(10, 10), pos=(0, 0), visibleWedge=(0, 180), autoLog=False, ori=180)

grating_right = RadialStim(win, tex='sqrXsqr', radialCycles=8, angularCycles=16, size=(10, 10), pos=(0, 0), visibleWedge=(0, 180), autoLog=False)

# Fixation cross
#fixation      = visual.ShapeStim(win, vertices=((0, -0.2), (0, 0.2), (0,0), (-0.2,0), (0.2, 0)), lineWidth=3, closeShape=False, lineColor="white")

# Flicker properties
hz_left  = 6   # Left visual hemifield frequency
hz_right = 7.5 # Right visual hemifield frequency
fps      = 60  # Assumed frame rate of the display

# Calculate frames per cycle
frames_per_cycle_left  = fps // hz_left
frames_per_cycle_right = fps // hz_right

# Stimulus duration
stim_duration = 100  # seconds
clock         = core.Clock()

# Main loop for flickering stimulus
while clock.getTime() < stim_duration:
    # Left side: toggle contrast for flicker
    if int(clock.getTime() * fps) % frames_per_cycle_left == 0:
        grating_left.contrast *= -1  # Invert contrast for flickering
    
    # Right side: toggle contrast for flicker
    if int(clock.getTime() * fps) % frames_per_cycle_right == 0:
        grating_right.contrast *= -1  # Invert contrast for flickering

    # Draw stimuli
    grating_left.draw()
    grating_right.draw()
    #fixation.draw()

    # Flip window to show
    win.flip()

    # Exit condition
    if event.getKeys(['escape']):
        break

# Clean up
win.close()
core.quit()
