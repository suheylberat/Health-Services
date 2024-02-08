
import requests
from bs4 import BeautifulSoup
import time 
import re


# ilaçlar hakkında bilgi al. 
# acil bir durumda gidilecek yerleri bul.
class Uygulama():
    def __init__(self):
        self.dongu= True

    def program(self):
        tercih = self.menu()

        if tercih == "1":
            print("İlaçlar hakkında bilgi almaya yönlendiriliyorsunuz.")
            Meds = Medicines()
            while Meds.dongu:
                Meds.program()

        if tercih == "2":
            print("En yakın acil servis hakkında bilgi almaya yönlendiriliyorsunuz.")
            servis = Emergency()
            while servis.dongu:
                servis.program()

        if tercih == "3":
            print("Çıkış yapılıyor, iyi günler")
            self.cikis()


    def menu(self):
        def control(tercih):
            if re.search("[^1-3]",tercih):
                raise Exception("Lütfen 1 ve 3 arasında bir seçim yapınız")
            
            elif len(tercih)!=1:
                raise Exception("Lütfen 1 ve 3 arasında bir seçim yapınız")
            
        while True:
            try:
                tercih = input("Merhabalar Berat Meds'e hoş geldiniz.\n\nLütfen yapmak istediğiniz işlemi seçiniz\n[1]- İlaçlar hakkında bilgi almak \n[2]- En yakın acili bulmak\n[3]- Çıkış\n\n")
                control(tercih)

            except Exception as hata:
                print(hata)
                time.sleep(3)

            else:
                break

        return tercih
    
    def cikis(self):
        self.dongu= False
        exit()
    
BeratMedS = Uygulama()
while BeratMedS.dongu:
    BeratMedS.program()



