# Imports

import discord
from discord.ext import commands
import json  # To read ask/ask.json file for responses.
from PIL import Image, ImageDraw, ImageFont  # For image manipulation.
import random  # To chose random response and picture.

# Defining colours. Not really necessary but very convenient
BLACK = (0, 0, 0)  # RGB value for black
WHITE = (255, 255, 255)  # RGB value for white
PURPLE = 0x510490  # Hex Value of Purple. '0x' Indicates that it is a hex number and the following numbers depict its value

# Creating a class or an object 'Quoted' for easier use on command call
class Quoted:
    def __init__(self, name, file, x, y, size, color):
        self.name = name  # Name of person
        self.file = file  # File path of image

        # Position size and colour of text
        self.x = x
        self.y = y
        self.size = size
        self.color = color


# Defines a variable for each famous person as an instance of above class
alex_ham = Quoted(
    "Alexander Hamilton", "ask/Images/alexander_hamilton.png", 50, 100, 65, BLACK
)
chinese_emp = Quoted(
    "Random Chinese Emporer", "ask/Images/constantine.png", 75, 100, 75, BLACK
)
disney = Quoted("Walt Disney", "ask/Images/disney.png", 20, 250, 40, BLACK)
dumbledore = Quoted("Albus Dumbledore", "ask/Images/dumbledore.png", 400, 50, 50, WHITE)
edison = Quoted("Thomas Edison", "ask/Images/edison.png", 40, 50, 50, BLACK)
einstien = Quoted("Albert Einstien", "ask/Images/einstien.png", 300, 100, 50, WHITE)
hitler = Quoted("Adolf Hitler", "ask/Images/hitler.png", 50, 50, 60, BLACK)
oogway = Quoted("Master Ooogway", "ask/Images/oogway.png", 350, 25, 40, BLACK)
sachin = Quoted("Sachin Tendulkar", "ask/Images/sachin.png", 200, 25, 40, BLACK)
trump = Quoted("Donald Trump", "ask/Images/trump.png", 350, 25, 40, BLACK)

# Placing all of the people variables in a list for easy looping
people = [
    trump,
    alex_ham,
    chinese_emp,
    disney,
    dumbledore,
    edison,
    einstien,
    hitler,
    oogway,
    sachin,
]

# Above methods can be seen in help.py as well

# Definiing a class for the cog. Mandatory for all Cogs. Name(askCog) is not relevant anywhere except on Line-82 for the setup function.
class askCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot  # Defining bot instance in class

        # Fectching responses and font file location from ask/ask.json using get_data function defined on Line 52
        self.responses = self.get_data()["responses"]
        self.fonts = self.get_data()["fonts"]

    # Defining get_data function to fetch data from ask/ask.json file.
    def get_data(self):
        # The usual or "hard" way to get data from a json file would be
        #   1. f = open('ask/ask.json', 'r')
        #   2. data = json.load(f)
        #   3. close('ask/ask.json')
        # Where "ask/ask.json" being the path to the file to open and " r" being the permission used, which is
        # in this case "read". to edit the file we would need "w" (write) or "a" (append) permission argument.

        # In this function the "with" keyword helps us shorten the above code. It basically closes the file autmatically
        # because it is easy to forget to close a file which can corrupt it.
        with open("ask/ask.json", "r") as f:
            data = json.load(
                f
            )  # Converts the contents of the json file into a python dictionary and stores it in "data"

        return data  # Returns the value of "data" whenever the function is called.

    @commands.command()  # Basically shows the bot that this function is a command.
    async def ask(
        self, ctx, question=None
    ):  # "question" is set to None by default. It is to determine wether a question
        # asked or if it was invoked empty.

        if (
            question is None
        ):  # Runs everything under this if statement is True ie. if there is no question asked.
            embed = discord.Embed(
                title="Ask a question dude.", color=PURPLE
            )  # Defines an embed because well its prettier than messages lol.
            await ctx.reply(
                embed=embed, mention_author=False
            )  # Replies to the message.
            return  # Returns the function so that no further code will be excecuted.

        person = random.choice(people)  # Chooses a random person from list "people"
        quote = (
            '"' + random.choice(self.responses) + '"'
        )  # Same thing but adds quotes ("") to the random response.
        year = random.randint(1200, 2200)  # Random year.
        font = random.choice(self.fonts)  # Chooses random font.
        font = ImageFont.truetype(
            font, person.size
        )  # Initalises font with image manipulation library.
        image = Image.open(person.file)  # Loads image file to edit.
        drawing = ImageDraw.Draw(
            image
        )  # Imagine it like setting up the image on a canvas ready to add some text

        drawing.text(
            (person.x, person.y), quote, font=font, fill=person.color
        )  # Draws the text according to the persons attributes (x, y and colour).
        image.save(
            "ask/Tempquote.png"
        )  # Saves edited image in the folder "ask" (this folder) and in the name "Tempquote.png".
        # NOTE: The "save" funtion overwrites it if a file already exists in the name. So we dont have to delete it after each time.

        output = discord.File(
            "ask/Tempquote.png"
        )  # Initializes the file to discord for sending it in an embed.
        embed = discord.Embed(
            title=f"{person.name.upper()} HAS SPOKEN", description=" ", color=PURPLE
        )  # NOTE: "upper" makes a string uppercase.
        embed.set_image(
            url="attachment://ask/Tempquote.png"
        )  # This is a little workaround for sending a local image because discord embeds usually only allow urls.
        embed.set_footer(text=f"~{person.name}, {year}")

        await ctx.reply(
            file=output, embed=embed, mention_author=False
        )  # Replies to the command with final embed.


# Mandatory setup command for all Cogs.
def setup(bot):
    bot.add_cog(askCog(bot))


# YAY! Thats it for the ask cog. We'll walk through /mth/math.py next :).
