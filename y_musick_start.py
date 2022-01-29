from yandex_music import Client

    
direct = 'tracks\\'

#AQAAAAAXBmN5AAdIuOE4IESjoU-kkBNpkBWd5EI
client = Client.from_credentials('blabla@yandex.ru', 'blablapass')#ТУТ СВОИ ДАННЫЕ
#client = Client.from_token('AQAAAAAXBmN5AAdIuOE4IESjoU-kkBNpkBWd5EI')

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


def send_search_request_and_print_result(query):

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

def playlists_list():
        alb_list = client.users_playlists_list()
        user_playlists = client.users_playlists_list()
        last_list = list(p.title for p in user_playlists)
        last_list.append('likes')
        return last_list
def playlist_info(title_list):
        user_playlists = client.users_playlists_list()
        if title_list == 'likes':
                tracks = client.users_likes_tracks()
                total_tracks = len(tracks.tracks)
                return f'В очередь будет добавлено {total_tracks} track(s) из плейлиста liked tracks.'
        else:       
                playlist = next((p for p in user_playlists if p.title == title_list), None)
                if playlist == None:
                        return f'playlist "{args.playlist_name}" not found'
                total_tracks = playlist.track_count
                return f'В очередь будет добавлен плейлист {playlist.title}. {total_tracks} track(s).'
                
        
def tracks_from_playlist(title_list):
        
       
        #print(alb_list)
        user_playlists = client.users_playlists_list()
        #print('specify --playlist-name', list(p.title for p in user_playlists))

        if title_list == 'likes':
                tracks = client.users_likes_tracks()
                total_tracks = len(tracks.tracks)
                print(f'Playing liked tracks. {total_tracks} track(s).')
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
                
        print(tracks_list)
        return tracks_list
'''
if __name__ == '__main__':
    while True:
        input_query = input('Введите поисковой запрос: ')
        send_search_request_and_print_result(input_query)
'''


#tracks_from_playlist('likes')