class Medicines:

    def __init__(self):
        self.dongu= True
        self.ilac = input("İlgilendiğiniz ilacın ismini lütfen söyleyiniz: ")


    def program(self):
        secim = self.menu()

        if secim == "1":
            print("İlaç bilgi sayfasına yönlendiriliyorsunuz...\n")
            time.sleep(3)
            self.About()

        if secim == "2":
            print("İlacı kimler kullanabilir, kimler kullanamaz hakkında bilgi alınıyor....\n")
            time.sleep(3)
            self.WhoCan()

        if secim == "3":
            print("İlacın kullanımı hakkında bilgi alınıyor...\n")
            time.sleep(3)
            self.howUs()

        if secim == "4":
            print("Yan etkiler hakkında bilgi alınıyor...\n")
            time.sleep(3)
            self.SideEffects()    

        if secim == "5":
            print("Sık sorulan sorular gösteriliyor...\n")
            time.sleep(3)
            self.commonQuestions()

        if secim == "6":
            print("Otomasyondan çıkılıyor. Teşekkürler...\n")
            time.sleep(3)
            self.cikis()
        



    def menu(self):
        def control(secim):
            if re.search("[^1-6]",secim):
                raise Exception("Lütfen 1 ve 6 arasında bir seçim yapınız")
            
            elif len(secim)!=1:
                raise Exception("Lütfen 1 ve 6 arasında bir seçim yapınız")
            
        while True:
            try:
                secim = input("Merhabalar Berat Meds'e hoş geldiniz.\n\nLütfen yapmak istediğiniz işlemi seçiniz\n[1]- About \n[2]- Who can and connot take or use it\n[3]- How and when to take it\n[4]- Side Effects\n[5]- Common Questions\n[6]- Exit\n\n")
                control(secim)

            except Exception as hata:
                print(hata)
                time.sleep(3)

            else:
                break

        return secim


    def About(self):
        while True:
            try:
                with open("ilaclar.txt","a+") as İlaclar:
                    İlaclar.write(f"{self.ilac}\n")



                url = f"https://www.nhs.uk/medicines/{self.ilac.lower()}/about-{self.ilac.lower()}/"
                parser = BeautifulSoup(requests.get(url).content, "html.parser")
                bilgi = parser.find("main",{"id":"maincontent"}).find("article").find_all("section")
                bilgi2 = bilgi[0].find_all("p")

                for i in bilgi2:
                    print(i.string)

                if any("li" in item for item in bilgi2):
                    lili = bilgi2.find_all("li")
                    print(lili)
                    break
            
            except AttributeError:
                    plus = f"https://www.nhs.uk/medicines/{self.ilac}/"
                    parser = BeautifulSoup(requests.get(plus).content, "html.parser")
                    info = parser.find("main",{"id":"maincontent"}).find("article").find("section", {"id": f"about-{self.ilac}"}).find_all("p")
                    for i  in info:
                        if any("a" in item for item in i):
                            print(i.string, i.a.string)
                        else:
                            print(i.string)

                    time.sleep(3)
                    break
            
            else:
                print("İlacın ismini yanlış girdiniz...")
                  

        time.sleep(3)
        self.menudon()        

    def commonQuestions(self):
        while True:
            try:
                url = f"https://www.nhs.uk/medicines/{self.ilac}/common-questions-about-{self.ilac}/"
                parser = BeautifulSoup(requests.get(url).content, "html.parser")
                bilgi = parser.find_all("span", {"class":"nhsuk-details"})
                #a tag varsa onu da yazdırmasını istiyorum, bilgi1 ile alakalı bu tag
                for i in bilgi:
                    soru = i.span.string
                    icerik = i.p.string
                    if i.p.a.string !=None:
                        print(soru, icerik, i.p.a.string)
                    
                    else:
                        print(soru, icerik)


            except AttributeError:
                qquestions =  f"https://www.nhs.uk/medicines/{self.ilac}/"
                parser = BeautifulSoup(requests.get(qquestions).content, "html.parser")
                bbilgi = parser.find_all("details", {"class":"nhsuk-details__summary-text"})
                bilgi2 = bbilgi.find_all("div", {"class": "nhsuk-details__text"})
                for i in bilgi2:
                    soru = i.span.string
                    icerik = i.p.string
                    if i.p.a !=None:
                        print(soru, icerik, i.p.a.string)
                    
                    else:
                        print(soru, icerik)
                    

    def SideEffects(self):
        while True:
            try:
                    url = f"https://www.nhs.uk/medicines/{self.ilac}/side-effects-of-{self.ilac}/"
                    parser = BeautifulSoup(requests.get(url).content, "html.parser")
                    bilgi = parser.find_all("section")

                    for i in range(0,len(bilgi)):
                        ptags = bilgi[i].find_all("p")
                        h2tags = bilgi[i].find_all("h2")
                        for k in h2tags:
                            print(k.string)
                        for j in ptags:
                            if j.a.string != None:
                                print(j, j.a.string)
                            else:
                                print(j)                                      
                    break

            except AttributeError:
                    plus = f"https://www.nhs.uk/medicines/{self.ilac}/"
                    parser = BeautifulSoup(requests.get(plus).content, "html.parser")
                    bilgi = parser.find_all("section")

                    for i in range(0,len(bilgi)):
                        ptags = bilgi[i].find_all("p")
                        h2tags = bilgi[i].find_all("h2")
                        for k in h2tags:
                            print(k.string)
                        for j in ptags:
                            if j.a.string != None:
                                print(j, j.a.string)
                            else:
                                print(j)    
                    break

            else:
                print("İlacın ismini yanlış girdiniz...")

        time.sleep(3)
        self.menudon()     


    def howUs(self):
        while True:
            try:
                url = f"https://www.nhs.uk/medicines/{self.ilac}/how-and-when-to-take-{self.ilac}/"
                parser = BeautifulSoup(requests.get(url).content, "html.parser")
                bilgi = parser.find_all("section")

                for i in range(0,len(bilgi)):
                        ptags = bilgi[i].find_all("p")
                        h2tags = bilgi[i].find_all("h2")
                        ultags = bilgi[i].find_all("ul")
                        for l in ultags:
                            print(l.li.string)
                        for k in h2tags:
                            print(k.string)
                        for j in ptags:
                            if j.a.string != None:
                                print(j, j.a.string)
                            else:
                                print(j)    
                break
            except AttributeError:
                    plus = f"https://www.nhs.uk/medicines/{self.ilac}/"
                    parser = BeautifulSoup(requests.get(plus).content, "html.parser")
                    bilgi = parser.find_all("section")

                    for i in range(0,len(bilgi)):
                        ptags = bilgi[i].find_all("p")
                        h2tags = bilgi[i].find_all("h2")
                        ultags = bilgi[i].find_all("ul")
                        oltags = bilgi[i].find("ol")

                        if oltags:
                            for o in oltags:
                                print(o.li.string)

                        if ultags:
                            for l in ultags:
                                print(l.li.string)
                        
                        if h2tags:
                            for k in h2tags:
                                print(k.string)
                        
                        if ultags:
                            for j in ptags:
                                if j.a.string != None:
                                    print(j, j.a.string)
                                else:
                                    print(j)  
                    break 
            
            else:
                print("İlacın ismini yanlış girdiniz...")

        time.sleep(3)
        self.menudon()     

    def WhoCan(self):
        pass

    def cikis(self):
        self.dongu= False
        exit()

    def menudon(self):
        while True:
            x = input("Ana menüye dönmek için 7'ye, çıkmak için 6'ya basınız...:")
            if x == "7":
                print("Ana menüye dönülüyor...")
                time.sleep(3)
                self.program()
                break

            elif x == "6":
                self.cikis()
                break

            else:
                print("Lütfen geçerli bir seçim yapınız.")



