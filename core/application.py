from core.visualization_state import VisualizationState

class Application:

    def __init__(self, app_id, name, description, workspace_class = None):
        self.id = app_id
        self.name = name
        self.description = description


    def get_visualization_state(self):
        return VisualizationState()
