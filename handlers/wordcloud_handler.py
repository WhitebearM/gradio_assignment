from wordcloud import WordCloud
import matplotlib.pyplot as plt

class WordCloudHandler:
    def generate_wordcloud(self, text, font_path, output_path="wordcloud.png"):
        wordcloud = WordCloud(
            font_path=font_path,
            background_color="white",
            width=800,
            height=600,
            max_words=200
        ).generate(text)

        plt.figure(figsize=(10, 5))
        plt.imshow(wordcloud, interpolation="bilinear")
        plt.axis("off")
        plt.tight_layout()
        plt.savefig(output_path)
        plt.close()
        return output_path
