from pathlib import Path
import subprocess
import os

def run_energyplus(energyplus_exe:str,idf_file:str,weather_file:str,output_dir:str):
    Path(output_dir).mkdir(parents=True,exist_ok=True)
    cmd=[
        energyplus_exe,
        "-w",weather_file,
        "-d",output_dir,
        idf_file
    ]
    print("Running:", " ".join(cmd))
    result=subprocess.run(cmd,capture_output=True,text=True)
    return {
        "returncode":result.returncode,
        "stdout":result.stdout,
        "stderr":result.stderr
    }

if __name__=="__main__":
    print("Import this module from main.py after configuring paths.")
