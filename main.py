import asyncio



async def retur():
    return "LEVEL 50 (GRANDMASTER THEURGIST)"


async def retur2():
    return "ETHAN JADE"

async def main():
    print("""
    Azoth Checker By Lxghtend      
    Credits:
    Milwr - used A LOT of his code in this bot
    Notfaj - helpin as always :3
              """) 
    wizard_name = await retur2()
    wizard =  await retur()
    wizard = wizard.split(' ')
    wizard[3] = wizard[3].replace(')', '') # changes ex. level 160 (prime diviner), to 160 diviner
    name = wizard[0], wizard[1], wizard[3]
    name2 = ' '.join(name)
    wizards = []
    if wizard not in wizards: # if the current wizard is not already in the list
            wizards.append(name2)    # add it
    print(wizard_name, "-", wizard[0], wizard[1], wizard[3])
    print (wizards)
    


asyncio.run(main())