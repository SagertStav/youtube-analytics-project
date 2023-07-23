import src.channel
class Video(src.channel.Channel):
    """Класс для ВИДЕО ютуб - канала"""
    def __init__(self, video_id) -> None:
       """
       Инициализация реальными данными атрибутов экземпляра класса `Video`:
       - id видео
       - название видео video_title
       - ссылка на видео
       - количество просмотровpy
       - количество лайков
       """
       '''
       получить статистику видео по его id
       получить id можно из адреса видео
       https://www.youtube.com/watch?v=gaoc9MPZ4bw или https://youtu.be/gaoc9MPZ4bw
       '''
       #video_id = 'gaoc9MPZ4bw'
       video_response = self.get_service().videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                              id=video_id
                                              ).execute()
       #print(video_response)
       self.__video_id = video_id                                                    # id видео
       try:
          self.title:str = video_response['items'][0]['snippet']['title']         # название видео
       except IndexError:
           if len(video_response['items']) == 0:
               self.title = None
               self.url = None
               self.view_count = None
               self.like_count = None
               print(f"На текущий момент видео с кодом '{video_id}' отсутствует!")
       else:
          self.url = 'https://www.youtu.be.com/'+video_id                               # ссылка на видео
          self.view_count: int = video_response['items'][0]['statistics']['viewCount']  # количество просмотров
          self.like_count: int = video_response['items'][0]['statistics']['likeCount']  # количество лайков

    def __str__(self):
        return f"{self.title}"

class PLVideo(Video):
    def __init__(self, video_id: str, playlist_id: str) -> None:
        """ Инициализация по 'id видео' и 'id плейлиста'
        > Видео может находиться в множестве плейлистов, поэтому непосредственно из видео через API информацию о плейлисте не получить.
         Инициализация реальными данными атрибутов экземпляра подкласса PLVideo:
        - id видео
        - название видео
        - ссылка на видео
        - количество просмотров
        - количество лайков
        - id плейлиста  """

        self.__playlist_id = self.playlist_id = playlist_id
        super().__init__(video_id)



