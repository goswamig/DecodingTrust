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


jobs = []

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

# TODO: Add logic to connect to DB
@app.get("/job/describe/{job_id}")
def describe_job(job_id: str):
    # Implement the logic to describe a job based on the job_id
    return {"job_id": job_id, "description": "Job description goes here"}

@app.post("/job/start/{job_id}")
def start_job(job_id: str):
    # Implement the logic to start a job based on the job_id
    return {"job_id": job_id, "status": "Job started"}

@app.post("/job/stop/{job_id}")
def stop_job(job_id: str):
    # Implement the logic to stop a job based on the job_id
    return {"job_id": job_id, "status": "Job stopped"}

@app.get("/jobs/")
def list_jobs():
    return {"jobs": jobs}
