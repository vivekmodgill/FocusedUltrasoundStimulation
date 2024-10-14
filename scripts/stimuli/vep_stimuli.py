from psychopy_visionscience.radial import RadialStim
from psychopy import visual, core, event
from rusocsci import buttonbox 
 
# make a buttonbox
bb = buttonbox.Buttonbox()

# Create a full-screen window
win = visual.Window(fullscr=True, monitor="testMonitor", units="deg", color=(0, 0, 0))

# Create radial gratings for left and right hemifields
grating_left  = RadialStim(win, tex='sqrXsqr', radialCycles=8, angularCycles=16, size=(10, 10), pos=(0, 0), visibleWedge=(5, 175), autoLog=False, ori=180)
grating_right = RadialStim(win, tex='sqrXsqr', radialCycles=8, angularCycles=16, size=(10, 10), pos=(0, 0), visibleWedge=(5, 175), autoLog=False)

# Fixation cross
fixation = visual.ShapeStim(win, vertices=((0, -0.2), (0, 0.2), (0,0), (-0.2,0), (0.2, 0)), lineWidth=3, closeShape=False, lineColor="white")

# Flicker properties
hz_left  = 6    # Left visual hemifield frequency
hz_right = 7.5  # Right visual hemifield frequency
fps      = 120  # Assumed frame rate of the display

# Calculate frames per cycle
frames_per_cycle_left  = fps // hz_left
frames_per_cycle_right = fps // hz_right

# Timing parameters for the experiment
flicker_duration          = 15                                    # Flickering for 15 seconds
fixation_duration         = 5                                     # Fixation for 5 seconds
block_duration            = flicker_duration + fixation_duration  # One block = flicker + fixation (20 seconds)
run_duration              = 240                                   # 4 minutes per run = 240 seconds
num_runs                  = 4                                     # 4 runs in total (16 minutes)
initial_fixation_duration = 10                                    # Initial fixation for 10 seconds

# Display initial fixation point for 10 seconds
fixation_clock = core.Clock()
while fixation_clock.getTime() < initial_fixation_duration:
    fixation.draw()
    win.flip()

# Main loop for runs
for run in range(num_runs):
    print(f"Starting run {run + 1}/{num_runs}")
    
    run_clock = core.Clock()
    
    # Each run lasts 4 minutes
    while run_clock.getTime() < run_duration:
        # Send trigger for flickering start
        bb.sendMarker(val=100)
        # Flickering for 15 seconds
        flicker_clock = core.Clock()
        while flicker_clock.getTime() < flicker_duration:
            # Left side: toggle contrast for flicker
            if int(flicker_clock.getTime() * fps) % frames_per_cycle_left == 0:
                grating_left.contrast *= -1  # Invert contrast for flickering
            
            # Right side: toggle contrast for flicker
            if int(flicker_clock.getTime() * fps) % frames_per_cycle_right == 0:
                grating_right.contrast *= -1  # Invert contrast for flickering

            # Draw stimuli
            grating_left.draw()
            grating_right.draw()
            fixation.draw()

            # Flip window to show
            win.flip()

            # Exit condition
            if event.getKeys(['escape']):
                win.close()
                core.quit()

        # Send trigger for fixation start
        bb.sendMarker(val=200)
        # Fixation-only period for 5 seconds
        fixation_clock = core.Clock()
        while fixation_clock.getTime() < fixation_duration:
            # Draw fixation cross only (blank screen with fixation)
            fixation.draw()

            # Flip window to show
            win.flip()

            # Exit condition
            if event.getKeys(['escape']):
                win.close()
                core.quit()

print("Experiment completed")

# Clean up
win.close()
core.quit()
