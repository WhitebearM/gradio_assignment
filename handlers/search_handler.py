import requests
from bs4 import BeautifulSoup

class SearchHandler:
    def search_with_scraping(self, query):
        """
        Google 검색을 통해 키보드 관련 정보를 크롤링합니다.
        """
        search_url = f"https://www.google.com/search?q={query.replace(' ', '+')}+keyboard"
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(search_url, headers=headers)
        
        if response.status_code != 200:
            return f"크롤링 실패: {response.status_code}"
        
        soup = BeautifulSoup(response.text, "html.parser")
        results = []

    
     # Google 검색 결과의 최신 CSS 선택자에 맞게 수정
        for result in soup.find_all('div', {'class': 'tF2Cxc'}):
            try:
                title = result.find('h3').text  # 결과 제목
                link = result.find('a')['href']  # 결과 링크
                results.append(f"{title} - {link}")
            except AttributeError:
                continue
        
        return results if results else ["검색 결과를 찾을 수 없습니다."]
