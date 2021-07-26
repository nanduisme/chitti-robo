from discord.ext import commands
import json
import random


class Listener(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.listener_file = 'listener/listener_replies.json'
        self.data = self.get_data()

    @commands.Cog.listener()
    @commands.guild_only()
    async def on_message(self, message):
        guild = str(message.guild.id)

        if message.content.lower() == 'e' and not message.author.bot:
            if message.author.id == 591078175778537512:
                await message.channel.send('Its okay you can say that.')
            else:
                await message.channel.send(f'Shut up {message.author.mention}')
            print(message.guild.id)

        try:
            for key in self.data[guild]['replies']:
                if key in self.data[guild]['active_keys'] and not message.author.bot and self.data[guild]['is_enabled']:
                    if ' ' in key:
                        if key in message.content.lower():
                            await message.channel.send(random.choice(self.data[guild]['replies'][key]))
                    elif ' ' not in key:
                        if key in message.content.lower().split():
                            await message.channel.send(random.choice(self.data[guild]['replies'][key]))
        except:
            pass

    def get_data(self):
        with open(self.listener_file, 'r') as f:
            data = json.load(f)
            return data

    def dump_data(self):
        with open(self.listener_file, 'w') as f:
            json.dump(self.data, f)

    @commands.group(name='listener', invoke_without_command=True)
    @commands.guild_only()
    async def listener(self, ctx):
        guild = str(ctx.guild.id)

        if guild not in self.data:
            self.data[guild] = {
                'replies': {},
                'active_keys':[],
                'is_enabled': True
            }

        self.dump_data()

        await ctx.send('''```Command cannot be invoked without subcommand! 
Use "$listener help" to see all subcommands```''')

    @listener.command(name='add')
    @commands.guild_only()
    async def add_listener(self, ctx, *keys):
        guild = str(ctx.guild.id)
        key = ' '.join(map(str, keys))

        if guild not in self.data:
            self.data[guild] = {
                'replies': {},
                'active_keys':[],
                'is_enabled': True
            }

        with open(self.listener_file, 'w') as f:
            json.dump(self.data, f)

        def check(m):
            return m.author == ctx.author and len(m.content) >= 1

        def yn_check(m):
            return m.author == ctx.author and m.content in ['y', 'n', 'Y', 'N']

        # Get Key
        while True:
            if len(key) < 1:
                await ctx.send('What word/phrase do you want to listen for?')
                key = await self.bot.wait_for('message', check=check)
                key = key.content

            if key in self.data[guild]['replies']:
                await ctx.send(f'Key "{key}" already exists. Would you like to add to it? (y/n)')
            else:
                break

            response = await self.bot.wait_for('message', check=yn_check)
            if response.content.lower() == 'y':
                break
            else:
                await ctx.send('Command Cancelled.')
                return

        # Get Value
        while True:
            await ctx.send('What word/phrase would you like the response to be?')
            value = await self.bot.wait_for('message', check=check)
            value = value.content

            if key in self.data[guild]['replies']:
                if value in self.data[guild]['replies'][key]:
                    await ctx.send(f'Response "{value}" already exists. Would you like to add a different response instead? (y/n)')
                else:
                    break

                response = await self.bot.wait_for('message', check=yn_check)
                if response.content.lower() == 'y':
                    pass
                else:
                    await ctx.send('Command Cancelled.')
                    return
            else:
                break

        # Conformation
        await ctx.send(f'So, you would like the key to be "{key}" and the response to be "{value}"? (y/n)')
        response = await self.bot.wait_for('message', check=yn_check)

        if response.content.lower() == 'y':
            pass
        else:
            await ctx.send('Command Cancelled.')
            return

        try:
            self.data[guild]['replies'][key.lower()].append(value)
        except:
            self.data[guild]['replies'][key.lower()] = [value]
            self.data[guild]['active_keys'].append(key.lower())

        self.dump_data()

        await ctx.send('New key and response added!')

    @listener.command(name='toggle')
    @commands.guild_only()
    async def toggle(self, ctx, *key):
        guild = str(ctx.guild.id)
        key = ' '.join(map(str, key))

        def key_check(m):
            with open(self.listener_file, 'r') as f:
                data = json.load(f)
                return m.author == ctx.author and m.content.lower() in data[guild]['active_keys']

        def yn_check(m):
            return m.author == ctx.author and m.content in ['y', 'n', 'Y', 'N']

        if len(key) < 1:
            await ctx.send('What key would you like to toggle?')
            key = await self.bot.wait_for('message', check=key_check)
            key = key.content.lower()

        if key not in self.data[guild]['replies']:
            await ctx.send(f'```Key "{key}" does not exist :/. Command cancelled```')
            return
        elif key in self.data[guild]['replies']:
            toggle = 'off' if key in self.data[guild]['active_keys'] else 'on'

            await ctx.send(f'`So you would like to toggle {toggle} "{key}"? (y/n)`')
            response = await self.bot.wait_for('message', check=yn_check)

            if response.content.lower() == 'n':
                await ctx.send('`Command cancelled`')
                return
            else:
                if toggle == 'on':
                    self.data[guild]['active_keys'].append(key)
                else:
                    self.data[guild]['active_keys'].remove(key)

        self.dump_data()
        await ctx.send(f'`Key "{key}" has been toggled {toggle}`')

        return

    @listener.command(name='list')
    @commands.guild_only()
    async def show(self, ctx, *key):
        guild = str(ctx.guild.id)

        status = '[ENABLED]' if self.data[guild]['is_enabled'] else '[DISABLED]'

        active_keys = []
        inactive_keys = []
        for key in self.data[guild]['replies']:
            if key in self.data[guild]['active_keys']:
                active_keys.append(key)
            elif key not in self.data[guild]['active_keys']:
                inactive_keys.append(key)

        active_keys_show = ''
        for key in active_keys:
            active_keys_show = active_keys_show + '-> ' + key + '\n'
            for reply in self.data[guild]['replies'][key]:
                active_keys_show = active_keys_show + '    -> ' + reply + '\n'
        inactive_keys_show = ''
        for key in inactive_keys:
            inactive_keys_show = inactive_keys_show + '-> ' + key + '\n'
            for reply in self.data[guild]['replies'][key]:
                inactive_keys_show = inactive_keys_show + '    -> ' + reply + '\n'

        show = f'''***KEYS AND REPLIES {status}***
```ACTIVE KEYS:
{active_keys_show}
INACTIVE KEYS:
{inactive_keys_show}
```        
'''
        await ctx.send(show)

    @listener.command(name='disable')
    @commands.guild_only()
    async def disable(self, ctx):
        guild = str(ctx.guild.id)

        if self.data[guild]['is_enabled']:
            self.data[guild]['is_enabled'] = False
        else:
            await ctx.send('`Listeners are already disabled.`')
            return

        self.dump_data()
        await ctx.send('Listeners have been diabled for this server.')

    @listener.command(name='enable')
    @commands.guild_only()
    async def enable(self, ctx):
        guild = str(ctx.guild.id)

        if not self.data[guild]['is_enabled']:
            self.data[guild]['is_enabled'] = True
        else:
            await ctx.send('`Listeners are already enabled.`')
            return

        self.dump_data()
        await ctx.send('Listeners have been enabled for this server.')

    @listener.command(name='remove')
    @commands.guild_only()
    async def remove(self, ctx, *key):
        guild = str(ctx.guild.id)
        key = ' '.join(map(str, key))

        def key_check(m):
            return m.author == ctx.author

        while True:
            if len(key) < 1:
                await ctx.send('From *what key* would you like to remove a reply?')
                key = await self.bot.wait_for('message', check=key_check)
                key = key.content

            if key not in self.data[guild]['replies']:
                await ctx.send(f'Key "{key}" does not exist. Commands cancelled.')
                return

            break

        replies = [reply for reply in self.data[guild]['replies'][key]]
        show = f'***KEY "{key}":***\n```'
        for reply in replies:
            show += f'{replies.index(reply)+1}- {reply}\n'

        show += '```\n Please enter the number of the reply you would like to remove.'
        await ctx.send(show)

        while True:
            idx = await self.bot.wait_for('message', check=key_check)
            idx = idx.content
            try:
                idx = int(idx)
            except:
                await ctx.send('Please enter a valid serial number')
                continue

            if idx <= len(replies) and idx > 0:
                break
            else:
                await ctx.send('Please enter a valid serial number')

        idx -= 1

        def yn_check(m):
            return m.author == ctx.author and m.content in ['y', 'n', 'Y', 'N']

        await ctx.send(f'So, you would like to remove response "{replies[idx]}" from key "{key}"? (y/n)')

        response = await self.bot.wait_for('message', check=yn_check)
        response = response.content

        if response.lower() == 'n':
            await ctx.send('Command cancelled')
            return

        if len(replies) == 1:
            await ctx.send(f'Response "{replies[idx]}" is the only response in key "{key}", deleting this key will delete the key too. Are you sure? (y/n)')
            response = await self.bot.wait_for('message', check=yn_check)
            response = response.content

            if response.lower() == 'n':
                await ctx.send('Command cancelled')
                return
            
            await ctx.send(f'Key "{key}" and all its response has been deleted.')
            del self.data[guild]['replies'][key]

            self.dump_data()
            return

        self.data[guild]['replies'][key].remove(replies[idx])
        self.dump_data()

        await ctx.send(f'The response has been removed from key "{key}"')

    @listener.command(name='help')
    @commands.guild_only()
    async def hepl(self, ctx):
        show = '''Current list and syntax of subcommands for "listener" : ```
- list
    -Lists out all the keywords and replies on this server.

- add |keyword: optional|
    -Adds a response to keyword or creates a new keyword.

- toggle |keyword: optional|
    -Toggles keywords on and off.

- disable
    -Disables all keywords for this server.

- enable
    -Enables all keywords for this server.

- remove |keyword: optional|
    -Removes a specified response from given keyword
    
All above mentioned commands to be invoked with prefix "$listener " ```'''
        await ctx.send(show)


def setup(bot):
    bot.add_cog(Listener(bot))
