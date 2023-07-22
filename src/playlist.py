import isodate
import datetime
import src.channel
class PlayList(src.channel.Channel):
    """   Реализуем класс `PlayList` ВИДЕО ютуб-канала, который инициализируется _id_ плейлиста
         и имеет следующие публичные атрибуты:
         - название плейлиста
         - ссылку на плейлист

     Методы класса `PlayList`
     - `total_duration`  -    возвращает объект класса `datetime.timedelta` с суммарной длительностью
     плейлиста(обращение как к свойству, использовать ` @ property `)
     - `show_best_video() -  возвращает ссылку на самое популярное видео из плейлиста (по
     количеству лайков)
    """

    def get_one_video_duration(self, video_id):
        """ возвращает продолжительность в секундах одного видео из плэйлиста по его video_id """
        #part = 'snippet,statistics,contentDetails,topicDetails',
        video_response = self.get_service().videos().list(part='contentDetails',
                                               id=video_id
                                               ).execute()
        return isodate.parse_duration(video_response['items'][0]['contentDetails']['duration']).seconds

    @property
    def total_duration(self):
        """возвращает длительность плэйлиста в формате времени 1:49:52 """

        playlist_videos = self.get_service().playlistItems().list(playlistId=self.__playlist_id,
                                                part='contentDetails',
                                                maxResults=50).execute()
        # сначала получим список всех видео-id в плэй-листе
        video_ids: list[str] = [video['contentDetails']['videoId'] for video in playlist_videos['items']]
        total_duration=datetime.timedelta(seconds=sum(self.get_one_video_duration(x) for x in video_ids))
        return total_duration



    def __init__(self, playlist_id)  -> None:
        #part = 'contentDetails, snippet',
        playlist_videos = self.get_service().playlistItems().list(playlistId=playlist_id,
                                                       part='snippet',

                                                       maxResults=50).execute()
        print(playlist_videos)
        self.__playlist_id=playlist_id
        print('title', playlist_videos)
 # Не совсем понятно, как надо было вытащить название плэйлиста ниже:   #https://stackoverflow.com/questions/68648806/how-to-get-the-title-of-a-playlist-from-the-youtube-api
        #self.title =playlist_videos['items'][0]['snippet']['title'].split('. ')[0]  # название плэй-листа
        pl_list=self.get_service().playlists().list(channelId=playlist_videos['items'][0]['snippet']['channelId'],
                                                       part='snippet', maxResults=50).execute()
        print(pl_list)
        self.title=pl_list['items'][0]['snippet']['title']

        self.url="https://www.youtube.com/playlist?list="+playlist_id


    def show_best_video(self):
        """ show_best_video() возвращает ссылку на самое популярное видео из плейлиста(по количеству лайков) """

        # сначала получим список всех видео-id в плэй-листе
        playlist_videos = self.get_service().playlistItems().list(playlistId=self.__playlist_id,
                                                part='contentDetails',
                                                maxResults=50).execute()

        #list_vidos:list[[int,str]]=[]
        list_vidos=[]
        #пройдемся снова по всем видео по их видео-id, запрашивая статистику конкретного видео в части лайков
        for vid in [video['contentDetails']['videoId'] for video in playlist_videos['items']]:

            video_response = self.get_service().videos().list(part='statistics',
                                               id=vid
                                               ).execute()
            #print(vid, int(video_response['items'][0]['statistics']['likeCount']))

            #list_vidos.append([100-int(video_response['items'][0]['statistics']['likeCount']),vid])
            # Добавив выше "100-" внутри выражения, убедился, что списки в Питоне по умолчанию отсортированные,
            # поэтому дополнительно сортировку не использую - возьму последний элемент с "хвоста"

            list_vidos.append([int(video_response['items'][0]['statistics']['likeCount']), vid])
        #print(sorted(list_vidos))

        return f'https://youtu.be/{list_vidos[-1][1]}'
