from pathlib import Path

def load_idf(path:str)->str:
    return Path(path).read_text(encoding="utf-8",errors="ignore")

def save_idf(path:str,content:str):
    Path(path).write_text(content,encoding="utf-8")

def replace_cooling_setpoint(idf_text:str,old_value:str,new_value:str)->str:
    return idf_text.replace(old_value,new_value)
