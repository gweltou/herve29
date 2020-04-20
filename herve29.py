import sys
import os
import random
import socket
import requests
import time
import re


class Bot(object):
    
    def __init__(self):  
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        
    def run(self):
        step = 0
        while True:
            data = self.get_text()
            if data:
                print(data)
                if data.startswith("PING"):
                    pong = "PONG {}\n".format(data.split()[1])
                    self.sock.send(pong.encode("utf-8")) 
                
                m = re.match(r":(.+)!.+PRIVMSG #(.+) :(.*)", data)
                if m:
                    sender = m.group(1)
                    dest = m.group(2)
                    msg = m.group(3)
                    if self.pseudo in msg:
                        self.direct_answer(sender)
                        
                    elif random.random() < 0.06:
                        self.random_answer(sender)
                        step = 0
                m = re.match(r":(.+)!.+JOIN #(.+)", data)
                if m:
                    sender = m.group(1)
                    dest = m.group(2)
                    if sender != self.pseudo:
                        self.say_hi(sender)
                
            if step > 10 and random.random() < 0.07:
                self.say_quote()
                step = 0
            
            step += 1
            time.sleep(2)
    
    
    def say_hi(self, name):
        messages = [f"Salut {name}",
                    f"Salut {name}, ça roule ?",
                    f"Hey {name}, la forme ?",
                    f"Salut {name}, ça fait plaiz de te voir !",
                    f"Salut {name}, quoi de 9 ?",
                   ]
        self.send(random.choice(messages))
    
    
    def direct_answer(self, sender):
        messages = [f"oui",
                    f"oui {sender}",
                    f"jamais de la vie !",
                    f"non",
                    f"mouais",
                    f"Merci",
                    f"chépa",
                    f"<3",
                    f"ben ouais !",
                    f"pas du tout",
                    f"hein ?",
                    f"quoi ?",
                    f"Quoi {sender} ?",
                    f"Ça me touche {sender}...",
                    f"Tu le penses vraiment {sender} ?",
                    f"Pourquoi ?",
                    f"Tu me parles ?",
                    f"Franchement, j'en sais rien {sender}",
                    f"Pardon ?",
                    f"Plaît-il ?",
                    f"Ben je sais pas, tu choisis",
                    f"Excuse-moi {sender}, je t'écoutais pas...",
                   ]
        self.send(random.choice(messages))
       
                                     
    def random_answer(self, sender):
        messages = [f"Ouais, c'est pas faux {sender}",
                    f"Bien dit {sender} !",
                    f"T'es vraiment sûr de ce que tu racontes {sender} ?",
                    f"J'aurais pas dit mieux !",
                    f"D'accord avec toi {sender}",
                    f"Hmmm...",
                    f"Wahou, tu m'épates {sender} !",
                    f"Impressionant !",
                    f"Quelle tristesse...",
                    f"Il dit qu'il voit pas le rapport",
                    f"C'est pas faux",
                    f"Ah oui ?",
                    f"Ah ben super...",
                    f"Sérieux ??!",
                    f"Hahahah",
                    f"C'est ouf !",
                    f"J'ai loupé qq chose ?",
                    f"J'adhère !",
                    f"Tu me plais {sender} !",
                    f"Ah si j'avais su...",
                    f"Naaaan...",
                    f"Pas croyap'",
                    f"Tu me fais marrer {sender} ^^",
                    f";-)",
                    f"Ça ressemble un peu à ce que j'ai vécu {sender}",
                    f"Tu m'épates {sender}",
                    f"yep",
                    f"Dingue !",
                    f"lol",
                    f"mdr",
                    f"ptdr :D",
                    f"Pas mal ! :D",
                    f"Carrément",
                    f"ça peut etre vu comme ça {sender} ;)",
                    f"Hahaha, vous êtes cons ! XD",
                    f"J'avais encore jamais entendu un truc pareil {sender}",
                    f"Comme quoi...",
                   ]
        self.send(random.choice(messages))
    

    def send(self, msg):
        self.sock.send(f"PRIVMSG {self.channel} :{msg}\n".encode("utf-8"))


    def connect(self, server, channel, pseudo):
        self.channel = channel
        self.server = server
        self.pseudo = pseudo
        
        print("connecting to:" + self.server)
        
        messages = [f"USER {pseudo} {pseudo} {pseudo} :Je suis un bot\n",
                    f"NICK {pseudo}\n",
                    f"JOIN {channel}\n"]
        self.sock.connect((server, 6667))
        for m in messages:
            self.sock.send(m.encode('utf-8'))
    
    
    def get_text(self):
        try:
            data = self.sock.recv(2048).decode('utf-8')
        except:
            self.send("On ne m'aura plus")
            data = ""
        return data
    
    
    def get_quote(self):
        api_endpoint = "https://favqs.com/api/qotd"
        
        r = requests.get(api_endpoint)
        try:
            r.raise_for_status()
            json = r.json()
            return json['quote']['author'], json['quote']['body']
        except:
            sys.stderr.write("Quote couldn't be fetched...\n")
            return None
        finally:
            sys.stderr.flush()
    
    
    def say_quote(self):
        print("sending quote")
        
        p = ["Comme le disait ce bon {0}, \"{1}\"",
             "{0} l'a dit : \"{1}\"",
             "\"{1}\", et c'est {0} qui l'a dit !",
             "\"{1}\", {0} était loin d'être un imbécile",
             "\"{1}\"",
            ]
        
        author, quote = self.get_quote()
        if quote:
            self.send(random.choice(p).format(author, quote))
    

if __name__ == "__main__":
    chan = "#labaleine"
    serv = "irc.freenode.net"
    nick = "herve29"
    
    b = Bot()
    b.connect(serv, chan, nick)
    b.run()
    
