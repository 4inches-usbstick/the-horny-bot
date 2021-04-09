
import discord
import time
import requests
import random
import configparser
import asyncio
print('HRN')
crimes = ['horny','assholery','hate','fire','carbon-monoxide','bullshit','illegal','borderline-illegal','excessive','w-t-a-f']
#[being too horny], [being just an asshole], [hateful speech], [starting unnecessacry crap], [drowning in toxcity - especially for debates or discussions - fallacies such as ad hominem], [spreading bullshit]

configurationparser = configparser.ConfigParser()

try: configurationparser.read("main.cfg")
except configparser.Error: print("unable to load config!")

bottoken = configurationparser["security"]["token"]
textenginehost = configurationparser["textengine"]['host']
default_to = int(configurationparser["textengine"]["timeout"])

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
    
def traceroute(username):
    f = open('horny-dns.txt', 'r')
    fds = f.read()
    f.close()
    if username+':' in fds:
        offset1 = fds.find(username+':')
        offset2 = fds.find(';', offset1)
        dnslookup = fds[offset1:offset2]
        dnslookupl = dnslookup.split(':')
        return dnslookupl[1]
    else:
        return 'Lookup failed! Could not find user'

intents = discord.Intents.default()
if configurationparser["security"]["open_pgi"] == 'True':
    yee = True
else:
    yee = False
intents.members = yee
client = discord.Client(intents=intents)
#client = discord.Client()


