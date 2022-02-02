import asyncio
import ffmpeg
import discord
import os
import random
from urllib.parse import urlparse
from asgiref.sync import async_to_sync

import y_musick_start
 
from discord.ext import commands

#d49ed4
#embed = discord.Embed(title="", description="", colour=0xD49ED4)
#embed.set_author(name="Sena", icon_url="https://static2.aniimg.com/upload/20170516/422/O/w/9/Ow9EEF.jpg")
direct = 'tracks\\'
if os.path.exists(direct) == False:
        os.mkdir('tracks')

server, server_id, channel_id, voice, client = None, None, None, None, None
is_pause, is_loop = False, False
tasks = list()
queue = []
queue_playlist = []


def create_embed(title, description):
        embed = discord.Embed(title=title, description=description, colour=0xD49ED4)
        #embed.set_author(name="Sena", icon_url="https://i.ytimg.com/vi/edKQaVGAzO0/hqdefault.jpg")
        return embed

def check_queue(client, ctx, voice):
        
                global queue, queue_playlist, is_loop
                
                async def redirect(ctx, embed):
                        await ms_send(ctx, embed)
                        
                
                if len(queue) == 0:
                        print('обычная пустая')
                        files = os.listdir(direct)
                        for i in range(0, len(files)):
                                os.remove(direct+files[i])

                        if len(queue_playlist) !=0:
                                res = y_musick_start.send_search_request_and_print_result(client, queue_playlist[0])
                                print(res)
                                if is_loop:
                                        queue_playlist.append(queue_playlist[0])
                                
                                #queue_playlist.pop(0)
                                player = direct+res
                                voice.play(discord.FFmpegPCMAudio(executable="ffmpeg.exe", source = player), after = lambda x=0: check_queue(client, ctx, voice))
                                asyncio.run_coroutine_threadsafe(redirect(ctx, create_embed('Сейчас играет', res[:-3])), bot.loop)
                                del queue_playlist[0]
                                
                        else:
                                print('оба пустые')
                                files = os.listdir(direct)
                                for i in range(0, len(files)):
                                        os.remove(direct+files[i])
                else:
                        
                        print(queue[0])
                        res = queue[0]
                        player = direct+str(queue[0])
                        if is_loop:
                                queue.append(queue[0])
                        voice.play(discord.FFmpegPCMAudio(executable="ffmpeg.exe", source = player), after = lambda x=0: check_queue(client, ctx, voice))
                        asyncio.run_coroutine_threadsafe(redirect(ctx, create_embed('Сейчас играет', res[:-3])), bot.loop)
                        del queue[0]
                        
 
