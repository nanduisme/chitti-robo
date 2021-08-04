import discord
from discord.ext import commands
import json
from PIL import Image, ImageDraw, ImageFont
import random

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
PURPLE = 0x510490


class Quoted:
    def __init__(self, name, file, x, y, size, color):
        self.name = name 
        self.file = file
        self.x = x
        self.y = y
        self.size = size
        self.color = color

alex_ham = Quoted('Alexander Hamilton', 'ask/Images/alexander_hamilton.png', 50, 100, 65, BLACK)
chinese_emp = Quoted('Random Chinese Emporer', 'ask/Images/constantine.png', 75, 100, 75, BLACK)
disney = Quoted('Walt Disney', 'ask/Images/disney.png', 20, 250, 40, BLACK)
dumbledore = Quoted('Albus Dumbledore', 'ask/Images/dumbledore.png', 400, 50, 50, WHITE)
edison = Quoted('Thomas Edison', 'ask/Images/edison.png', 40, 50, 50, BLACK)
einstien = Quoted('Albert Einstien', 'ask/Images/einstien.png', 300, 100, 50, WHITE)
hitler = Quoted('Adolf Hitler', 'ask/Images/hitler.png', 50, 50, 60, BLACK)
oogway = Quoted('Master Ooogway', 'ask/Images/oogway.png', 350, 25, 40, BLACK)
sachin = Quoted('Sachin Tendulkar', 'ask/Images/sachin.png', 200, 25, 40, BLACK)
trump = Quoted('Donald Trump', 'ask/Images/trump.png', 350, 25, 40, BLACK)

people = [trump, alex_ham, chinese_emp, disney, dumbledore, edison, einstien, hitler, oogway, sachin]

class askCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.responses = self.get_data()['responses']
        self.fonts = self.get_data()['fonts']

    def get_data(self):
        with open('ask/ask.json', 'r') as f:
            data = json.load(f)
        return data

    @commands.command()
    async def ask(self, ctx, question=None):
        if question is None:
            embed = discord.Embed(title='Ask a question dude.', color=PURPLE)
            await ctx.reply(embed=embed, mention_author=False)
            return

        person = random.choice(people)
        quote = '"'+random.choice(self.responses)+'"'
        year = random.randint(1200, 2200)
        font = random.choice(self.fonts)
        font = ImageFont.truetype(font, person.size)
        image = Image.open(person.file)
        drawing = ImageDraw.Draw(image)
        
        drawing.text((person.x, person.y), quote, font=font, fill=person.color)
        image.save("ask/Tempquote.png")

        output = discord.File('ask/Tempquote.png')
        embed = discord.Embed(title=f'{person.name.upper()} HAS SPOKEN', description=' ', color=PURPLE)
        embed.set_image(url='attachment://ask/Tempquote.png')
        embed.set_footer(text=f'~{person.name}, {year}')

        await ctx.reply(file=output, embed=embed, mention_author=False)


def setup(bot):
    bot.add_cog(askCog(bot))
