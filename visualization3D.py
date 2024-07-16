import vtk

class CustomInteractorStyle(vtk.vtkInteractorStyleTrackballCamera):

    def __init__(self, renderer, actors):
        self.AddObserver("LeftButtonPressEvent", self.left_button_press_event)
        self.AddObserver("MouseMoveEvent", self.mouse_move_event)
        self.AddObserver("LeftButtonReleaseEvent", self.left_button_release_event)
        self.renderer = renderer
        self.actors = actors
        self.selected_actor = None
        self.last_picked_position = None
        self.picker = vtk.vtkPropPicker()
        self.AddObserver("KeyPressEvent", self.key_press_event)
        
    def key_press_event(self, obj, event):
        key = self.GetInteractor().GetKeySym()
        if key == "r" and self.selected_actor:
            save_stl(self.selected_actor.GetMapper().GetInput(), "selected_actor.stl")
            print("Saved selected actor as selected_actor.stl")
        super().OnKeyPress()

    def left_button_press_event(self, obj, event):
        click_pos = self.GetInteractor().GetEventPosition()
        self.picker.Pick(click_pos[0], click_pos[1], 0, self.renderer)
        self.selected_actor = self.picker.GetActor()
        if self.selected_actor:
            self.last_picked_position = self.picker.GetPickPosition()
        self.OnLeftButtonDown()

    def mouse_move_event(self, obj, event):
        if self.selected_actor:
            click_pos = self.GetInteractor().GetEventPosition()
            self.picker.Pick(click_pos[0], click_pos[1], 0, self.renderer)
            new_picked_position = self.picker.GetPickPosition()
            if self.last_picked_position:
                translation = [new_picked_position[i] - self.last_picked_position[i] for i in range(3)]
                self.selected_actor.AddPosition(translation)
                self.last_picked_position = new_picked_position
        self.OnMouseMove()

    def left_button_release_event(self, obj, event):
        self.selected_actor = None
        self.last_picked_position = None
        self.OnLeftButtonUp()

def load_stl(filename):
    reader = vtk.vtkSTLReader()
    reader.SetFileName(filename)
    reader.Update()

    mapper = vtk.vtkPolyDataMapper()
    mapper.SetInputConnection(reader.GetOutputPort())

    actor = vtk.vtkActor()
    actor.SetMapper(mapper)

    return actor

def main(stl_paths):
    renderer = vtk.vtkRenderer()
    render_window = vtk.vtkRenderWindow()
    render_window.AddRenderer(renderer)
    interactor = vtk.vtkRenderWindowInteractor()
    interactor.SetRenderWindow(render_window)

    actors = []
    for stl_path in stl_paths:
        actor = load_stl(stl_path)
        renderer.AddActor(actor)
        actors.append(actor)

    style = CustomInteractorStyle(renderer, actors)
    interactor.SetInteractorStyle(style)

    renderer.SetBackground(0.1, 0.2, 0.4)
    render_window.SetSize(800, 600)
    render_window.Render()
    interactor.Initialize()
    interactor.Start()

if __name__ == "__main__":
    file_path = r"C:\Users\prana\Documents\GitHub\InteriorLab\currentModel.stl"
    file_path2 = r"C:\Users\prana\Documents\GitHub\InteriorLab\test_stl_models\modelone.stl"
    stl_paths = [file_path, file_path2]  
    main(stl_paths)
