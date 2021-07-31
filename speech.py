from subprocess import Popen
import speech_recognition as sr
import time
from gtts import gTTS 
import os 
import math
import time
from pynput.keyboard import Key, Controller
import screeninfo
from tkinter import *  
import requests, json
top = Tk()  

dil="tr"
top.geometry("400x500") 
yol="~/"
  
listbox = Listbox(top)  
listbox.place(x=0,y=0,width=400,height=500)
listbox.insert(1,".")
listbox.insert(2,"..")
liste=os.popen("ls -U1 ~/").read().split("\n")
listbox.heigth=len(liste)+1
for i in range(3,len(liste)+2):
    listbox.insert(i,liste[i-3])
listbox.selection_set(0)
  

  
  
  
 


# Initialize recognizer class (for recognizing the speech)

#hcitool rssi 1C:91:9D:2B:4B:C9
def itemindex():
   for item in listbox.curselection():
       return item

r = sr.Recognizer()
#print(os.popen("adb devices").read().split("\n")[1].find("device"))
language = 'tr'
os.system("mkdir -p ~/.config/makbule")
makbus=False
# Reading Microphone as source
# listening the speech and store in audio_text variable
#paketler=["com.whatsapp","ru.yandex.disk","com.wolfram.android.alpha","com.twitter.android","org.thunderdog.challegram","com.stremio.one","com.microsoft.office.outlook","com.tmob.AveaOIM","com.mixplorer","com.touchtype.swiftkey.beta","mega.privacy.android.app","com.pozitron.iscep","com.instagram.android","deezer.android.app","com.aurora.store","com.amazon.mShop.android.shopping","droom.sleepIfUCan","org.adaway"]
paketler=["org.adaway","ru.yandex.disk"]
print(os.popen("adb shell stat -c '%g' /data/data/com.whatsapp").read())

def komut(com):
    Popen(com,shell=False, stdin=None,stdout=None,stderr=None,close_fds=True)
def konus(cumle):
    myobj = gTTS(text=cumle, lang=language, slow=False) 
    myobj.save("file.mp3") 
    os.system("mpv --audio-display=no file.mp3")
            
def dinle(pof):
    with sr.Microphone() as source:
        global makbus
        global dil
        r.adjust_for_ambient_noise(source,duration=0.5)
        print(r.energy_threshold)
        if len(pof)>0: konus(pof)
        print("dinliyorum")
        data = r.listen(source)
        print(dil)
        try:
            text = r.recognize_google(data,language=dil)
            
        except sr.WaitTimeoutError:
            pass
            text=""
        except sr.UnknownValueError:
            pass
            text=""
        print(text.lower())
        return text.lower()
def sifre(laf):
    
    text=dinle(laf)
    print(text)
    print("şifre dinledi")
    sif=text.lower().replace(" ","")
        
    if os.popen("faillock --reset && echo "+sif+" | sudo -S echo deneme").read().find("deneme")>-1:
        return text.lower().replace(" ","")
    else:
        return sifre("Hatalı giriş")
