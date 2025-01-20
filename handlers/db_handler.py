import pymysql
from config.config import Config

class DBHandler:
    def __init__(self):
        # Config 클래스를 사용해 DB 연결 정보 가져오기
        self.connection = pymysql.connect(
            host=Config.DB_HOST,
            user=Config.DB_USER,
            password=Config.DB_PASSWORD,
            database=Config.DB_NAME,
            charset=Config.DB_CHARSET,
            cursorclass=pymysql.cursors.DictCursor
        )

    def fetch_keyboard_info(self, model_name):
        """
        키보드 모델명을 기준으로 DB에서 정보를 검색.
        """
        with self.connection.cursor() as cursor:
            sql = "SELECT * FROM keyboards WHERE model LIKE %s"
            cursor.execute(sql, (f"%{model_name}%",))
            result = cursor.fetchall()
        return result

    def search_keyboard_model(self, model_name):
        """
        키보드 모델명을 기준으로 DB에서 정보를 검색하고 형식화된 결과 반환.
        """
        results = self.fetch_keyboard_info(model_name)
        if results:
            return "\n".join([f"{row['brand']} {row['model']}: {row['description']} - {row['link']}" for row in results])
        return "검색 결과를 찾을 수 없습니다."

    def close_connection(self):
        self.connection.close()
