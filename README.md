PemboPiper
==========

altcoin testing

Here's the final product: http://i.imgur.com/4RUzs8U.jpg [1]

I am totally new at python raspi coding, so please make a backup copy of your "home/pi/Printer" folder and an extra copy of your keys on a flash drive. If something crashes or fails to work, you can copy/paste the contents of the backup "Printer-backup" folder back to the main "Printer" directory and everything will be just as it was before. I'm using a Piper A model [2] and this is for software version 1.05. Since this is the only version I have right now.

After you've backed up your Printer folder, copy this page to a text file on a flash drive to load to your Piper. I've tried opening the files outside of the pi then overwriting them, but it didn't work. I had to edit the files locally in Leafpad. Go to the Printer folder and open "gui.py" "genkeys.py" and "piper.py" using Leafpad. I'm going to mark new code with ++ so you can see where it fits with the rest of the code. Do not leave the ++ in the code. (In leafpad, go to the options menu and enable Line Numbers, many helpful). We're basically adding 5 copies of the sames piece of code in each case. Also the bulk wallet feature didn't work to well, I would suggest staying with printing one at a time.

Here are the bmp backgrounds https://www.dropbox.com/s/gdu0ojeewu89x1t/doge-wallet-enc.zip that you need to add to "home/pi/Printer/Images" folder. You can create any bmp and rename/replace the image and the printer will now print that one for that number selection.

Close the gui Piper Wallet program. Open "gui.py" using Leafpad add the following code at line 549. This adds the additional 5 buttons on the Settings tab, http://i.imgur.com/nsyUjBj.jpg, in the Piper gui. We are also changing the "padx" value to 5 so everything fits.

    tk.Label(coinTypeFrame, text="Coin type:").pack(side=tk.LEFT, padx=10, pady=10)
    self.coinType = tk.StringVar()
    tk.Radiobutton(coinTypeFrame, text="Bitcoin", variable=self.coinType, value="bitcoin").pack(side=tk.LEFT, padx=5, pady=10)
    tk.Radiobutton(coinTypeFrame, text="Litecoin", variable=self.coinType, value="litecoin").pack(side=tk.LEFT, padx=5, pady=10)
    ++   tk.Radiobutton(coinTypeFrame, text="Dogecoin", variable=self.coinType, value="dogecoin").pack(side=tk.LEFT, padx=5, pady=10)
    ++   tk.Radiobutton(coinTypeFrame, text="Doge1", variable=self.coinType, value="doge1").pack(side=tk.LEFT, padx=5, pady=10)
    ++   tk.Radiobutton(coinTypeFrame, text="Doge2", variable=self.coinType, value="doge2").pack(side=tk.LEFT, padx=5, pady=10)
    ++   tk.Radiobutton(coinTypeFrame, text="Doge3", variable=self.coinType, value="doge3").pack(side=tk.LEFT, padx=5, pady=10)
    ++   tk.Radiobutton(coinTypeFrame, text="Doge4", variable=self.coinType, value="doge4").pack(side=tk.LEFT, padx=5, pady=10)
    coinTypeFrame.pack()

On line 568 - change the displayed information about address prefixes, this does not effect how it works

    tk.Label(self, text="Address prefix - 1 for bitcoin - L for litecoin - D for Doge - or key generation will fail.").pack(padx=10)

Next is line 611 in the same file. This adds a check to make sure AES is selected

    #first, check that BIP0038 and litecoin are not both set
    if(self.coinType.get() == "litecoin" and self.encType.get() == "bip0038"):
        self.showMessage("Error!!","BIP0038 is not compatible with litecoin.  Settings not saved.") 
        self.encType.set("aes") 
    ++  if(self.coinType.get() == "dogecoin" and self.encType.get() == "bip0038"):
    ++      self.showMessage("Error!!","BIP0038 is not compatible with dogecoin.  Settings not saved.") 
    ++      self.encType.set("aes") 
    ++
    ++  if(self.coinType.get() == "doge1" and self.encType.get() == "bip0038"):
    ++      self.showMessage("Error!!","BIP0038 is not compatible with dogecoin.  Settings not saved.") 
    ++      self.encType.set("aes") 
    ++
    ++  if(self.coinType.get() == "doge2" and self.encType.get() == "bip0038"):
    ++      self.showMessage("Error!!","BIP0038 is not compatible with dogecoin.  Settings not saved.") 
    ++      self.encType.set("aes") 
    ++
    ++  if(self.coinType.get() == "doge3" and self.encType.get() == "bip0038"):
    ++      self.showMessage("Error!!","BIP0038 is not compatible with dogecoin.  Settings not saved.") 
    ++      self.encType.set("aes")  
    ++
    ++  if(self.coinType.get() == "doge4" and self.encType.get() == "bip0038"):
    ++      self.showMessage("Error!!","BIP0038 is not compatible with dogecoin.  Settings not saved.") 
    ++      self.encType.set("aes") 
        return
    #second, check that prefix is valid