def makbule():
    global makbus
    global dil
    text=dinle("")
    if text.find("temizle")>-1:
        text=text.split("temizle ")[1]
    if text=="makbule" or text=="makbuş":
        konus('Efendim')
        makbus=True
    if makbus==True:
            #text=text.split("temizle ")[len(text.split("temizle "))-1]
        if text=="film izleyeceğim" or text=="i will watch a movie":
            konus("İyi seyirler dilerim")
            komut("stremio")
        if text=="filmi kapat" or text=="close the movie":
            os.system("pkill -f stremio")
        if text.find("google'da ara ")>-1 or text.find("google it ")>-1 :
            os.system("brave https://www.google.com/search?q=" + text.replace("google'da ara ","").replace("google it ","").replace(" ","%20"))
            konus("İşte " + text.replace("google'da ara ","").replace("google it ","") +" için bulunan sonuçlar.")
        if text=="bilgisayarı kapat" or text=="shutdown the computer":
            konus("Görüşürüz")
            os.system("shutdown now")
        if text=="bilgisayarı yeniden başlat" or text=="reboot the computer":
            os.system("shutdown -r now")
        if text=="lateksi aç":
            komut("gnome-latex")
        if text=="sağa kaydır":
            info=screeninfo.get_monitors()[1].width
            os.popen("xdotool windowmove $(xdotool getwindowfocus) "+str(info)+" 0")
        if text=="sola kaydır":
            os.popen("xdotool windowmove $(xdotool getwindowfocus) 0 0")
        if text=="lateksi kapat" or text=="lateks i kapat":
            os.system("pkill -f gnome-latex")
        if text=="mesajları aç":
            os.system("brave https://www.web.whatsapp.com")
        if text=="verileri yok et" or text=="execute order 66":
            os.system("rm -rf ~/.config/makbule/*")
            konus("Başarıyla tamamlandı")
        if text=="dinlemeyi bırak":
            makbus=False
        if text=="şifreyi değiştir":
            sif=dinle()
        if text=="i̇ngilizceye geç":
            dil="en-US"
        if text=="switch to turkish":
            dil="tr"
        if text=="hava sıcaklığı" or text=="weather temperature":
            #2bddf0e4b40040563aee96fed576907f
            x = requests.get("http://api.openweathermap.org/data/2.5/weather?appid=2bddf0e4b40040563aee96fed576907f&q=Istanbul").json()
            if x["cod"] != "404":
                derece=x["main"]["temp"]-272.15
                if derece>=30.0:
                    konus("Hava " + str(derece)[:4] + " derece. Sıcak yok da nem var. Nem çok bunaltıyo.")
                else:
                    konus("Hava " + str(derece)[:4] + " derece")
            else:
                konus("Böyle bir şehir yok")
        if text=="dosya yöneticisini aç" or text=="open file manager":
            top.update()
            kemt=""
            while (kemt!="bitir"):
                kemt=dinle("")
                if kemt=="sonraki" or kemt=="next":
                    mikmik=itemindex()
                    listbox.selection_clear(0,END)
                    listbox.selection_set(mikmik+1)
                    top.update()
                if kemt.find("satır")>-1:
                    satir=int(kemt.replace("satır ","").replace("altı","6").replace("yedi","7"))
                    listbox.selection_clear(0,END)
                    listbox.selection_set(satir-1)
                    top.update()
                if kemt=="aç":
                    os.popen("xdg-open "+yol+listbox.get(listbox.curselection()[0]))
                if text=="kapat":
                    os.popen("xdotool windowkill $(xdotool getwindowfocus)")
        if text=="değiştir" or text=="change":
            name=os.popen("xdotool getactivewindow getwindowname").read().replace("\n","")
            isaret='""'
            windows=os.popen("wmctrl -l|awk '{$3="+isaret+"; $2="+isaret+"; $1="+isaret+"; print $0}'").read().split("\n")
            windows.remove(windows[0])
            windows.remove(windows[0])
            windows.remove(windows[0])
            windows.remove(windows[0])
            isaret=0
            kemkum=""
            while (kemkum!="dur"):
                os.popen("wmctrl -a "+chr(ord('"'))+windows[isaret%len(windows)].strip()+chr(ord('"')))
                isaret+=1
                print("\a")
                kemkum=dinle("")
        if text=="yazma modu" or text=="typing mode":
            gevgev=""
            while (gevgev!="bitir"):
                gevgev=dinle("")
                keyboard=Controller()
                if gevgev.find("harf sil")<0:
                    keyboard.type(gevgev)
                else:
                    miktar=int(gevgev.replace("harf sil","").replace(" ",""))
                    for l in range(0,miktar):
                        keyboard.press(Key.backspace)
                        keyboard.release(Key.backspace)
        if text=="lost'un sonu nasıldı":
            konus("lost çok bozdu. başlarda güzeldi sonra ama öyle böyle bozmadı, önünü alamadık. bozdu bozdu bozdu daha ne kadar bozabilir dedim ya!")
        if text=="tam ekran":
            os.system("wmctrl -r :ACTIVE: -b add,toggle,fullscreen")
            print("\a")
        if text=="kapat":
            os.popen("xdotool windowkill $(xdotool getwindowfocus)")
        if text=="tam ekrandan çık":
            os.system("wmctrl -r :ACTIVE: -b remove,toggle,fullscreen")
        if text=="boyutu değiştir":
            os.popen("wmctrl -r :ACTIVE: -b toggle,maximized_vert,maximized_horz")
        if text.lower()=="sesi dışarı ver":
            os.popen("pactl set-default-sink alsa_output.pci-0000_00_1b.0.analog-stereo")
        if text.lower()=="sesi kulaklığa ver":
            os.popen("pactl set-default-sink bluez_sink.1C_91_9D_2B_4B_C9.a2dp_sink")
        if text.lower()=="telefonu yedekle" and os.popen("adb devices").read().split("\n")[1].find("device")>-1:
            os.system("mkdir -p ~/.config/makbule/data/data")
            os.system("mkdir -p ~/.config/makbule/data/user/0")
            for i in paketler:
                path=os.popen("adb shell pm path " + i).read().split("\n")[0].replace("package:","").replace("\n","")
                os.system("adb pull "+path +" ~/.config/makbule/"+i+".apk")
                os.system("adb shell su -c tar -pcvzf /storage/emulated/0/"+i+".tar /data/data/"+i)
                os.system("adb shell su -c tar -pcvzf /storage/emulated/0/"+i+"2.tar /data/user/0/"+i)
                os.system("adb pull /storage/emulated/0/"+i+".tar ~/.config/makbule/data/data/")
                os.system("adb pull /storage/emulated/0/"+i+"2.tar ~/.config/makbule/data/user/0/")
                os.system("adb shell rm /storage/emulated/0/"+i+".tar")
                os.system("adb shell rm /storage/emulated/0/"+i+"2.tar")
            #os.system("cd ~/.config/makbule && adb pull /storage/emulated/0/WhatsApp && adb pull /storage/emulated/0/DCIM && adb pull /storage/emulated/0/Download && adb pull /storage/emulated/0/Music && adb pull /storage/emulated/0/TitaniumBackup")
        if text.lower()=="verileri geri yükle" and os.popen("adb devices").read().split("\n")[1].find("device")>-1:
            for i in paketler:
                os.system("cd ~/.config/makbule && adb install "+i+".apk")
                time.sleep(3)
                id=str(os.popen("adb shell stat -c '%g' /data/data/"+i).read())
                id=id[0]+id[1]+id[2]+id[3]+id[4]
                os.system("adb push ~/.config/makbule/data/data/"+i+".tar /storage/emulated/0/ && adb push ~/.config/makbule/data/user/0/"+i+"2.tar /storage/emulated/0/")
                os.system("adb shell su -c tar -pxvzf /storage/emulated/0/"+i+".tar --owner="+str(id)+" --group="+str(id))
                os.system("adb shell su -c tar -pxvzf /storage/emulated/0/"+i+"2.tar --owner="+str(id)+" --group="+str(id))
                os.system("adb shell rm /storage/emulated/0/"+i+".tar")
                os.system("adb shell rm /storage/emulated/0/"+i+"2.tar")
#pactl set-sink-volume alsa_output.pci-0000_00_1b.0.analog-stereo +90% sesi arttırır
#pactl set-default-source bluez_source.1C_91_9D_2B_4B_C9.headset_head_unit mikrofon değişir
#pactl list-sinks | grep name: hoperlör listeleme
#pactl list sources mikrofon listeleme
#os.popen("adb shell stat -c '%g' /data/data/com.instagram.android")
#adb shell su -c tar -xf /storage/emulated/0/com.instagram.android2.tar --owner=10308 --group=10308

while True:
    time.sleep(0.1)
    makbule()
    
