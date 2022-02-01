import asyncio
import ffmpeg
import discord
import os
import random
from urllib.parse import urlparse

import y_musick_start
 
from discord.ext import commands

#d49ed4
#embed = discord.Embed(title="", description="", colour=0xD49ED4)
direct = 'tracks\\'
if os.path.exists(direct) == False:
        os.mkdir('tracks')

server, server_id, channel_id, voice, client = None, None, None, None, None
is_pause = False
tasks = list()
queue = []
queue_playlist = []


def check_queue(client, ctx, voice):
        
                global queue, queue_playlist, tasks
                
                async def redirect(ctx, mess):
                        await ms_send(ctx, mess)
                        
                
                if len(queue) == 0:
                        files = os.listdir(direct)
                        for i in range(0, len(files)):
                                os.remove(direct+files[i])
                        #print('обычная очередь закончилась')
                        ##
                        #if len(queue_playlist) <= queue_pl_k:
                        #       queue_pl_k = 0
                        if len(queue_playlist) !=0:
                                res = y_musick_start.send_search_request_and_print_result(client, queue_playlist[0])
                                print(res)
                                queue_playlist.pop(0)
                                player = direct+res
                                #print(player)
                                voice.play(discord.FFmpegPCMAudio(executable="ffmpeg.exe", source = player), after = lambda x=0: check_queue(client, ctx, voice))
                                #await ms_send(ctx, f'{player[:-3]}')
                                loop = asyncio.get_event_loop()
                                future = loop.run_until_complete('future').create_task(redirect(ctx, f'{res[:-3]}'))
                                #loop.run_until_complete('future').create_task(redirect(ctx, f'{res[:-3]}'))
                                while future.is_running():
                                        print("луп крутится")
                                
                        else:
                                files = os.listdir(direct)
                                for i in range(0, len(files)):
                                        os.remove(direct+files[i])
                else:
                        #print(len(queue))
                        print(queue[0])
                        
                        player = direct+str(queue.pop(0))
                        #print(player)
                        voice.play(discord.FFmpegPCMAudio(executable="ffmpeg.exe", source = player), after = lambda x=0: check_queue(client, ctx, voice))
                        asyncio.get_running_loop().run_until_complete('future').create_task(redirect(ctx, f'{res[:-3]}'))
                
                
                '''
                elif len(queue_playlist) == 0:
                        files = os.listdir(direct)
                        for i in range(0, len(files)):
                                os.remove(direct+files[i])
                        #return 'очередь закончилась'
                else:
                        print(len(queue))
                        print(queue[0])
                        
                        player = direct+str(queue.pop(0))
                        print(player)
                        voice.play(discord.FFmpegPCMAudio(executable="ffmpeg.exe", source = player), after = lambda x=0: check_queue(client, ctx, voice))
                        asyncio.get_running_loop().create_task(redirect(ctx, f'{player[:-3]}'))
                        #await ms_send(ctx, f'{player[:-3]}')
                        #return str(player)
                        #ms.ms_send(ctx, f'Сейчас играет: {player[:-3]}')
                        #ctx.send(f'Сейчас играет: {player[:-3]}')
                '''
 
class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
 
   
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
        embed = discord.Embed(title="Join", description=f"Connect to {name_channel}", colour=0xD49ED4)
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
                await ctx.send(f'Connect to {name_channel}')
        voice = discord.utils.get(bot.voice_clients, guild = server)

        url = urlparse(query)
        if (url[1] == 'music.yandex.ru') and ('album' in url[2]):
                album_id = url[2][7:]
                tracks_list = y_musick_start.albums_to_playlist(client, album_id)
                print(album_id)
                await ctx.send(tracks_list.pop())
                queue_playlist += tracks_list
                check_queue(client, ctx, voice)
        else:
                res = y_musick_start.send_search_request_and_print_result(client, query)
                if res == '-1' or res is None:
                        await ctx.send('трек не найден')
                        if (len(queue) != 0 or len(queue_playlist) !=0):
                                check_queue(client, ctx, voice)
                else:
                        if ctx.voice_client.is_playing():
                                queue.append(res)
                                await ctx.send(f'{res[:-3]} добавлено в очередь')
                        else:
                                player = direct+str(res)
                                print(player)
                                voice.play(discord.FFmpegPCMAudio(executable="ffmpeg.exe", source = player), after = lambda x=0: check_queue(client, ctx, voice))
                                await ctx.send(f'Сейчас играет: {res[:-3]}')
                        
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
                    await ctx.send('звуки пустоты')
            #res = y_musick_start.send_search_request_and_print_result(query)
            #print(res)
            #if res == '-1':
            #        await ctx.send('трек не найден')
            #else:
            #        queue.append(res)
            #        await ctx.send(f'{res[:-3]} добавлено в очередь')

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
            await ctx.send('Skyrim Shuffle complite!')
            
    @commands.command()
    async def playlist(self, ctx, *, title_list):

            global client
            await ctx.send(y_musick_start.playlist_info(client, title_list))
            await ctx.send('При большем количестве треков потребуется время для их извлечения из ЯМ')
            
            global queue_playlist
            queue_playlist += y_musick_start.tracks_from_playlist(client, title_list)
            await ctx.send('Очередь успешно заполнена')
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
            await ctx.send(f'Connect to {name_channel}')
            voice = discord.utils.get(bot.voice_clients, guild = server)
            if voice is None:
                    await voice_channel.connect()
            voice = discord.utils.get(bot.voice_clients, guild = server)
            check_queue(client, ctx, voice)
            

                    
    @commands.command()
    async def test(self, ctx, *, title_list):
            await ms_send(ctx, title_list)
            check_queue(client, ctx, title_list)

    #@commands.command()     
    #async def ms_send(self, ctx, *, query):
    #        await ctx.send(query)
            
    @commands.command()
    async def volume(self, ctx, volume: int):
        """Changes the player's volume"""
        if ctx.voice_client is None:
                return await ctx.send("Not connected to a voice channel.")
 
        ctx.voice_client.source.volume = volume / 100
        await ctx.send(f"Changed volume to {volume}%")
        
    @commands.command()
    async def skip(self, ctx):
            server_id = ctx.guild.id
            server = bot.get_guild(server_id)
            voice = discord.utils.get(bot.voice_clients, guild = server)
            voice_channel = server.voice_client
            voice_channel.stop()
            check_queue(client, ctx, voice) 

 
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
        await ctx.send('Очередь очищена')
        
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
        await ctx.send(channel)
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
async def ms_send(ctx, query):
        await ctx.send(query)

client = y_musick_start.authorization()
bot.add_cog(Music(bot))
bot.run('NzE5OTgyOTQzODQ1NzQ0NzEw.Xt_WXg.IoHwMZbqTZZEXRH6QC0m4lh5enk')#Тут указывает токен вашего бота
