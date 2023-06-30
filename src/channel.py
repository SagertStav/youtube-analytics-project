import os, json  #isodate

# необходимо установить через: pip install google-api-python-client
from googleapiclient.discovery import build


class Channel:
    """Класс для ютуб-канала"""

    api_key: str = os.getenv('API_KEY')  # было 'YT_API_KEY'

    @classmethod
    def get_service(self):
        """ get_service() возвращает объект для работы с YouTube API """
        return build('youtube', 'v3', developerKey=self.api_key)


    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.channel_id = channel_id

    # channel_id = 'UC-OVMPlMA3-YCIeg4z5z23A'  # MoscowPython
 #   channel_id = 'UCwHL6WHUarjGfUM_586me8w'  # HighLoad Channel
        channel = self.get_service().channels().list(id=channel_id, part='snippet,statistics').execute()
        #with channel["items"][0] as i:
        #   print(channel["items"][0])
        self.title= channel["items"][0] ['snippet']['title']                         # - название канала
        self.description= channel['items'][0]["snippet"]["description"]              # - описание канала
        self.url = 'https://www.youtube.com/channel/'+channel_id                     # - ссылка на канал
        self.subscriber_count = channel['items'][0]["statistics"]["subscriberCount"] # - количество подписчиков
        self.video_count = channel['items'][0]["statistics"]["videoCount"]           # - количество видео
        self.view_count = channel['items'][0]["statistics"]["viewCount"]             # - общее количество просмотров

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        #print(f'ID ютуб-канала: {self.__dict__}')
        channel = self.get_service().channels().list(id=self.channel_id, part='snippet,statistics').execute()
        #print(channel["items"][0])
        print(json.dumps(channel["items"][0], indent=2, ensure_ascii=False))




    def to_json(self, jsn_of_channel_file):
        '''to_json() сохраняет в файл значения атрибутов экземпляра Channel'''
        #json_string=
        with open(jsn_of_channel_file, 'w') as f:
            print(self.__dict__)
            json.dump(self.__dict__, f)

