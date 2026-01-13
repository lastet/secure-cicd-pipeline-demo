from fastapi import FastAPI

app = FastAPI(title="Secure CI/CD Demo")

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/hello")
def hello(name: str = "mr unicorn"):
    if name == "anya":
        return {"message": "hello, blonde"}
    return {"message": f"hello, {name}"}
