from openai import OpenAI
from gui import GUI
from scadInit import ScadInitializer
from visualization3D import CustomInteractorStyle
from visualization3D import main as vis_main
from accessPrevPrompts import PromptMemory
from SCADtoSTL import SCADtoSTL

client = OpenAI()

def generate_3d_model(user_message):
    memory = PromptMemory()
    completion = client.chat.completions.create(
        model="gpt-4-turbo",
        messages=[
            {"role": "system", "content": """
            You are GPT-4-Turbo, a highly advanced 3D modeling assistant. 
            Your primary function is to generate 3D models of furniture using the OpenSCAD language. 
            Please follow OpenSCAD documentation properly. 
            Your responses must be as accurate as possible, ensuring that all components attach correctly, look proper, follow proper OpenSCAD syntax, and are of average size. 
            You provide detailed and precise OpenSCAD code to create realistic and functional furniture models.
            Please limit measurements & parameters to 30 units per parameter MAXIMUM. That's length, width, and height.
            Only prompts about generating FURNITURE must be accepted. If user prompts about generating anything other than furniture, respond with "ERROR! No furniture generation command detected." 
            
            """
            +
            "Grant users the ability to fix certain aspects of the code you output. If the user refers to anything you did wrong, you will fix it in OpenSCAD. Refer to their most recent prompt in " + memory.read_prompts() + " and your most recent response in " + memory.read_responses() + "."
            """
             MOST IMPORTANTLY: Only send OpenSCAD code, no conversational speak here. Don't use notes like '''OpenSCAD '''. Anything like that. Just pure code and minor notes to clarify what sections mean.
            """},
            {"role": "user", "content": user_message}
        ]
    )
    
    response = completion.choices[0].message.content
    memory.update_prompts(user_message)
    memory.update_responses(response)
    
    print(response)

    # SCAD init
    scad_init = ScadInitializer()
    scad_init.update_counter()

    # Create new SCAD file
    counter = scad_init.read_counter()
    new_scad_file = f"C:/Users/prana/Documents/GitHub/InteriorLab/generated_models/currentModel{counter}.scad"
    with open(new_scad_file, 'w') as file:
        file.truncate(0)
        file.write(response)
    
    # SCAD to STL conversion
    scad_file = f"C:/Users/prana/Documents/GitHub/InteriorLab/generated_models/currentModel{counter}.scad"
    stl_file = f"C:/Users/prana/Documents/GitHub/InteriorLab/generated_models/currentModel{counter}.stl"
    openscad_path = "C://Program Files//OpenSCAD//openscad.exe"

    scad_converter = SCADtoSTL()
    scad_converter.scad_to_stl(scad_file, stl_file, openscad_path)

    # 3D visualization
    visualizer = CustomInteractorStyle(renderer="", actors="")
    stl_paths = [stl_file]
    vis_main(stl_paths)

    

def interiorLab():
    gui = GUI(generate_3d_model)
    gui.run()

interiorLab()
