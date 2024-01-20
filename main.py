from fastapi import FastAPI
import uvicorn

app = FastAPI()

@app.get("/")
async def root():
    return "hi"

@app.get("/get_path")
async def get_path():
    '''
    Function:   gets something

    Input:      

        {
            "start": ""
        }

    Sample:

        {
            "a":123
        }
    
    Output:

        {
            "number": <integer>
        }
    
    Sample:

        {
            "number":123
        }
    '''

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=5000,reload=True)