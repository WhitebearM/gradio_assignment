import gradio as gr
from config.config import Config
from handlers.chatbot_handler import ChatbotHandler
from handlers.image_handler import ImageHandler
from handlers.wordcloud_handler import WordCloudHandler
from handlers.audio_handler import AudioHandler
from handlers.db_handler import DBHandler
# from handlers.search_handler import SearchHandler

# 핸들러 초기화
config = Config()
chatbot_handler = ChatbotHandler(config.GEMMA2_MODEL_NAME, config.GEMMA2_TEMPERATURE)
image_handler = ImageHandler()
wordcloud_handler = WordCloudHandler()
audio_handler = AudioHandler()
db_handler = DBHandler()
# searchHandler = SearchHandler()

def search_keyboard(model_name):
    return db_handler.search_keyboard_model(model_name)

# Gradio 인터페이스 생성
with gr.Blocks() as iface:
    with gr.Tab("키보드에 대해서 물어보셈"):
        gr.ChatInterface(
            fn=chatbot_handler.chat,
            examples=[
                "안녕하세요!",
                "키보드의 축 종류는 무엇이 있나요?",
                "키보드는 브랜드 추천해주세요."
            ],
            title="챗봇",
            description="키보드에 관해서 궁금한 정보가 있으신가요?"
        )
        
    with gr.Tab("키보드 검색"):
        gr.Markdown("키보드 모델 정보 검색")
        gr.Markdown("키보드 모델명을 입력하면 관련 정보를 검색합니다.")
        
        model_input = gr.Textbox(label="키보드 모델명 입력")
        output_text = gr.Textbox(label="검색 결과")
        search_button = gr.Button("검색 시작")
        
        search_button.click(
            fn = search_keyboard,
            inputs=[model_input],
            outputs=[output_text]
        )
        
        
    # with gr.Tab("키보드 모델 검색"):
    #     gr.Markdown("키보드 모델 관려 정보 검색")
    #     gr.Markdown("키보드 이름을 입력하면 관련 홈페이지나 기사를 검색합니다.")
        
    #     model_input = gr.Textbox(label="키보드 모델명 입력")
    #     output_text = gr.Textbox(label="검색 결과")
    #     search_button = gr.Button("검색 시작")
        
    #     def fetch_search_result(model_name):
    #         """
    #         크롤링 핸들러를 사용해 모델명 검색 결과 반환
    #         """
            
    #         results = searchHandler.search_with_scraping(model_name)
    #         return "\n".join(results)
        
    #     search_button.click(
    #         fn=fetch_search_result,
    #         inputs=[model_input],
    #         outputs=[output_text]
    #     )
        
    with gr.Tab("이미지 분석"):
        image_input = gr.Image(type="pil", label="이미지를 업로드해주세요")
        submit_button = gr.Button("분석")
        output_text = gr.Textbox(lines=5, label="결과")
        submit_button.click(image_handler.analyze_image, inputs=[image_input], outputs=output_text)
        
    with gr.Tab("wordCloud"):
        upload_file = gr.File(label="파일 업로드", file_types=[".txt"])
        output_image = gr.Image(label="워드 클라우드 결과")
        output_message = gr.Textbox(label="결과 메시지")
        generate_btn = gr.Button("결과 생성")
        generate_btn.click(
            fn=lambda file: wordcloud_handler.generate_wordcloud(file.read(), config.FONT_PATH),
            inputs=[upload_file],
            outputs=[output_message, output_image]
        )
        
    with gr.Tab("음성 텍스트 반환"):
        audio_file = gr.File(label="오디오 파일 업로드", file_types=[".wav", ".mp3"])
        output_text = gr.Textbox(label="변환된 텍스트")
        transcribe_btn = gr.Button("변환 시작")
        transcribe_btn.click(audio_handler.transcribe_audio, inputs=[audio_file], outputs=[output_text])

iface.launch(server_port=7989, server_name="0.0.0.0")
