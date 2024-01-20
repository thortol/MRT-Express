from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from classes import MainController

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
            "end": <string with the station code>,
            "exit": <string ABC123>
        }

    Sample:

        {
            "start": "NS1",
            "end": "NS3",
            "exit": "A"
        }
    
    Output:

        {
            "stations": [
                {
                    "name": <string representing station>,
                    "instructions": [
                        {
                            "type": <2 types board or transfer>,
                            "station": <string representing station>,
                            "details": <string with details>,
                            "towards": <string representing station>
                        }
                    ]
                },
                {
                    "name": "NE7",
                    "instructions": [
                        {
                            "type": <2 types board or transfer>,
                            "description": <string>
                        },
                        {
                            "type": <2 types board or transfer>,
                            "station": <string representing station>,
                            "details": <string with details>,
                            "towards": <string representing station>
                        }
                    ]
                },
                {
                    "name": <string representing station>,
                    "instructions": []
                }
            ],
            "time": <integer>
        }
    
    Sample:

        {
            "stations": [
                {
                    "name": "NE1",
                    "instructions": [
                        {
                            "type": "board",
                            "station": "NE1",
                            "details": "Platform B, Door ('12', '12', '12')",
                            "towards": "NE17"
                        }
                    ]
                },
                {
                    "name": "NE7",
                    "instructions": [
                        {
                            "type": "transfer",
                            "description": "transfer to downtown line"
                        },
                        {
                            "type": "board",
                            "station": "DT12",
                            "details": "Platform A, Door ('8', '5', '10')",
                            "towards": "DT35"
                        }
                    ]
                },
                {
                    "name": "DT13",
                    "instructions": []
                }
            ],
            "time": 17
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