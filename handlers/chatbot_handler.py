from langchain_community.chat_models import ChatOllama
from langchain.schema import HumanMessage, AIMessage

class ChatbotHandler:
    def __init__(self, model_name, temperature=0.7, verbose=False):
        self.model = ChatOllama(model=model_name, temperature=temperature, verbose=verbose)
        
    
    def chat(self, message, history):
        
        context = """
        당신은 키보드 전문가 챗봇입니다. 다음과 같은 주제에 대해 정확하고 상세한 정보를 제공합니다:
        1. 기계식 키보드의 작동 원리 및 장점.
        2. 멤브레인 키보드와의 차이점.
        3. 키 스위치 종류(Cherry MX, Gateron, Kailh)와 특징.
        4. 키보드 레이아웃(예: ANSI, ISO) 및 적합한 사용 사례.
        5. 게이밍, 프로그래밍, 일반 사용에 적합한 키보드 추천.
        6. 키보드 커스터마이징 방법(예: 키캡 교체, 윤활 작업 등).
        7. 키보드 브랜드 및 종류
        """
        
        chat_history = [HumanMessage(content=context)] #처음 맥락 추가
        
        for human, ai in history:
            chat_history.append(HumanMessage(content=human))
            chat_history.append(AIMessage(content=ai))
        
        if message:
            chat_history.append(HumanMessage(content=message))
            response = self.model.invoke(chat_history)
            if hasattr(response, "content"):
                return response.content  # 문자열 반환
            return str(response)  # 예상치 못한 경우 문자열 반환
        
        return "메시지를 입력해주세요."    
