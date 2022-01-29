import asyncio
import ffmpeg
import discord
import os
import random

import y_musick_start
 
from discord.ext import commands


direct = 'tracks\\'
os.mkdir('tracks')

server, server_id, channel_id, voice = None, None, None, None
is_pause = False
queue = []
queue_playlist = []

#def start_check_queue(self, ctx, voice):

#        asyncio.run(check_queue(self, ctx, voice))

def check_queue(self, ctx, voice):
        
                #ms = Music(self.bot)
                #bot = commands.Bot(command_prefix=commands.when_mentioned_or("!"))
                #bot.loop.create_task(Music.ms_send('очередь закончилась'))
                #bot.run("")
                global queue, queue_playlist
                    
                if len(queue) == 0:
                        #ms.ms_send(self, ctx, 'очередь закончилась')
                        #await ctx.send('очередь закончилась')
                        files = os.listdir(direct)
                        for i in range(0, len(files)):
                                os.remove(direct+files[i])
                        print('обычная очередь закончилась')
                        ##
                        res = y_musick_start.send_search_request_and_print_result(queue_playlist[0])
                        print(res)
                        queue_playlist.pop(0)
                        player = direct+res
                        print(player)
                        voice.play(discord.FFmpegPCMAudio(executable="ffmpeg.exe", source = player), after = lambda x=0: check_queue(self, ctx, voice))
                elif len(queue_playlist) == 0:
                        files = os.listdir(direct)
                        for i in range(0, len(files)):
                                os.remove(direct+files[i])
                        return 'очередь закончилась'
                else:
                        print(len(queue))
                        print(queue[0])
                        
                        player = direct+str(queue.pop(0))
                        print(player)
                        voice.play(discord.FFmpegPCMAudio(executable="ffmpeg.exe", source = player), after = lambda x=0: check_queue(self, ctx, voice))
                        #return str(player)
                        #ms.ms_send(ctx, f'Сейчас играет: {player[:-3]}')
                        #ctx.send(f'Сейчас играет: {player[:-3]}')

 
class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
 
   
    @commands.command()
    async def join(self, ctx, *, command =  None):
        """Joins a voice channel"""
        global server, server_id, channel_id, voice, queue
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
        
    
    @commands.command()
    async def play(self, ctx, *, query):
        """Plays a file from the local filesystem"""
        global server, server_id, channel_id, queue, queue_playlist
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

        res = y_musick_start.send_search_request_and_print_result(query)
        if res == '-1' or res is None:
                await ctx.send('трек не найден')
                if (len(queue) != 0 or len(queue_playlist) !=0):
                        check_queue(self, ctx, voice)
        else:
                if ctx.voice_client.is_playing():
                        queue.append(res)
                        await ctx.send(f'{res[:-3]} добавлено в очередь')
                else:
                        player = direct+str(res)
                        print(player)
                        voice.play(discord.FFmpegPCMAudio(executable="ffmpeg.exe", source = player), after = lambda x=0: check_queue(self, ctx, voice))
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
            list = y_musick_start.playlists_list()
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

           
            await ctx.send(y_musick_start.playlist_info(title_list))
            await ctx.send('При большем количестве треков потребуется время для их извлечения из ЯМ')
            
            global queue_playlist
            queue_playlist = y_musick_start.tracks_from_playlist(title_list)
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
            check_queue(self, ctx, voice)
            

                    
    @commands.command()
    async def test(self, ctx):
            global queue
            queue = ['Resonance - Home.mp3']

    @commands.command()     
    async def ms_send(self, ctx, *, query):
            await ctx.send(query)
            
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
            check_queue(self, ctx, voice) 

 
    @commands.command()
    async def stop(self, ctx):
        """Stops and disconnects the bot from voice"""
 
        await ctx.voice_client.disconnect()
        
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
 
bot.add_cog(Music(bot))
bot.run('')#Тут указывает токен вашего бота