class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    #@commands.command()
    #async def join(self, ctx):
            

   
    @commands.command()
    async def join(self, ctx, *, command =  None):   
        """Joins a voice channel"""
        global server, server_id, channel_id, voice, queue, client
        #print(client)
        author = ctx.author
        name_channel = author.voice.channel.name
        channel_id = author.voice.channel.id
        server_id = ctx.guild.id
        server = bot.get_guild(server_id)
        voice_channel = discord.utils.get(ctx.guild.voice_channels, id = channel_id)
        embed = discord.Embed(title=f"Connect to {name_channel}", description="", colour=0xD49ED4)
        await ctx.send(embed = embed)
        voice = discord.utils.get(bot.voice_clients, guild = server)
        if voice is None:
                await voice_channel.connect()
        voice = discord.utils.get(bot.voice_clients, guild = server)
        
    
    @commands.command()
    async def play(self, ctx, *, query):
        """Plays a file from the local filesystem"""
        global server, server_id, channel_id, queue, queue_playlist, client
        server_id = ctx.guild.id
        server = bot.get_guild(server_id)
        author = ctx.author
        name_channel = author.voice.channel.name
        channel_id = author.voice.channel.id
        voice_channel = discord.utils.get(ctx.guild.voice_channels, id = channel_id)
        voice = discord.utils.get(bot.voice_clients, guild = server)
        if voice is None:
                await voice_channel.connect()
                embed = create_embed(f'Connect to {name_channel}', '')
                await ctx.send(embed = embed)
        voice = discord.utils.get(bot.voice_clients, guild = server)

        url = urlparse(query)
        if (url[1] == 'music.yandex.ru') and ('album' in url[2]):
                album_id = url[2][7:]
                tracks_list = y_musick_start.albums_to_playlist(client, album_id)
                print(album_id)
                embed = create_embed(tracks_list.pop(), "")
                await ctx.send(embed = embed)
                queue_playlist += tracks_list
                check_queue(client, ctx, voice)
        else:
                res = y_musick_start.send_search_request_and_print_result(client, query)
                if res == '-1' or res is None:
                        embed = create_embed("трек не найден", "")
                        await ctx.send(embed = embed)
                        if (len(queue) != 0 or len(queue_playlist) !=0):
                                check_queue(client, ctx, voice)
                else:
                        if ctx.voice_client.is_playing():
                                queue.append(res)
                                embed = create_embed( f'{res[:-3]}', 'добавлено в очередь')
                                await ctx.send(embed = embed)
                        else:
                                #player = direct+str(res)
                                queue.append(res)
                                #print(player)
                                check_queue(client, ctx, voice)
                                #voice.play(discord.FFmpegPCMAudio(executable="ffmpeg.exe", source = player), after = lambda x=0: check_queue(client, ctx, voice))
                                #embed = create_embed('Сейчас играет', f'{res[:-3]}')
                                #await ctx.send(embed = embed)
                        
    @commands.command()
    #async def queue(self, ctx, *, query):
    async def queue(self, ctx):
            global queue, queue_playlist
            if len(queue) == 0:
                    if len(queue_playlist) >= 66:
                            how_parts = int(len(queue_playlist)/66+1)
                            print(how_parts)
                            short_list = []
                            k=0
                            for i in range(len(queue_playlist)):
                                    if k < 66:
                                            short_list.append(queue_playlist[i])
                                            k = k+1
                                    else:
                                            await ctx.send(short_list)
                                            short_list.clear()
                                            k=0
                            await ctx.send(short_list)
                            short_list.clear()
                    else:
                            await ctx.send(queue_playlist)
                    
            elif len(queue_playlist) == 0:
                    await ctx.send(queue)
            elif len(queue) != 0 and len(queue_playlist) != 0:
                    await ctx.send(queue)
                    if len(queue_playlist) >= 66:
                            how_parts = int(len(queue_playlist)/66+1)
                            print(how_parts)
                            short_list = []
                            k=0
                            for i in range(len(queue_playlist)):
                                    if k < 66:
                                            short_list.append(queue_playlist[i])
                                            k = k+1
                                    else:
                                            await ctx.send(short_list)
                                            short_list.clear()
                                            k=0
                            await ctx.send(short_list)
                            short_list.clear()
                    else:
                            await ctx.send(queue_playlist)
            else:
                    embed = create_embed('звуки пустоты', '')
                    await ctx.send(embed = embed)

    @commands.command()
    async def show_playlists(self, ctx):
            global client
            list = y_musick_start.playlists_list(client)
            await ctx.send(list)

    @commands.command()
    async def shuffle(self, ctx):
            global queue, queue_playlist
            if len(queue) != 0:
                    random.shuffle(queue)
            if len(queue_playlist) != 0:
                    random.shuffle(queue_playlist)
            #ctx.send('Skyrim Shuffle complite!')
            embed = create_embed('Skyrim Shuffle complite!', '')
            await ctx.send(embed = embed)
            
    @commands.command()
    async def playlist(self, ctx, *, title_list):

            global client
            await ctx.send(y_musick_start.playlist_info(client, title_list))
            #await ctx.send('При большем количестве треков потребуется время для их извлечения из ЯМ')
            embed = create_embed('ВНИМАНИЕ', 'При большем количестве треков потребуется время для их извлечения из ЯМ')
            await ctx.send(embed = embed)
            
            global queue_playlist
            queue_playlist += y_musick_start.tracks_from_playlist(client, title_list)
            embed = create_embed('Очередь успешно заполнена', '')
            await ctx.send(embed = embed)
            ######тут убрать элементы массивов
            if len(queue_playlist) >= 66:
                    how_parts = int(len(queue_playlist)/66+1)
                    print(how_parts)
                    short_list = []
                    k=0
                    for i in range(len(queue_playlist)):
                            if k < 66:
                                    short_list.append(queue_playlist[i])
                                    k = k+1
                            else:
                                    await ctx.send(short_list)
                                    short_list.clear()
                                    k=0
                    await ctx.send(short_list)
                    short_list.clear()
            else:
                    await ctx.send(queue_playlist)

            

            #коннект к войс каналу
            author = ctx.author
            name_channel = author.voice.channel.name
            channel_id = author.voice.channel.id
            server_id = ctx.guild.id
            server = bot.get_guild(server_id)
            voice_channel = discord.utils.get(ctx.guild.voice_channels, id = channel_id)
            embed = create_embed(f'Connect to {name_channel}', '')
            await ctx.send(embed = embed)
            #await ctx.send(f'Connect to {name_channel}')
            voice = discord.utils.get(bot.voice_clients, guild = server)
            if voice is None:
                    await voice_channel.connect()
            voice = discord.utils.get(bot.voice_clients, guild = server)
            check_queue(client, ctx, voice)
            

                    
    @commands.command()
    async def test(self, ctx, *, title_list):
            await ms_send(ctx, title_list)
            check_queue(client, ctx, title_list)
            
    @commands.command()
    async def volume(self, ctx, volume: int):
        """Changes the player's volume"""
        if ctx.voice_client is None:
                embed = create_embed('Not connected to a voice channel.', '')
                return await ctx.send(embed = embed)
        
 
        ctx.voice_client.source.volume = volume / 100
        embed = create_embed(f"Changed volume to {volume}%", '')
        await ctx.send(embed = embed)
        #await ctx.send(f"Changed volume to {volume}%")

    @commands.command()
    async def loop(self, ctx):
            global is_loop, queue, queue_playlist
            '''
            #if len(queue) == 0 and len(queue_playlist) == 0:
            #        embed = create_embed('LOOPить нечего', '')
            #        await ctx.send(embed = embed)
            #else:        
                    if is_loop == False:
                            is_loop = True
                            embed = create_embed('заLOOPил', '')
                            await ctx.send(embed = embed)
                    else:
                            is_loop = False
                            embed = create_embed('разLOOPил', '')
                            await ctx.send(embed = embed)
                '''
            if is_loop == False:
                    is_loop = True
                    embed = create_embed('заLOOPил', '!НЕДОПИЛ!\nвсе последующие треки будут добавлены в луп')
                    await ctx.send(embed = embed)
            else:
                    is_loop = False
                    embed = create_embed('разLOOPил', '')
                    await ctx.send(embed = embed)

            
    @commands.command()
    async def skip(self, ctx):
            server_id = ctx.guild.id
            server = bot.get_guild(server_id)
            voice = discord.utils.get(bot.voice_clients, guild = server)
            voice_channel = server.voice_client
            voice_channel.stop()
            #embed = create_embed("Скипнул", '')
            #await ctx.send(embed = embed)
            #global queue
            #print(queue)
            #check_queue(client, ctx, voice) 

 
    @commands.command()
    async def stop(self, ctx):
        """Stops and disconnects the bot from voice"""
        global queue, queue_playlist
        queue.clear()
        queue_playlist.clear()
        files = os.listdir(direct)
        await ctx.voice_client.disconnect()
        for i in range(0, len(files)):
                os.remove(direct+files[i])

    @commands.command()
    async def clear(self, ctx):
        """Stops and disconnects the bot from voice"""
        global queue, queue_playlist
        queue.clear()
        queue_playlist.clear()
        await ctx.voice_client.stop()
        files = os.listdir(direct)
        for i in range(0, len(files)):
                os.remove(direct+files[i])
        embed = create_embed('Очередь очищена', '')
        await ctx.send(embed = embed)
        
    @commands.command()
    async def pause(self, ctx):
        global is_pause
        if is_pause == False:
                server = ctx.message.guild
                voice_channel = server.voice_client
                voice_channel.pause()
                is_pause = True

    @commands.command()
    async def resume(self, ctx):
        global is_pause
        if is_pause == True:
                server = ctx.message.guild
                voice_channel = server.voice_client
                voice_channel.resume()
                is_pause = False
        
    @commands.command()
    async def new_channel(self, ctx, *, channel: discord.VoiceChannel):
        """Joins a voice channel"""
        
        embed = create_embed(f'Подрубился к {channel}', '')
        await ctx.send(embed = embed)
        if ctx.voice_client is not None:
            return await ctx.voice_client.move_to(channel)
        await channel.connect()

    @play.before_invoke
    async def ensure_voice(self, ctx):
        if ctx.voice_client is None:
            if ctx.author.voice:
                await ctx.author.voice.channel.connect()
            else:
                await ctx.send("You are not connected to a voice channel.")
                raise commands.CommandError("Author not connected to a voice channel.")
 
    
    
bot = commands.Bot(command_prefix=commands.when_mentioned_or("!"),#Тут можно поменять префикс вашего бота
                   description='Relatively simple music bot example')
 
 
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print('------')

@bot.event
async def ms_send(ctx, embed):
        await ctx.send(embed = embed)

client = y_musick_start.authorization()
bot.add_cog(Music(bot))
bot.run('')#Тут указывает токен вашего бота
