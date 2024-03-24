import json
import subprocess
import rumps
import os

class Yabai:
    def __init__(self):
        self.yabai_path = self.find_app_in_common_locations("yabai")
        if not self.yabai_path:
            raise Exception("yabai not found in common locations")
    
    def find_app_in_common_locations(self, app_name):
        common_paths = ["/usr/local/bin/", "/usr/bin/", "/bin/", "/opt/local/bin/", "/opt/homebrew/bin"]
        for path in common_paths:
            full_path = os.path.join(path, app_name)
            if os.path.exists(full_path):
                return full_path
        return None

    def query_spaces_or_windows(self, query_type='--spaces'):
        try:
            output = subprocess.check_output([self.yabai_path, '-m', 'query', query_type], text=True)
            return json.loads(output)
        except Exception as e:
            print(f"Error querying yabai: {e}")
            return []

import rumps

class SpaceIndicatorApp(rumps.App):
    def __init__(self, yabai_instance):
        super(SpaceIndicatorApp, self).__init__("", title="")
        self.yabai = yabai_instance  # Assuming yabai_instance is an instance of a class that has the query_spaces_or_windows method
        self.update_title()

    @rumps.timer(5)
    def update_title(self, _=None):
        # Query windows and spaces
        windows = self.yabai.query_spaces_or_windows('--windows')
        spaces_with_windows = set(window['space'] for window in windows if 'space' in window)
        
        spaces = self.yabai.query_spaces_or_windows('--spaces')
        focused_space = next((space['index'] for space in spaces if space.get('has-focus', False)), None)
        
        # Construct status elements, including focus indication
        status_elements = []
        for i in range(len(spaces)):  # Assuming you want a square for each space returned by yabai
            if (i + 1) == focused_space:
                element = f'{i+1}🟩'  # Green square (assuming 🟩) for focused
            elif (i + 1) in spaces_with_windows:
                element = f'{i+1}■'  # Filled square for occupied
            else:
                element = f'{i+1}□'  # Empty square for unoccupied
            status_elements.append(element)

        self.title = ' '.join(status_elements)

if __name__ == "__main__":
    try:
        yabai_instance = Yabai()  # Ensure Yabai is correctly referenced (e.g., yabai or Yabai)
        SpaceIndicatorApp(yabai_instance).run()
    except Exception as e:
        print(f"Failed to start SpaceIndicatorApp: {e}")
