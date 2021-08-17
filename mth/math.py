from discord.ext import commands

class Math(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='add') # The keyword argument, "name='add'", is not necessary in this case as the 
    # code autmatically recognises the name of the command as the name of the function if it is not mentioned.
    async def add(self, ctx, *nums):
        # The "self" argument is for passing the class itself as an argument to use this function as an attribute of the class
        # The "ctx" argument passes the context of a message which has attributes such as, "ctx.author", "ctx.content", "ctx.guild" etc.
        # NOTE: A guild is just a discord server, its just how they use it in this library. So guild=server. 
        # It also contains methods like "ctx.send(message)", "ctx.reply(message)" and many more.
        # The "*nums" argument catches all the given inputs irregardles of count and puts them all in a list named "nums".

        try: # Tries to excecute certain block of code and if it throws an error it excucutes the "except: " part. Here in Line 18
            nums = [float(num) for num in nums] # Tries to turn all the numbers in nums to a floating point number.
        except:
            # Exrcutes the following ONLY IF the above try rasies an error.
            await ctx.send('Input error. Command cancelled.')
            return 

        # Defining empty variables to assign values to in the future.
        sum = 0
        show = ''

        # Looping through nums and adding them into 
        for x in nums:
            sum += x # Adds every number to "sum", which makes "sum" the sum of all numbers in "nums by the end."
            show += f'{str(x)} + ' # Adds the number in string form for displaying as a result.

        await ctx.send(f'{show[:-2]} = {sum}') # Displays the results.

    @commands.command(name='mult')
    async def mult(self, ctx, *nums):
        try:
            nums = [float(num) for num in nums]
        except:
            await ctx.send('Input error. Command cancelled.')
            return

        product = 1
        show = ''
        for x in nums:
            product *= x
            show += f'{str(x)} x '

        await ctx.send(f'{show[:-2]} = {product}')

    @commands.command(name='subtract')
    async def sub(self, ctx, first:float=None, second:float=None): # Takes in two arguments and sets them to None as default 
        if first is None or second is None: # Excecuted when any one of the numbers are not given 
            await ctx.send('Please input 2 values. For eg: `$subtract 2 3`')
        else: 
            total = first - second # Subtracts the numbers inputted. 
            await ctx.send(f'{first} - {second} = {total}') # Sends the the result.

    @commands.command(name='div')
    async def div(self, ctx, first:int=None, second:int=None):
        if first is None or second is None:
            await ctx.send('Please input 2 values. For eg: `$div 2 3`')
        else:
            total = first / second
            await ctx.send(f'{first} / {second} = {total}')

    def sort_numlist(self, nums: list):
        # This is a sorting algorithm I created for the median command.
        # It takes in a list "nums" and returns it sorted

        # NOTE: This is NOT a command. Just a function.

        sorted_list = [] # Initialize an empty list to return at the end.
        for num in nums: # Loops through numbers in list, "nums".
            # This function checks for every element in 'sorted_list' and determines wether to add "num" to
            # the left of the element or right. 
            # Returns a tuple like, (Should add to left[if false then adds to right], Index of where to add).

            def check(sorted_list=sorted_list, num=num):  
                for x in sorted_list:
                    last = len(sorted_list)-1
                    if num <= x:
                        return (True, sorted_list.index(x))
                    elif num >= sorted_list[last] and x == sorted_list[last]:
                        return (False, sorted_list.index(x))

            # Distributes the tuple between "to_insert" and "idx"
            to_insert, idx = check() if len(sorted_list) != 0 else (0, 0)

            # Simply adds to "sorted_list" if it is empty.
            if len(sorted_list) == 0:
                sorted_list.append(num)

            # Checks wether to add to left or right and does so.
            elif to_insert:
                sorted_list.insert(idx, num)
            elif not to_insert:
                sorted_list.append(num)

        return sorted_list # Returns sorted list.

    @commands.command()
    # Accepts a list of nums through "*nums" to find the average.
    async def mean(self, ctx, *nums):
        try: # Similar to the "try" in add and mult
            nums = [float(num) for num in nums]
        except:
            await ctx.send('Input error. Command cancelled.')
            return

        mean = sum(nums)/float(len(nums)) # Finds the mean of the list.

        await ctx.send(f'The mean of `{nums}` is : `{mean}`') # Sends the mean as a message.

    @commands.command()
    async def median(self, ctx, *nums):
        try: # Same thing here too
            nums = [float(num) for num in nums]
        except:
            await ctx.send('Input error. Command cancelled.')
            return

        sorted_nums = self.sort_numlist(nums) # Sorts nums with "sort_numlist".

        # Following if statements checks wether the number of elements is even or odd and takes action accordinly.
        # NOTE: idx means index as in the location of the element in the list.

        if len(sorted_nums)%2 == 1: 
            idx = int((len(sorted_nums)+1)/2)-1
            median = sorted_nums[idx]
        else:
            idx1 = int((len(sorted_nums)+1)/2)-1
            idx2 = int((len(sorted_nums))/2)-1
            median = (sorted_nums[idx1]+sorted_nums[idx2])/2

        await ctx.send(f'The median of `{sorted_nums}` is : `{median}`.')

    @commands.command()
    async def mode(self, ctx, *nums):  
        try: # Still same
            nums = [float(num) for num in nums]
        except:
            await ctx.send('Input error. Command cancelled.')
            return

        modes = []
        for num in nums:
            count = 0
            for element in nums:
                if num == element:
                    count += 1

                    if not modes:
                        modes.append([num, count])

                    else:
                        for mode in modes:
                            m = [m[0] for m in modes]
                            if count >= mode[1]:
                                if num in m:
                                    modes[m.index(num)][1] = count
                                    for e in modes:
                                        if count > e[1]:
                                            modes.remove(e)
                                elif [num, count] not in modes:
                                    modes.append([num, count])
        count = modes[0][1]
        modes = [mode[0] for mode in modes]
        many = '(s)' if len(modes) > 1 else ''
        modes = modes[0] if len(modes) == 1 else [mode for mode in modes]

        await ctx.send(f'The mode{many} of `{self.sort_numlist(nums)}` is : `{modes}`. Occuring at a total of `{count}` times in the given data.')

def setup(bot):
    bot.add_cog(Math(bot))