class Emergency():
    def __init__(self):
        self.dongu = True

    def program(self):
        seceenek = self.menu()

    def menu(self):
        def control(secim):
            if re.search(" ",secim):
                ayirma = secim.split()
                url = f"https://www.nhs.uk/service-search/pharmacy/find-a-pharmacy/results/{ayirma[0]}%20{ayirma[1]}"
                parser = BeautifulSoup(requests.get(url).content,"html.parser")

                lit = parser.find("ol").find_all("li")

                for i in range(0,len(lit)):
                    distance = lit.find("p", {"id": f"distance_{i}"}).string
                    name = lit.find("h2", {"id": f"orgname_{i}"}).find("a").string
                    road = lit.find("p", {"id": f"address_{i}"}).string
                    phone = lit.find("p", {"id": f"phone_{i}"}).string
                    print(distance.string,distance.span.string,name,road,phone)
               

            else:
                url = f"https://www.nhs.uk/service-search/find-an-accident-and-emergency-service/results/{secim}"
                parser = BeautifulSoup(requests.get(url).content,"html.parser")
                lit = parser.find("ol").find_all("li")

                for i in range(0,len(lit)):
                    distance = lit.find("p", {"id": f"distance_{i}"})
                    name = lit.find("h2", {"id": f"orgname_{i}"}).find("a").string
                    road = lit.find("p", {"id": f"address_{i}"}).string
                    phone = lit.find("p", {"id": f"phone_{i}"}).string
                    print(distance.string,distance.span.string,name,road,phone)
               

        while True:
            try:
                secim = input("Merhabalar, size yardımcı olabilmemiz için lütfen yaşadığınız yerin posta kodunu giriniz.")
                problem = input("Lütfen acil olan durumunuzu belirtiniz.")

                with open("Emergencycases","a+") as Emergency:
                    Emergency.write(f"{problem}\n")

                control(secim)

            except AttributeError:
                print("Hatalı bir posta kodu girdiniz.")
                time.sleep(3)

            else:
                break

        return secim

    def menudon(self):

        while True:
            x = input("Ana menüye dönmek için 7'ye, çıkmak için 6'ya basınız...:")
            if x == "7":
                print("Ana menüye dönülüyor...")
                time.sleep(3)
                self.program()
                break

            elif x == "6":
                self.cikis()
                break

            else:
                print("Lütfen geçerli bir seçim yapınız.")

    def cikis(self):
        self.dongu= False
        exit()