from fastapi import FastAPI
from pydantic import BaseModel
import subprocess

app = FastAPI()

class GPTRequest(BaseModel):
    model: str
    key: str
    data_file: str
    out_file: str

@app.post("/generate/")
def generate_text(request: GPTRequest):
    command = f"python adv-glue-plus-plus/gpt_eval.py --model {request.model} --key {request.key} --data-file {request.data_file} --out-file {request.out_file}"
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    if result.returncode == 0:
        return {"success": True, "output": result.stdout}
    else:
        return {"success": False, "error": result.stderr}