async def poller(z, channeldes, msg):
    global configurationparser, textenginehost, default_to
    ok = 1
    numberofoptionsandtime = str(z[2]).split(':')
    channel = client.get_channel(channeldes)

    rint_cb = str(random.randint(10000, 99999))
        
    offset = find_nth(msg, ';', 2)
        #await message.channel.send(msg[offset:])
        
    if ' ' in msg[offset:len(msg) - 2]:
        await channel.send('No whitespaces are allowed within the poll options')
        ok = 0
        return 0
        
    if ok == 1:
        await channel.send('Attempting to open Chatbox: voting-tmp'+rint_cb)
            
        try:
            f = requests.get('http://' + textenginehost + '/textengine/sitechats/newchat_integration.php?newname=voting-tmp'+rint_cb+'&option=l&rurl=norefer', timeout=default_to)
        except:
            await channel.send(':no_entry_sign: Connection timed out - users will not be able to vote for the poll')
            return 0
                
        
        await channel.send('POLL: '+z[1])
        
        qty = int(numberofoptionsandtime[0])
        options = []
        
        while qty > 0:
            await channel.send(z[qty + 2] + ' - ' + 'http://' + textenginehost + '/textengine/sitechats/sendmsg_integration.php?write=voting-tmp'+rint_cb+'&msg='+z[qty+2]+'&encoderm=UTF-8&namer=vote-&rurl=norefer')
            options.append(z[qty + 2])
            qty -= 1
            
        await asyncio.sleep(int(numberofoptionsandtime[1]))
        await channel.send('Polling has closed. Counting results...')
        try:
            f = requests.get('http://' + textenginehost + '/textengine/sitechats/voting-tmp'+rint_cb, timeout=default_to)
            g = f.text
            
            for i in options:
                instances = g.count(i)
                await channel.send('Option **'+i+'** got **'+str(instances)+'** votes.')
        except:
                await channel.send(':no_entry_sign: Connection timed out')
                return 0
                
                
        if configurationparser["textengine"]["uid_ukey"] != 'use':
            try:
                print('not uidukey')
                f = requests.get('http://' + textenginehost + '/textengine/sitechats/terminalprocess.php?cmd=del&params=voting-tmp'+rint_cb+'&pass='+configurationparser["textengine"]["textengine_password"])
                #await channel.send(f.text)
                await channel.send('Chatbox closed')
                print('http://' + textenginehost + '/textengine/sitechats/terminalprocess.php?cmd=del&params=voting-tmp'+rint_cb+'&pass='+configurationparser["textengine"]["textengine_password"])
            except:
                await channel.send(':no_entry_sign: Connection timed out - failed to send DEL command')
                return 0
        if configurationparser["textengine"]["uid_ukey"] == 'use':
            try:
                print('uidukey')
                len('http://' + textenginehost + '/textengine/sitechats/terminalprocess.php?cmd=del&params=voting-tmp'+rint_cb+'&uid='+configurationparser["textengine"]["textengine_uid"]+'&ukey='+configurationparser["textengine"]["textengine_ukey"])
                f = requests.get('http://' + textenginehost + '/textengine/sitechats/terminalprocess.php?cmd=del&params=voting-tmp'+rint_cb+'&uid='+configurationparser["textengine"]["textengine_uid"]+'&ukey='+configurationparser["textengine"]["textengine_ukey"])
            #await channel.send(f.text[:1999])
                await channel.send('Chatbox closed (UID/UKEY)')
            except:
                await channel.send(':no_entry_sign: Connection timed out - failed to send DEL command (UID/UKEY)')
                return 0

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
        if traceroute(z[1]) != 'Lookup failed! Could not find user':
            await message.channel.send('resolved name **'+z[1]+'** to **'+traceroute(z[1])+'**')
            z[1] = traceroute(z[1])        
            randombullshitoutput = pull(message.author, z[1], z[2], message.created_at)
            await message.channel.send(randombullshitoutput)
        else:
            randombullshitoutput = pull(message.author, z[1], z[2], message.created_at)
            await message.channel.send(randombullshitoutput)
        
    if z[0] == '$ stat':
        if traceroute(z[1]) != 'Lookup failed! Could not find user':
            await message.channel.send('resolved name **'+z[1]+'** to **'+traceroute(z[1])+'**')
            z[1] = traceroute(z[1])
            randombullshitoutput = stat(z[1], z[2])        
            await message.channel.send(randombullshitoutput)        
        else:
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
        if traceroute(z[2]) != 'Lookup failed! Could not find user':
            await message.channel.send('resolved name **'+z[2]+'** to **'+traceroute(z[2])+'**')
            z[2] = traceroute(z[2])
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
    
    if z[0] == '$ registerns':
        if float(z[3]) == float(curpp):
            f = open('horny-dns.txt', 'a')
            f.write(z[1] + ':' + z[2] + ':;\n')
            f.close()
            await message.channel.send('Registered name.')
        else:
            await message.channel.send('Error: invalid key')
        
    if z[0] == '$ log':
        f = open('list.txt', 'r')
        contents = f.read()
        f.close()
        await message.author.send(contents)
        await message.channel.send('User has requested a copy of list.txt - check DM')
        
    if z[0] == '$ nslookup':
        f = open('horny-dns.txt', 'r')
        contents = f.read()
        f.close()
        await message.author.send(contents)
        await message.channel.send('User has requested a copy of horny-dns.txt - check DM')
    
    if z[0] == '$ cgu':
        if not bool(configurationparser["security"]["open_pgi"]):
            await message.channel.send('fatal: priviledged intents not set, cannot continue execution')
            return 100
        xmsg = message.guild.members
        if '<user>' not in str(z[1]):
            await message.channel.send('You need to include <user> somewhere to construct a message')
            return 0
        ids = []
        for i in xmsg:
            ids.append(i.id)
        index = random.randint(0, len(xmsg) - 1)
        mention = "<@"+str(ids[index])+">"
        try:
            messag = str(z[1]).replace('<user>', mention)
            await message.channel.send(messag)
        except IndexError:
            await message.channel.send(mention)

    if z[0] == '$ cgu-noping':
        if not bool(configurationparser["security"]["open_pgi"]):
            await message.channel.send('fatal: priviledged intents not set, cannot continue execution')
            return 100
        
        xmsg = message.guild.members
        ids = []
        for i in xmsg:
            ids.append(i.id)
        index = random.randint(0, len(xmsg) - 1)
        mention = "<User ID "+str(ids[index])+">"
        if '<user>' not in str(z[1]):
            await message.channel.send('You need to include <user> somewhere to construct a message')
            return 0
        try:
            messag = str(z[1]).replace('<user>', mention)
            await message.channel.send(messag)
        except IndexError:
            await message.channel.send(mention)
        
    if z[0] == '$ ping':
        await message.channel.send('Bot latency: {0}'.format(round(client.latency, 1)))
        
        try:
            awa = requests.get('http://' + textenginehost + '/textengine/sitechats/sendmsg_integration.php?preventcache=' + str(random.randint(100, 999)), timeout=default_to)
            await message.channel.send('CBE server response time: '+str(awa.elapsed))
        except:
            await message.channel.send('CBE server is dead.')

    if message.content.startswith('$ poll'):
        z = message.content.split(";")
        print(type(message.channel.id))
        await poller(z, message.channel.id, message.content)

        
try:
    client.run(bottoken)
except:
    input('Unable to start bot, check if priviledged intents are enabled for this bot')
