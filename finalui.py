import urllib.request, urllib.parse, urllib.error
import requests
import os
import sys
ip1=input('which one? (1)single user , (2)multiuser , (3)mergeffileparts ==> ')
if ip1=='1':
    def downloads(url):
        name='dl.part' #url.split('/')[-1]
        if os.path.exists(name):
            tsz=str(open('ncfg.txt','r').read())
            fs=os.stat(name).st_size
            b='bytes='+str(fs)+'-'+tsz
            print('File found continue download...')
            headers={}
            headers['Range']=str(b)
            r = requests.get(url,headers=headers, stream=True)
        else:
            r = requests.get(url, stream=True)
            tsize = int(r.headers['content-length'])
            nns=open('ncfg.txt','w')
            nns.write(str(tsize))
            nns.close()
        chunk_size=1024
        count=0

        with open(name,'ab') as f:
            for chunk in r.iter_content(chunk_size=chunk_size):
                if chunk: # filter out keep-alive new chunks

                    f.write(chunk)
                    #
                    count= len(chunk)+count
                    ct=round((count/(1024*1024)),2)
                    x='Downloaded.....'+str(ct)+'MB '
                    sys.stdout.write('\r'+str(x))
                    sys.stdout.flush()
                    f.flush()
    downloads(input('Enter the url of file: '))
if ip1=='2':
    def cfgdl(url,range,part):
        name= str(part)+'.part'
        headers={}
        print(range)
        headers['Range']=str(range)
        r = requests.get(url,headers=headers, stream=True)
        #tsize = int(r.headers['content-length'])

        chunk_size=1024
        count=0
        with open(name,'ab') as f:
            for chunk in r.iter_content(chunk_size=chunk_size):
                if chunk: # filter out keep-alive new chunks
                    f.write(chunk)
                    count= len(chunk)+count
                    ct=round((count/(1024*1024)),2)
                    x='Downloaded.....'+str(ct)+'MB '
                    sys.stdout.write('\r'+str(x))
                    sys.stdout.flush()
                    f.flush()
    ip2= input('''Which one?
                             (1)multiuser start config file
                             (2)already have config
                             (3)continue multiuser downloading
                             ==> ''')
    if ip2=='1':

        if os.path.exists('config.txt'):
            if input('config file exists do you want to continue?(y/n): ')=='n':
                quit()
            else:
                pass
        url = input('Enter the url:')
        r = requests.get(url, stream=True)
        tsize = int(r.headers['content-length'])
        def splitx(x, n):
            #stackof
            z=[]
            if x < n:
                print(-1)

            elif x % n == 0:
                for i in range(n):
                    z.append(x//n)
            else:
                zp = n - (x % n)
                pp = x//n
                for i in range(n):
                    if i>= zp:
                        z.append(pp + 1)
                    else:
                        z.append(pp)
            return z
        y=[]
        count=0
        n = int(input('Enter the number of users:'))
        x=splitx(tsize,n)

        ix=0
        lenx=len(x)-1
        for i in x:
            if ix!=lenx:
                t = 'bytes='+str(count)+'-'+str(count+i-1)
            else:
                t = 'bytes='+str(count)+'-'+str(count+i)
            count=count+i
            y.append(t)
            ix=ix+1
        #y list to file n to file
        cfh =open('config.txt','w')
        cfh.write('parts='+str(n)+'\n')
        for i in y:
            xii=i+'\n'
            cfh.write(xii)
        cfh.write(url)
        option=input('do you want to download now?(y/n):')
        if option=='y':
            print('Enter the part:')
            for i in range(n):
                print(i+1,':',y[i])
            part = int(input('Enter part:')) - 1
            wx=open('conf1.txt','w')
            wx.write(str(part))
            wx.close()
            cfgdl(url,y[part])
        else:
            quit()
    if ip2=='2':
        cfg = open('config.txt')
        n=0
        y=[]
        for i in cfg:
            if 'parts' in i:
                n = int(i.split('=')[1])
                nx=n
                continue
            if n>0:
                n=n-1
                y.append(i[:-1])
            elif n==0:
                if 'url' in i:
                    url=i.split('=')[1]
                    url=url[:-1]
                    break
        cfg.close()
        print('Enter the part:')
        for i in range(nx):
            print(i+1,':',y[i])
        part = int(input('Enter part:')) - 1
        wx=open('conf1.txt','w')
        wx.write(str(part))
        wx.close()
        print(url)
        ww=open('conf1.txt','w')
        ww.write(str(part))
        ww.close()
        cfgdl(url,y[part],part)
    if ip2=='3':
        cfg = open('config.txt')
        n=0
        y=[]
        for i in cfg:
            if 'parts' in i:
                n = int(i.split('=')[1])
                nx=n
                continue
            if n>0:
                n=n-1
                y.append(i[:-1])
            elif n==0:
                if 'url' in i:
                    url=i.split('=')[1]
                    url=url[:-1]
                    break
        cfg.close()
        ww=open('conf1.txt','r').read()
        part=int(ww)
        bx=y[part].split('=')[1]
        bx=bx.split('-')[1]
        by=y[part].split('=')[1]
        by=by.split('-')[0]
        name=str(part)+'.part'
        if os.path.exists(name):
            fs=os.stat('0.part').st_size
            b='bytes='+str(int(by)+fs)+'-'+str(bx)
            cfgdl(url,b,part)
        else:
            print('no files in download')
            quit()
if ip1=='3':
    n=int(input('enter no. of files(merged file is 0.part):'))
    fh1=open('0.part','ab')
    i=1
    while True:
        name=str(i)+'.part'
        with open(name,'rb')as f:
            while True:
                buf=f.read(1024)
                if buf:
                    fh1.write(buf)
                else:
                    break
        if i==n:
            break
        i=i+1
    q = input('do you want to rename final file?(y/n)')
    if q=='y':
        nam = input('enter the file name with proper format eg."x.txt"')
        if os.path.exists('0.part'):
            os.rename('0.part',nam)
        print('Merged')
        quit()
    else:
        print('Merged')
        quit()
#else:
#    print('enter valid detail')
    #quit()
