"""Execute code cells in-process and save real outputs, without kernel sockets.

Usage (from repository root): python scripts/execute_notebook.py
Standard Jupyter execution is also supported; this runner is useful in environments
where spawning a socket-based kernel is unavailable. It runs trusted project code.
"""
import os
from pathlib import Path
import nbformat
from IPython.core.interactiveshell import InteractiveShell
from IPython.utils.capture import capture_output

ROOT=Path(__file__).resolve().parents[1]

def main():
    os.chdir(ROOT)
    path=ROOT/'notebooks/01_quality_analysis.ipynb'
    notebook=nbformat.read(path,as_version=4)
    shell=InteractiveShell.instance()
    count=0
    for cell in notebook.cells:
        if cell.cell_type!='code': continue
        count+=1
        with capture_output(stdout=True,stderr=True,display=True) as captured:
            result=shell.run_cell(cell.source,store_history=True)
        if result.error_before_exec or result.error_in_exec:
            raise RuntimeError(f'Notebook cell {count} failed: {result.error_before_exec or result.error_in_exec}')
        cell.execution_count=count
        cell.outputs=[]
        if captured.stdout:cell.outputs.append(nbformat.v4.new_output('stream',name='stdout',text=captured.stdout))
        if captured.stderr:cell.outputs.append(nbformat.v4.new_output('stream',name='stderr',text=captured.stderr))
        for output in captured.outputs:
            cell.outputs.append(nbformat.v4.new_output('display_data',data=output.data,metadata=output.metadata))
    nbformat.validate(notebook)
    nbformat.write(notebook,path)
    print(f'Executed {count} code cells successfully: {path.name}')

if __name__=='__main__':main()
