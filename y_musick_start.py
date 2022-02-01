from yandex_music import Client
import sqlite3
import os

#import dic_part

direct = 'tracks\\'


def proc_captcha(captcha_image_url):
        print(captcha_image_url['x_captcha_url'])
        return input('Код с картинки: ')

def logPassAuth():
        log = input('Введите почту: ')
        password = input('Введите пароль: ')
        try:
                client = Client.from_credentials(log, password, captcha_callback=proc_captcha)
                return client
        except:
                print('Неверный логин, пароль или капча')
                logPassAuth()

def authorization():
        bdDir = 'database\\'
        #print(os.path.exists(bdDir))
        if os.path.exists(bdDir) == False:
                os.mkdir('database')
                conn = sqlite3.connect(f'{bdDir}YMbase.db')
                cur = conn.cursor()
                cur.execute("""CREATE TABLE IF NOT EXISTS userInfo(
                userid INT PRIMARY KEY,
                YMtoken TEXT,
                display_name TEXT);
                """)
                conn.commit()
                print('бд создана')
                print('Вам необходимо единоразово войти в свой аккаунт яндекс для получения API токена.')
                
                
                logPassClient = logPassAuth()
                #print(logPassClient)
                token = logPassClient['token']
                uinfo = []
                uinfo.append(logPassClient.accountStatus().account['uid'])
                uinfo.append('None')
                uinfo.append(logPassClient.accountStatus().account['display_name'])
                #print(uinfo)
                cur.execute("INSERT INTO userInfo VALUES(?, ?, ?);", uinfo)
                conn.commit()
                try:
                        client = Client.from_token(token)
                        print(client['token'])
                        print(uinfo[0])
                        cur.execute("""UPDATE userInfo set YMtoken = ? where userid = ?""", (f"{client['token']}", uinfo[0]))
                        conn.commit()
                        conn.close()
                        print('бд заполнена и закрыта')
                        print(f'{uinfo[2]}, токен успешно получен.')
                        return client
                        
                except:
                        print('Ошибка авторизации по токену. Будет использована авторизация лог\пар')
                        return logPassAuth()
        else:
                conn = sqlite3.connect(f'{bdDir}YMbase.db')
                cur = conn.cursor()
                cur.execute("""SELECT * from userInfo""")
                records = cur.fetchall()
                print('ваш токен успешно считан:')
                #print(records[0][1])
                try:
                        print(records[0][1])
                        client = Client.from_token(records[0][1])
                        print(f'\n\n\n{records[0][2]}, авторизация по токену завершена\n\n\n')
                        return client
                except:
                        print('Ошибка авторизации по токену. Будет использована авторизация лог\пар')
                        return logPassAuth()
                


type_to_name = {
    'track': 'трек',
    'artist': 'исполнитель',
    'album': 'альбом',
    'playlist': 'плейлист',
    'video': 'видео',
    'user': 'пользователь',
    'podcast': 'подкаст',
    'podcast_episode': 'эпизод подкаста',
}


def send_search_request_and_print_result(client, query):

    search_result = client.search(query)

    text = [f'Результаты по запросу "{query}":', '']

    best_result_text = ''
    if search_result.best:
        type_ = search_result.best.type
        best = search_result.best.result

        #print(best)
        #print(best.id)
        if type_ in ['track', 'podcast_episode']:
            artists = ''
            if best.artists:
                artists = ' - ' + ', '.join(artist.name for artist in best.artists)
            best_result_text = best.title + artists
            path = direct+best_result_text+'.mp3'
            best.download(path)
            res = best_result_text+'.mp3'
            return res
    else:
            print("трек не найден")
            return '-1'

def playlists_list(client):
        alb_list = client.users_playlists_list()
        user_playlists = client.users_playlists_list()
        last_list = list(p.title for p in user_playlists)
        last_list.append('likes')
        last_list.append('плейлист дня')
        return last_list
