import uvicorn
from fastapi import FastAPI, Response, status, Header
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
from src import url_shortener

class Url(BaseModel):
    url: str

app = FastAPI()

if __name__ == "__main__":
    # Run the app
    uvicorn.run(
        "app:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
    )

@app.post("/", status_code=status.HTTP_201_CREATED)
def make_short_url(url: Url, response: Response):
    original_url = url.url
        
    if not(original_url.startswith("https://") or original_url.startswith("https://")):
        # 정상 url이 아닐 경우: https:// or http:// 로 시작하지 않는 주소의 경우
        # 400_BAD_REQUEST, {"error": "Invalid URL format"} 응답
        
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"error": "Invalid URL format"}
    
    url_index = url_shortener.search_url(original_url)
    # search_url(): url리스트의 인덱스를 반환
    # url이 존재하면 인덱스 반환, 존재하지 않을 경우 -1 반환
    
    if url_index >= 0:
        # url이 이미 shortened한 url일 경우
        # 200_OK, original_url, short_slug, short_url 응답
        
        response.status_code = status.HTTP_200_OK
        
        short_url = url_shortener.get_slug(url_index)
        # get_slug(): 인덱스를 기준으로 slug 리스트에서 slug 반환
        
        return {
        "original_url": original_url,
        "short_slug": short_url,
        "short_url": "http://localhost:8000/" + short_url
        }
        
    # 기존에 존재하지 않는 url일 경우
    # 201_CREATED, slug 생성 후 original_url, short_slug, short_url 응답
    return {
    "original_url": original_url,
    "short_slug": url_shortener.generate_slug(original_url),
    "short_url": "http://localhost:8000/" + url_shortener.generate_slug(original_url)
    }

@app.get("/{slug}", status_code=status.HTTP_200_OK)
def url_responce(slug: str, response: Response):
    
    print(slug)
    
    url_index = url_shortener.search_slug(slug)
    # search_slug(): slug가 이미 존재하는지 확인
    # 존재한다면 인덱스 반환, 존재하지 않는다면 -1 반환
    
    if url_index >= 0:
        # slug가 이미 존재할 경우
        # 308_PERMANENT_REDIRECT, {"url": original_url} 응답
        print("url", url_shortener.get_url(url_index))
        
        return RedirectResponse(url=url_shortener.get_url(url_index))
    
    # url이 슬러그 필드에 존재할 경우 404
    response.status_code = status.HTTP_404_NOT_FOUND
    return {"error": "URL not found"}

@app.get("/", status_code=status.HTTP_200_OK)
def root():
    return {"messsage: hello world!"}