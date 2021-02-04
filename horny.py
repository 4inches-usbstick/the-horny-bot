
import discord
import time
import requests
import random
print('HRN')
crimes = ['horny','assholery','hate','fire','carbon-monoxide','bullshit','illegal','borderline-illegal','excessive','w-t-a-f']
#[being too horny], [being just an asshole], [hateful speech], [starting unnecessacry crap], [drowning in toxcity - especially for debates or discussions - fallacies such as ad hominem], [spreading bullshit]




        
def pull(puller, perp, crime, time):
    f = open('list.txt', 'a')
    if crime in crimes:
        towrite = 'User '+str(perp)+' had the alarm pulled on them for: '+str(crime)+' at '+str(time)+' by user '+str(puller)+'.'
        toreturn = towrite
        #f.write(towrite+'\n')
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
    toreturn = 'User '+str(person)+' has had the alarm pulled on them '+str(total)+' times in total and '+str(crimesa)+' times for that particular crime.'
   
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
    global curpp
    curpp = random.random()
    print(curpp)
    
@client.event
async def on_message(message):
    global curpp

    z = message.content.split(';')
    if z[0] == '$ pull':
        randombullshitoutput = pull(message.author, z[1], z[2], message.created_at)
        await message.channel.send(randombullshitoutput)
        
    if z[0] == '$ stat':
        randombullshitoutput = stat(z[1], z[2])        
        await message.channel.send(randombullshitoutput)        
   
    if z[0] == '$ sa':
        if float(z[2]) == float(curpp):
            await message.channel.send(z[1])
            curpp = random.random()
            curpp = float(curpp)
            print(curpp)
        elif float(z[2]) != float(curpp):
            await message.channel.send('Error: invalid key')
            curpp = random.random()
            curpp = float(curpp)
            print(curpp)
            
    if z[0] == '$ unpull':
        if float(z[1]) == float(curpp):
            f = open('list.txt', 'r')
            contents = f.read()
            f.close()
            offset0 = contents.find(z[2])
            offset1 = int(len(z[2])) + offset0
            #remote_contents = contents[offset0:offset1]
            halfbefore = contents[:offset0]
            halfafter = contents[offset1:]
            
            if offset0 != -1:
                f = open('list.txt','w')
                f.write(halfbefore)
                f.write('ACTIVATION OVERWRITE')
                f.write(halfafter)
                f.close()
                await message.channel.send('Horny activation at '+str(offset0)+'-'+str(offset1)+' was erased ')
                #await message.channel.send(z[1])
                curpp = random.random()
                curpp = float(curpp)
                print(curpp)
            else:
                await message.channel.send('Error: Substring not found within string')
                await message.channel.send(z[1])
                curpp = random.random()
                curpp = float(curpp)
                print(curpp)
        else:
            await message.channel.send('Error: invalid key')
            await message.channel.send(z[1])
            curpp = random.random()
            curpp = float(curpp)
            print(curpp)
            
    if z[0] == '$ help':
        f = open('who-horny.txt', 'r')
        contents = f.read()
        f.close()
        await message.channel.send(contents)
        
    if z[0] == '$ log':
        f = open('list.txt', 'r')
        contents = f.read()
        f.close()
        await message.author.send(contents)
        await message.channel.send('User has requested a copy of list.txt - check DM')
        
    if z[0] == '$ ping':
        await message.channel.send('Bot latency: {0}'.format(round(client.latency, 1)))
        
        try:
            awa = requests.get('http://71.255.240.10:8080/textengine/sitechats/sendmsg_integration.php', timeout=15)
            await message.channel.send('CBE server response time: '+str(awa.elapsed))
        except:
            await message.channel.send('CBE server is dead.')
        

        
        
    if z[0] == '$ poll':
        ok = 1
        msg = message.content
        str(msg)
        
        offset = find_nth(msg, ';', 2)
        #await message.channel.send(msg[offset:])
        
        if ' ' in msg[offset:len(msg) - 2]:
            await message.channel.send('No whitespaces are allowed within the poll options')
            ok = 0
        
        if ok == 1:
            await message.channel.send('Attempting to open Chatbox... (all other commands will be suspended during this procedure)')
            
            try:
                f = requests.get('http://71.255.240.10:8080/textengine/sitechats/newchat_integration.php?newname=voting-tmp&option=l&rurl=norefer', timeout=15)
            except:
                await message.channel.send(':no_entry_sign: Connection timed out - users will not be able to vote for the poll')
                
            await message.channel.send('POLL: '+z[1])
        
            qty = int(z[2])
            options = []
        
            while qty > 0:
                await message.channel.send(z[qty + 2] + ' - ' + 'http://71.255.240.10:8080/textengine/sitechats/sendmsg_integration.php?write=voting-tmp&msg='+z[qty+2]+'&encoderm=UTF-8&namer=vote-&rurl=norefer')
                options.append(z[qty + 2])
                qty = qty - 1
            
            time.sleep(6)
            await message.channel.send('Polling has closed. Counting results...')
            try:
                f = requests.get('http://71.255.240.10:8080/textengine/sitechats/voting-tmp', timeout=15)
                g = f.text
            
                for i in options:
                    instances = g.count(i)
                    await message.channel.send('Option **'+i+'** got **'+str(instances)+'** votes.')
            except:
                await message.channel.send(':no_entry_sign: Connection timed out')
                
                
        f = requests.get('http://71.255.240.10:8080/textengine/sitechats/terminalprocess.php?cmd=del&params=voting-tmp&pass=hubhogjingobone&key=hubhogjingobone')
        await message.channel.send(f.text)
    
    
client.run('bot token')
