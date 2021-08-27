from discord.ext import commands
from discord.ext.commands.context import Context
import math, statistics

class Cog(commands.Cog):

    '''Simple math commands.'''

    def __init__(self, bot):
        self.bot = bot
        
    async def math(self, nums: list, op: str, ctx: Context):
        nums = await self.convert_list(nums, ctx)

        if nums is None:
            return

        show = (
            ''.join(f'{x} {op} ' for x in nums)[:-3]
            if op in {'+', 'x'}
            else f'{nums[0]} {op} {nums[1]}'
        )

        if op == '+':
            result = sum(nums)
        elif op == '-':
            result = nums[0] - nums[1]
        elif op == '/':
            result = nums[0] / nums[1]

        elif op == 'x':
            result = 1
            for num in nums:
                result *= num
        return show, result

    async def convert_list(self, input: list, ctx: Context):
        try:
            input = list(map(float, input))
            return input
        except:
            await ctx.send(f'Input error! Use `{ctx.prefix}help math {ctx.command}` for help.')
            return

    # Basic Arithmetic Operations

    @commands.command()
    async def add(self, ctx: Context, *nums):

        '''Gives the sum of an infinite number given numbers.'''

        if await self.math(nums, '+', ctx) is None:
            return

        show, result = await self.math(nums, '+', ctx)
        await ctx.send(f'{show} = {result}')

    @commands.command()
    async def sub(self, ctx: Context, *nums):

        '''Gives the differenc of two given numbers.'''

        if await self.math(nums, '-', ctx) is None:
            return
            
        show, result = await self.math(nums, '-', ctx)
        await ctx.send(f'{show} = {result}')

    @commands.command()
    async def mult(self, ctx: Context, *nums):

        '''Gives the product of an infinite number of given numbers.'''

        if await self.math(nums, 'x', ctx) is None:
            return
            
        show, result = await self.math(nums, 'x', ctx)
        await ctx.send(f'{show} = {result}')   
    
    @commands.command()
    async def div(self, ctx: Context, *nums):

        '''Gives the quotient of two given numbers.'''

        if await self.math(nums, '+', ctx) is None:
            return
            
        show, result = await self.math(nums, '+', ctx)
        await ctx.send(f'{show} = {result}')

    # Statistical Measures of Central Tendancies
    @commands.command()
    async def mean(self, ctx: Context, *nums):
    
        '''Gives the arithmetic mean or average of an infinite number of given numbers.'''
    
        if self.convert_list(nums) is None:
            return

        mean = statistics.mean(nums)

        await ctx.send(f'The arithmetic mean of `{nums}` is `{mean}`')

    @commands.command()
    async def median(self, ctx: Context, *nums):
    
        '''Gives the mdian of an infinite list of given numbers.'''
    
        if self.convert_list(nums) is None:
            return

        median = statistics.median(nums)

        nums.sort()

        await ctx.send(f'The median of `{nums}` is `{median}`')

    @commands.command()
    async def mode(self, ctx: Context, *nums):
    
        '''Gives the mode of an infinite list of given numbers.'''
    
        if self.convert_list(nums) is None:
            return

        mode = statistics.mode(nums)

        await ctx.send(f'The mode of the list `{nums}` is `{mode}` occuring `{nums.count(mode)}` number of times.')


def setup(bot):
    bot.add_cog(Cog(bot))