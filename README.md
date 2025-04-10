# Overview

A tkinter frontend hijacking Pysh's interpreter run calls

# How to use

Setup a virtual environment with `python -m venv --prompt interpysh venv`. Then, `source venv/bin/activate`. 
Next, `pip install -r requirements.txt`. Finally, `pip install -e .`

To run the tkinter frontend, type `interpysh` into your terminal.

Pysh has json files containing programs to be run for testing. Check the `examples` folder or the link below for examples.

https://github.com/RowanTL/pyshgp/tree/tkinter/tests/resources/programs

Point tkinter towards a json push program with the `push code path` button.
Next, load the program with the `load push code` button.

Usage is very similar to interpush.

Inspired by: https://lspector.github.io/interpush/

# Notes

**THERE IS NO SUPPORT FOR INPUTS. LITERALS AND INSTRUCTIONS ONLY**

If you load code into interpysh and it doesn't update, check the console. There may be an error when loading json.

The stacks are pretty printed to the terminal if needed.

There's a bug in code_extract in pysh. If the index is 0, code_extract returns the entire CodeBlock rather than the 0th index of the CodeBlock.
Furthermore, code_extract is unable to return the final element of any CodeBlock.