def playlist_info(client, title_list):
        user_playlists = client.users_playlists_list()
        if title_list == 'likes':
                tracks = client.users_likes_tracks()
                total_tracks = len(tracks.tracks)
                return f'В очередь будет добавлено {total_tracks} track(s) из плейлиста liked tracks.'
        elif title_list == 'плейлист дня':
            PersonalPlaylistBlocks = client.landing(blocks=['personalplaylists']).blocks[0]
            DailyPlaylist = next(x.data.data for x in PersonalPlaylistBlocks.entities if x.data.data.generated_playlist_type == 'playlistOfTheDay')
            total_tracks = DailyPlaylist.track_count
            #print(DailyPlaylist)
            return f'В очередь будет добавлен плейлист дня. {total_tracks} track(s).'

            
        else:
                playlist = next((p for p in user_playlists if p.title == title_list), None)
                if playlist == None:
                        return f'playlist "{args.playlist_name}" not found'
                total_tracks = playlist.track_count
                return f'В очередь будет добавлен плейлист {playlist.title}. {total_tracks} track(s).'
                
        
def tracks_from_playlist(client, title_list):
        
       
        #print(alb_list)
        user_playlists = client.users_playlists_list()
        #print('specify --playlist-name', list(p.title for p in user_playlists))

        if title_list == 'likes':
                tracks = client.users_likes_tracks()
                total_tracks = len(tracks.tracks)
                print(f'Playing liked tracks. {total_tracks} track(s).')
        elif title_list == 'плейлист дня':
                PersonalPlaylistBlocks = client.landing(blocks=['personalplaylists']).blocks[0]
                DailyPlaylist = next(x.data.data for x in PersonalPlaylistBlocks.entities if x.data.data.generated_playlist_type == 'playlistOfTheDay')
                total_tracks = DailyPlaylist.track_count
                #print(total_tracks)
                tracks = DailyPlaylist.tracks if DailyPlaylist.tracks else DailyPlaylist.fetch_tracks()
                #print(tracks)
                
        else:       
                playlist = next((p for p in user_playlists if p.title == title_list), None)
                if playlist == None:
                        print(f'playlist "{args.playlist_name}" not found')
                total_tracks = playlist.track_count
                print(f'Playing {playlist.title} ({playlist.playlist_id}). {total_tracks} track(s).')
                tracks = playlist.tracks if playlist.tracks else playlist.fetch_tracks()
                #print(tracks)
                
        short_track_mass = []
        for (i, short_track) in enumerate(tracks):
                short_track_mass.append(short_track)
                #print(i)
        tracks_list = []
        for i in range(0, total_tracks):
                
                track = short_track_mass[i].track if short_track_mass[i].track else short_track_mass[i].fetchTrack()
                #print(f'{track.title}_{track.artists[0].name}.mp3')
                #tracks_list.append(f'{track.title}_{track.artists[0].name}.mp3')
                tracks_list.append(f'{track.title} {track.artists[0].name}')
                
        #print(tracks_list)
        return tracks_list

def albums_to_playlist(client, ALBUM_ID):
        album = client.albums_with_tracks(ALBUM_ID)
        tracks = []
        for i, volume in enumerate(album.volumes):
                if len(album.volumes) > 1:
                        tracks.append(f'💿 Диск {i + 1}')
                tracks += volume
        #print(tracks)
        tracks_list = []
        for track in tracks:
                if isinstance(track, str):
                        #print(track)
                        tracks_list.append(track)
                else:
                        artists = ''
                        if track.artists:
                                artists = ' - ' + ', '.join(artist.name for artist in track.artists)
                        #print(track.title + artists)
                        tracks_list.append(track.title + artists)
        #print(tracks_list)
        text = 'АЛЬБОМ\n\n'
        text += f'{album.title}\n'
        text += f"Исполнитель: {', '.join([artist.name for artist in album.artists])}\n"
        tracks_list.append(text)
        return tracks_list
'''
if __name__ == '__main__':
    while True:
        input_query = input('Введите поисковой запрос: ')
        send_search_request_and_print_result(input_query)
'''

#clientAss = authorization()
#playlist_info(clientAss, 'Плейлист дня')
#print(albums_playlist(clientAss, 5829983))
#tracks_from_playlist(clientAss, 'плейлист дня')
