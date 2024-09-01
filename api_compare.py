from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, HttpUrl
from bedrock_compare import compare_images

app = FastAPI()

class CompareRequest(BaseModel):
    image1_uri: HttpUrl
    image2_uri: HttpUrl

@app.post("/compare")
async def compare(request: CompareRequest):
    try:
        result = compare_images(str(request.image1_uri), str(request.image2_uri))
        return {"comparison_result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
