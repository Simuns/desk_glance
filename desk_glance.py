#!/usr/bin/python3
import json
import subprocess
import rumps

def query_yabai_spaces():
    # Use the yabai command to query window details
    try:
        output = subprocess.check_output(['/opt/homebrew/bin/yabai', '-m', 'query', '--windows'], text=True)
        windows = json.loads(output)
    except Exception as e:
        print(f"Error querying yabai: {e}")
        return []

    # We'll track which spaces have at least one window
    spaces_with_windows = set()

    for window in windows:
        if 'space' in window:
            spaces_with_windows.add(window['space'])

    return spaces_with_windows

class SpaceIndicatorApp(rumps.App):
    def __init__(self):
        super(SpaceIndicatorApp, self).__init__("", title="")
        self.update_title()

    @rumps.timer(10)  # Update every 10 seconds; adjust as needed
    def update_title(self, _=None):
        spaces_with_windows = query_yabai_spaces()

        # Use squares to represent spaces. Here we use a light shade square (□) for empty spaces,
        # and a darker shade square (■) for occupied spaces.
        # Note: The visibility and contrast of these symbols might vary based on the system theme and background.
        status_elements = [f'{i+1}■' if i+1 in spaces_with_windows else f'{i+1}□' for i in range(8)]
        status = ' '.join(status_elements)
        
        self.title = status

if __name__ == "__main__":
    SpaceIndicatorApp().run()
