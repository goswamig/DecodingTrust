from fastapi import FastAPI
from pydantic import BaseModel
import subprocess
import sys

app = FastAPI()

class GPTRequest(BaseModel):
    model: str
    key: str
    data_file: str
    out_file: str

@app.post("/generate/")
def generate_text(request: GPTRequest):
    command = f"python adv-glue-plus-plus/gpt_eval.py --model {request.model} --key {request.key} --data-file {request.data_file} --out-file {request.out_file}"

    # stdout and stderr goes to stdout 
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)

    # Stream the subprocess output
    for line in iter(process.stdout.readline, ''):
        sys.stdout.write(line)
        sys.stdout.flush()

    process.communicate()  # Wait for the process to finish
    if process.returncode == 0:
        return {"success": True, "output": result.stdout}
    else:
        return {"success": False, "error": result.stderr}



