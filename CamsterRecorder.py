import urllib.request, os, time, datetime, random, sys, threading
from bs4 import BeautifulSoup
from livestreamer import Livestreamer

#specify path to save to ie "/Users/Joe/camster"
save_directory = "/Users/Joe/camster"
#specify the path to the wishlist file ie "/Users/Joe/camster/wanted.txt"
wishlist = "/Users/Joe/camster/wanted.txt"

if not os.path.exists("{path}".format(path=save_directory)):
    os.makedirs("{path}".format(path=save_directory))
recording = []
def getOnlineModels():
    wanted = []
    with open(wishlist) as f:
        for model in f:
            models = model.split()
            for theModel in models:
                wanted.append(theModel.lower())
    f.close()
    online = []
    result = urllib.request.urlopen("http://new.naked.com/")
    result = result.read()
    soup = BeautifulSoup(result, 'lxml')
    for a in soup.find_all('a', href=True):
        if a['href'][:8] == '/webcam/':
            online.append(a['href'])
    result = urllib.request.urlopen("http://new.naked.com" + random.choice(online))
    result = result.read()
    soup = BeautifulSoup(result, 'lxml')
    for model in soup.findAll("div", {"class": "each-girls"}):
        aux = model.findAll('a')
        modelName = str(aux).split('"')[3][8:].split('/')[0].lower()
        if modelName in wanted and modelName not in recording:
            link = str(aux).split('"')[11][6:]
            thread = threading.Thread(target=startRecording, args=(modelName, link))
            thread.start()

def startRecording(model, link):
    session = Livestreamer()
    streams = session.streams("hls://http://transcode.k8s-do.naked.com/hls/" + link + "/index.m3u8")
    stream = streams["best"]
    fd = stream.open()
    ts = time.time()
    st = datetime.datetime.fromtimestamp(ts).strftime("%Y.%m.%d_%H.%M.%S")
    if not os.path.exists("{path}/{model}".format(path=save_directory, model=model)):
        os.makedirs("{path}/{model}".format(path=save_directory, model=model))
    with open("{path}/{model}/{st}_{model}.mp4".format(path=save_directory, model=model,
                                                       st=st), 'wb') as f:
        recording.append(model.lower())
        while True:
            try:
                data = fd.read(1024)
                f.write(data)
            except:
                recording.remove(model)
                f.close()
                return ()

if __name__ == '__main__':
    while True:
        getOnlineModels()
        for i in range(20, 0, -1):
            sys.stdout.write("\033[K")
            print("{} model(s) are being recorded. Next check in {} seconds".format(len(recording), i))
            sys.stdout.write("\033[K")
            print("the followingmodels are being recorded: {}".format(recording), end="\r")
            time.sleep(1)
            sys.stdout.write("\033[F")
