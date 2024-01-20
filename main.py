from fastapi import FastAPI, Request
import uvicorn

from classes import MainController

app = FastAPI()
mc = MainController()

@app.get("/")
async def root():
    return "hi"

@app.post("/get_path")
async def get_path(request: Request):
    '''
    Function:   gets something

    Input:      

        {
            "start": <string with the station code>,
            "end": <string with the station code>
        }

    Sample:

        {
            "start": "NS1",
            "end": "NS3"
        }
    
    Output:

        {
            "stations" :
            [
                {
                    "name": "EW24",
                    "instructions":                 
                    [
                        {
                            "type":"board",
                            "station": "EW24",
                            "details": "Platform A, Door 7",
                            "towards": "EW1"
                        }
                    ]
                },
                {
                    "name": "EW21",
                    "instructions":
                    [
                        {
                            "type": "transfer",
                            "description": "transfer to circle line"
                        },
                        {
                            "type":"board",
                            "station": "EW21",
                            "details": "Platform A, Door 7",
                            "towards": "CC1"
                        }
                    ]
                }
            ]
        }
    
    Sample:

        {
            "number":123
        }
    '''
    json = await request.json()
    return mc.get_path(json)
    return       {
            "stations" :
            [
                {
                    "name": "EW24",
                    "instructions" :                
                    [
                        {
                            "type":"board",
                            "station": "EW24",
                            "details": "Platform A, Door 7",
                            "towards": "EW1"
                        }
                    ]
                },
                {
                    "name": "EW21",
                    "instructions":
                    [
                        {
                            "type": "transfer",
                            "description": "transfer to circle line"
                        },
                        {
                            "type":"board",
                            "station": "EW21",
                            "details": "Platform A, Door 7",
                            "towards": "CC1"
                        }
                    ]
                }
            ]
        }

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=5001,reload=True)