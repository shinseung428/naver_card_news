# 네이버 카드 뉴스 생성기

네이버 뉴스 URL 제공해주면 카드뉴스 형태의 결과를 내보내주는 코드(네이버뉴스 링크만 가능) 
1. 네이버 뉴스 URL 에서 BeautifulSoup 사용해 제목과 본문 추출
2. [OpenAI ChatGPT API](https://platform.openai.com/docs/api-reference/introduction) 또는 [업스테이지 Solar API](https://developers.upstage.ai/terms-and-policies/solar/terms-of-service) 사용해 내용 요약
3. 카드뉴스 이미지 템플릿 사용해 이미지 생성

## Results
### Sample 1
News URL: https://n.news.naver.com/mnews/article/421/0007494658
```
python main.py --url https://n.news.naver.com/mnews/article/421/0007494658
```
<img src="https://github.com/shinseung428/naver_card_news/assets/17181911/afa87151-0b40-489c-a4ab-f613926531ad" width="640">

### Sample 2
News URL: https://n.news.naver.com/mnews/article/001/0014643838
```
python main.py --url https://n.news.naver.com/mnews/article/001/0014643838
```
<img src="https://github.com/shinseung428/naver_card_news/assets/17181911/52cb4bd6-66c7-4152-9b8a-91e27fe9b5dc" width="640">

