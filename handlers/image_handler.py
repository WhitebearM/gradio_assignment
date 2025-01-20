from transformers import BlipProcessor, BlipForConditionalGeneration
from deep_translator import GoogleTranslator

class ImageHandler:
    def __init__(self):
        self.processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
        self.model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")

    def generate_description(self, image):
        inputs = self.processor(images=image, return_tensors="pt")
        outputs = self.model.generate(**inputs)
        return self.processor.decode(outputs[0], skip_special_tokens=True)

    def translate_to_korean(self, text):
        return GoogleTranslator(source='en', target="ko").translate(text)

    def analyze_image(self, image):
        if image is None:
            return "이미지를 업로드해주세요."
        try:
            description = self.generate_description(image)
            return self.translate_to_korean(description)
        except Exception as e:
            return f"이미지 분석에 실패했습니다: {str(e)}"
