import speech_recognition as sr
from pydub import AudioSegment
import os

class AudioHandler:
    def transcribe_audio(self, uploaded_audio):
        if uploaded_audio is None:
            return "오디오 파일을 업로드해주세요."

        recognizer = sr.Recognizer()
        try:
            audio_path = uploaded_audio.name
            audio = AudioSegment.from_file(audio_path)
            wav_path = "temp.wav"
            audio.export(wav_path, format="wav")

            with sr.AudioFile(wav_path) as source:
                audio_data = recognizer.record(source)
                text = recognizer.recognize_google(audio_data, language="ko-KR")
            
            os.remove(wav_path)
            return text
        except sr.UnknownValueError:
            return "음성을 인식할 수 없습니다."
        except sr.RequestError as e:
            return f"STT 서비스에 문제가 발생했습니다: {e}"