Just below this code in the same file we need to add the vanitygen info and check for the "D" suffix

    if(self.coinType.get() == "litecoin"):
        if(len(self.addrPrefix.get()) == 0 or self.addrPrefix.get()[0] != "L"):
            self.showMessage("Error!!","Invalid address prefix.  Litecoin addresses must begin with L.") 
            return
        process = Popen(["./vanitygen-litecoin", "-q", "-n", "-L", "-t","1","-s", "/dev/random", self.addrPrefix.get()], stderr=PIPE)
    ++      elif(self.coinType.get() == "dogecoin"):
    ++          if(len(self.addrPrefix.get()) == 0 or self.addrPrefix.get()[0] != "D"):
    ++              self.showMessage("Error!!","Invalid address prefix.  Dogecoin must begin with D.") 
    ++              return
    ++          process = Popen(["./vanitygen-litecoin", "-q", "-n", "-X30", "-t","1","-s", "/dev/random", self.addrPrefix.get()], stderr=PIPE)
    ++      elif(self.coinType.get() == "doge1"):
    ++          if(len(self.addrPrefix.get()) == 0 or self.addrPrefix.get()[0] != "D"):
    ++              self.showMessage("Error!!","Invalid address prefix.  Dogecoin must begin with D.") 
    ++              return
    ++          process = Popen(["./vanitygen-litecoin", "-q", "-n", "-X30", "-t","1","-s", "/dev/random",     self.addrPrefix.get()], stderr=PIPE)
    ++      elif(self.coinType.get() == "doge2"):
    ++          if(len(self.addrPrefix.get()) == 0 or self.addrPrefix.get()[0] != "D"):
    ++              self.showMessage("Error!!","Invalid address prefix.  Dogecoin must begin with D.") 
    ++              return
    ++          process = Popen(["./vanitygen-litecoin", "-q", "-n", "-X30", "-t","1","-s", "/dev/random", self.addrPrefix.get()], stderr=PIPE)
    ++      elif(self.coinType.get() == "doge3"):
    ++          if(len(self.addrPrefix.get()) == 0 or self.addrPrefix.get()[0] != "D"):
    ++              self.showMessage("Error!!","Invalid address prefix.  Dogecoin must begin with D.") 
    ++              return
    ++          process = Popen(["./vanitygen-litecoin", "-q", "-n", "-X30", "-t","1","-s", "/dev/random", self.addrPrefix.get()], stderr=PIPE)
    ++      elif(self.coinType.get() == "doge4"):
    ++          if(len(self.addrPrefix.get()) == 0 or self.addrPrefix.get()[0] != "D"):
    ++              self.showMessage("Error!!","Invalid address prefix.  Dogecoin must begin with D.") 
    ++              return
    ++          process = Popen(["./vanitygen-litecoin", "-q", "-n", "-X30", "-t","1","-s", "/dev/random", self.addrPrefix.get()], stderr=PIPE)
    else:
        if(len(self.addrPrefix.get()) == 0 or self.addrPrefix.get()[0] != "1"):
            self.showMessage("Error!!","Invalid address prefix.  Bitcoin addresses must begin with 1.") 
            return
        process = Popen(["./vanitygen", "-q","-n", "-t","1","-s", "/dev/random", self.addrPrefix.get()], stderr=PIPE)

Save and Close

------In the Next file "genkeys.py" and go to line 48, adding vanitygen info

    if(coinType == "litecoin"):
    process = Popen(["./vanitygen-litecoin", "-q", "-L", "-t","1","-s", "/dev/random", addrPrefix], stdout=PIPE)
    ++  elif(coinType == "dogecoin"):
    ++      process = Popen(["./vanitygen-litecoin", "-q", "-X30", "-t","1","-s", "/dev/random", addrPrefix], stdout=PIPE)
    ++  elif(coinType == "doge1"):
    ++      process = Popen(["./vanitygen-litecoin", "-q", "-X30", "-t","1","-s", "/dev/random", addrPrefix], stdout=PIPE)
    ++  elif(coinType == "doge2"):
    ++      process = Popen(["./vanitygen-litecoin", "-q", "-X30", "-t","1","-s", "/dev/random", addrPrefix], stdout=PIPE)
    ++  elif(coinType == "doge3"):
    ++      process = Popen(["./vanitygen-litecoin", "-q", "-X30", "-t","1","-s", "/dev/random", addrPrefix], stdout=PIPE)
    ++  elif(coinType == "doge4"):
    ++      process = Popen(["./vanitygen-litecoin", "-q", "-X30", "-t","1","-s", "/dev/random", addrPrefix], stdout=PIPE)
    else:
       process = Popen(["./vanitygen", "-q", "-t","1","-s", "/dev/random", addrPrefix], stdout=PIPE)

Save and close.

----------------Open "pyper.py" and go line 64. This is how it knows what background picture goes with each radio button on the Settings tab

    if(coinType == "litecoin"):
        finalImgName="ltc-wallet"
    ++  elif(coinType == "dogecoin"):
    ++      finalImgName="doge-wallet"
    ++  elif(coinType == "doge1"):
    ++      finalImgName="1doge-wallet"
    ++  elif(coinType == "doge2"):
    ++      finalImgName="2doge-wallet"
    ++  elif(coinType == "doge3"):
    ++      finalImgName="3doge-wallet"
    ++  elif(coinType == "doge4"):
    ++      finalImgName="4doge-wallet"
    else:
        finalImgName="btc-wallet"

Save and close. That should be it.

Double click the Piper shortcut on the desktop and launch the new gui. From the setting tab, select one of the Doges, put a "D" in the prefix box, and Apply changes. Now when you print from the first tab or press the button on the outside, it will print that corresponding background.
