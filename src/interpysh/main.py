import typer
import tkinter as tk
import tkinter.ttk as ttk
import tkinter.filedialog as filedialog
import json

from pyshgp.push.interpreter import InspectInterpreter
from pyshgp.push.state import PushState
from pyshgp.push.utils import get_program, _deserialize_atoms, all_instruction_set
from pyshgp.push.config import PushConfig
from pyshgp.push.instruction_set import InstructionSet
from pyshgp.push.program import ProgramSignature, Program
from pyshgp.push.atoms import CodeBlock, Closer, Literal, InstructionMeta, Input


app = typer.Typer()

@app.command()
def run():
    states: list[PushState] | None = None
    state_index: int = 0

    root: tk.Tk = tk.Tk()
    root.title("InterPysh")

    file_path_str: tk.StringVar = tk.StringVar()
    file_path_str.set("No Path Selected")
    file_path_label: tk.Label = tk.Label(
        master=root,
        textvariable=file_path_str,
    )

    # Path to push code json
    def push_code_path():
        path = filedialog.askopenfile()
        if path is None:
            file_path_str.set("FAILED TO FIND PATH")
        else:
            file_path_str.set(path.name)

    file_path_button: ttk.Button = ttk.Button(
        master=root,
        text="push code path",
        command=push_code_path
    )

    # Load push code to stacks
    def load_push_code():
        nonlocal state_index
        nonlocal states
        if file_path_str.get() == "No Path Selected" or file_path_str.get() == "FAILED TO FIND PATH":
            return
        
        with open(file_path_str.get()) as f:
            atoms = _deserialize_atoms(json.load(f), all_instruction_set)
        code_block = CodeBlock(atoms)
        program = Program(code=code_block, signature=ProgramSignature(arity=1, output_stacks=[]))
        states = InspectInterpreter().run(program, [])
        state_index = 0

        update_labels(states[state_index])

    load_push_code_button: ttk.Button = ttk.Button(
        master=root,
        text="load push code",
        command=load_push_code
    )

    # interpret one step
    def interpret_one_step():
        nonlocal state_index
        nonlocal states
        if state_index + 1 > len(states) - 1:
            return
        state_index += 1
        update_labels(states[state_index])

    interpret_one_step_button: ttk.Button = ttk.Button(
        master=root,
        text="interpret one step",
        command=interpret_one_step
    )

    # previous step
    def previous_step():
        nonlocal state_index
        nonlocal states
        if state_index - 1 < 0:
            return
        state_index -= 1
        update_labels(states[state_index])

    previous_step_button: ttk.Button = ttk.Button(
        master=root,
        text="previous step",
        command=previous_step
    )

    # interpret all
    def interpret_all():
        nonlocal state_index
        nonlocal states
        state_index = len(states) - 1
        update_labels(states[state_index])

    interpret_all_button: ttk.Button = ttk.Button(
        master=root,
        text="interpret all",
        command=interpret_all
    )

    # labels
    def update_labels(state: PushState):
        exec_str.set("exec: " + str(state["exec"]))
        code_str.set("code: " + str(state['code']))
        int_str.set("int: " + str(state["int"]))
        float_str.set("float: " + str(state["float"]))
        str_str.set("str: " + str(state["str"]))
        bool_str.set("bool: " + str(state["bool"]))
        char_str.set("char: " + str(state["char"]))
        vector_int_str.set("vector_int: " + str(state["vector_int"]))
        vector_float_str.set("vector_float: " + str(state["vector_float"]))
        vector_str_str.set("vector_str: " + str(state["vector_str"]))
        vector_char_str.set("vector_char: " + str(state["vector_char"]))
        vector_bool_str.set("vector_bool: " + str(state["vector_bool"]))
        state.pretty_print()
        print("-----------------------------------------------------")

    exec_str: tk.StringVar = tk.StringVar()
    exec_label: tk.Label = tk.Label(
        master=root,
        textvariable=exec_str,
    )

    code_str: tk.StringVar = tk.StringVar()
    code_label: tk.Label = tk.Label(
        master=root,
        textvariable=code_str,
    )

    int_str: tk.StringVar = tk.StringVar()
    int_label: tk.Label = tk.Label(
        master=root,
        textvariable=int_str,
    )

    float_str: tk.StringVar = tk.StringVar()
    float_label: tk.Label = tk.Label(
        master=root,
        textvariable=float_str,
    )

    str_str: tk.StringVar = tk.StringVar()
    str_label: tk.Label = tk.Label(
        master=root,
        textvariable=str_str,
    )

    char_str: tk.StringVar = tk.StringVar()
    char_label: tk.Label = tk.Label(
        master=root,
        textvariable=char_str,
    )

    bool_str: tk.StringVar = tk.StringVar()
    bool_label: tk.Label = tk.Label(
        master=root,
        textvariable=bool_str
    )

    vector_int_str: tk.StringVar = tk.StringVar()
    vector_int_label: tk.Label = tk.Label(
        master=root,
        textvariable=vector_int_str,
    )

    vector_float_str: tk.StringVar = tk.StringVar()
    vector_float_label: tk.Label = tk.Label(
        master=root,
        textvariable=vector_float_str,
    )

    vector_str_str: tk.StringVar = tk.StringVar()
    vector_str_label: tk.Label = tk.Label(
        master=root,
        textvariable=vector_str_str,
    )

    vector_char_str: tk.StringVar = tk.StringVar()
    vector_char_label: tk.Label = tk.Label(
        master=root,
        textvariable=vector_int_str,
    )

    vector_bool_str: tk.StringVar = tk.StringVar()
    vector_bool_label: tk.Label = tk.Label(
        master=root,
        textvariable=vector_bool_str
    )

    # Place everything on the grid    
    file_path_label.grid(row = 0, sticky=tk.W)
    file_path_button.grid(row = 1, sticky=tk.W)
    load_push_code_button.grid(row = 2, sticky=tk.W)
    interpret_one_step_button.grid(row = 3, sticky=tk.W)
    previous_step_button.grid(row = 4, sticky=tk.W)
    interpret_all_button.grid(row = 5, sticky=tk.W)
    exec_label.grid(row = 6, sticky=tk.W)
    code_label.grid(row = 7, sticky=tk.W)
    int_label.grid(row = 8, sticky=tk.W)
    float_label.grid(row = 9, sticky=tk.W)
    str_label.grid(row = 10, sticky=tk.W)
    char_label.grid(row = 11, sticky=tk.W)
    bool_label.grid(row = 12,sticky=tk.W)
    vector_int_label.grid(row = 13, sticky=tk.W)
    vector_float_label.grid(row = 14, sticky=tk.W)
    vector_str_label.grid(row = 15, sticky=tk.W)
    vector_char_label.grid(row = 16, sticky=tk.W)
    vector_bool_label.grid(row = 17, sticky=tk.W)

    # run the gui
    root.mainloop()

if __name__ == "__main__":
    run()
