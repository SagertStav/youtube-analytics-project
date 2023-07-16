import os
import json

# необходимо установить через: pip install google-api-python-client
from googleapiclient.discovery import build


class Channel:
    """Класс для ютуб - канала"""

    api_key: str = os.getenv('API_KEY')  # было 'YT_API_KEY'

    @classmethod
    def get_service(cls):
        """ get_service() возвращает объект для работы с YouTube API """
        return build('youtube', 'v3', developerKey = cls.api_key)


    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала.
        Дальше все данные будут подтягиваться по API."""
        self.__channel_id = channel_id
        channel = self.get_service().channels().list(id=channel_id, part='snippet,statistics').execute()
        self.title= channel["items"][0] ['snippet']['title']                         # - название канала
        self.description= channel['items'][0]["snippet"]["description"]              # - описание канала
        self.url = 'https://www.youtube.com/channel/'+channel_id                     # - ссылка на канал
        self.subscriber_count = int(channel['items'][0]["statistics"]["subscriberCount"]) # - количество подписчиков
        self.video_count = channel['items'][0]["statistics"]["videoCount"]           # - количество видео
        self.view_count = channel['items'][0]["statistics"]["viewCount"]             # - общее количество просмотров

    def __str__(self):
        return f"'{self.title} ({self.url})'"

    def __add__(self, other):
        return self.subscriber_count + other.subscriber_count

    def __sub__(self, other):
        return self.subscriber_count - other.subscriber_count

    def __gt__(self, other):
        return self.subscriber_count > other.subscriber_count

    def __ge__(self, other):
        return self.subscriber_count >= other.subscriber_count

    def __lt__(self, other):
        return self.subscriber_count < other.subscriber_count

    def __le__(self, other):
        return self.subscriber_count <= other.subscriber_count

    def __eq__(self, other):
        return self.subscriber_count == other.subscriber_count

    # Геттер для channel_id, без создания сеттера
    @property
    def channel_id(self):
        return self.__channel_id
    @channel_id.setter
    def channel_id(self,name):
        """Метод срабатывает при операции присваивания:
        СИМУЛИРУЮ отсутствие сеттера для .channel_id - для достижения целей ожидаемого поведения main по ДЗ2 """
        print("AttributeError: property 'channel_id' of 'Channel' object has no setter")
        # сами переприсваивания игнорирую здесь, ничего не выполняя
        # (взамен обработки исключений try ... except AttributeError ...


    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        channel = self.get_service().channels().list(id=self.channel_id, part='snippet,statistics').execute()
        print(json.dumps(channel["items"][0], indent=2, ensure_ascii=False))



    def to_json(self, jsn_of_channel_file):
        '''to_json() сохраняет в файл значения атрибутов экземпляра Channel'''
        with open(jsn_of_channel_file, 'w') as f:
            #print(self.__dict__)
            json.dump(self.__dict__, f)

    def printj(dict_to_print: dict) -> None:
       """Выводит словарь в json-подобном удобном формате с отступами"""
       print(json.dumps(dict_to_print, indent=2, ensure_ascii=False))
