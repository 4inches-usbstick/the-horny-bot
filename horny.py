
import discord
import time
import requests
print('HRN')
crimes = ['horny','assholery','hate','fire','carbon-monoxide','bullshit','illegal','borderline-illegal','excessive','w-t-a-f']
#[being too horny], [being just an asshole], [hateful speech], [starting unnecessacry crap], [drowning in toxcity - especially for debates or discussions - fallacies such as ad hominem], [spreading bullshit]


        
def pull(puller, perp, crime, time):
    f = open('list.txt', 'a')
    if crime in crimes:
        towrite = 'User '+str(perp)+' had the alarm pulled on them for: '+str(crime)+' at '+str(time)+' by user '+str(puller)+'.'
        toreturn = towrite
        f.write(towrite+'\n')
        #await message.channel.send(towrite)
       
        towrite = str(crime)+':'+str(perp)
        f.write(towrite+'\n\n')
        f.close()
        return(toreturn)
        
    elif crime not in crimes:
        #await message.channel.send('This is not a crime.')
        toreturn = 'This is not a valid crime'
        return(toreturn)
        f.close()
    
def stat(person, crime):
    f = open('list.txt', 'r')
    contents = f.read()
    
    str(contents)
    #print(contents)
    
    total = contents.count(str(person))
    crimesa = contents.count(str(crime)+':'+str(person))
    
    int(total)
    
    #await message.channel.send('User '+person+' has had the alarm pulled on them '+total+' times in total and '+crimes+' times for that particular crime.')
    toreturn = 'User '+str(person)+' has had the alarm pulled on them '+str(int(total / 2))+' times in total and '+str(crimesa)+' times for that particular crime.'
   
    f.close()
    return(toreturn)

def find_nth(haystack, needle, n):
    start = haystack.find(needle)
    while start >= 0 and n > 1:
        start = haystack.find(needle, start+len(needle))
        n -= 1
    return start

   
client = discord.Client()

@client.event
async def on_ready():
    print('Ready to go...')
    
@client.event
async def on_message(message):

    z = message.content.split(';')
    
    if z[0] == '$ pull':
        randombullshitoutput = pull(message.author, z[1], z[2], message.created_at)
        await message.channel.send(randombullshitoutput)
        
    if z[0] == '$ stat':
        randombullshitoutput = stat(z[1], z[2])        
        await message.channel.send(randombullshitoutput)        
   
    if z[0] == '$ sa':
        if z[2] == 'admin password':
            await message.channel.send(z[1])
        elif z[2] != 'admin password':
            await message.channel.send('You are forbidden to send messages as me.')
            
    if z[0] == '$ help':
        f = open('who-horny.txt', 'r')
        contents = f.read()
        f.close()
        await message.channel.send(contents)
        
 
    
    
client.run('ya thingy here')
