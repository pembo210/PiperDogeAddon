# This file is part of Piper.
#
#    Piper is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    Piper is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with Piper.  If not, see <http://www.gnu.org/licenses/>.
#
# Piper Copyright (C) 2013  Christopher Cassano

import Tkinter as tk
import ttk
import sqlite3
import sys
import piper as Piper
import wallet_enc
import Image
import ImageFont
import ImageDraw
import qrcode
import time
import os
from subprocess import Popen, PIPE

class PiperUtil:
	def printBulkWallet(self):
		global tab2
		try:
			qty = int(tab2.bulkQuantity.get())
			for x in range(0,qty):
				self.printWallet()
				if qty > 1 and x < qty-1:
					time.sleep(30)
		
		except ValueError:
			print "Please enter an int!!"
			qrPopup = QRPopup()
			qrPopup.showAlert("Error, enter an integer for the number of wallets field!")
	
	
	def printWallet(self):
		print "printWallet!"
		global tab1
		try:
			qty = int(tab1.walletQuantity.get())
			
			if(tab1.verPass.get() != tab1.walletPass.get()):
				print "Error, passwords don't match!"
				qrPopup = QRPopup()
				qrPopup.showAlert("Error, passwords don't match!")
				return
			
			remFlag = ""
			
			rKey = tab1.remKey.get()
			if(rKey == 1):
				remFlag = True
			elif(rKey == 2):
				remFlag = False
			else:
				#invalid option, return
				return
			
			remPrivFlag = ""
			rKey = tab1.remPrivKey.get()
			if(rKey == 1):
				remPrivFlag = True
			elif(rKey == 2):
				remPrivFlag = False
			else:
				#invalid option, return
				return
			
			Piper.genAndPrintKeys(remFlag, remPrivFlag, qty, tab1.walletPass.get())
		
		except ValueError:
			print "Please enter an int!"
			qrPopup = QRPopup()
			qrPopup.showAlert("Error, enter an integer for the copies of wallet field!")
			#uncomment the 'raise' to make it print the real exception
			#raise
	
	def setEncryptYes(self):
		global tab1
		tab1.passGroup.pack(padx=10, pady=10)
		tab1.printButton.forget()
		tab1.printButton.pack()
	
	
	def setEncryptNo(self):
		global tab1
		tab1.walletPass.set("")
		tab1.verPass.set("")
		tab1.passGroup.forget()

	def tabChangedEvent(self, event):
		if event.widget.index("current") == 2:
			global tab3
			tab3.populate()
	
	def reprint(self, event):
		#print_keypair(pubkey, privkey, leftBorderText)
		Piper.print_keypair(event.widget.pubkey, event.widget.privkey, "Serial Number: "+str(event.widget.serialnum))

class DecryptedKeyPopup:
	
	def decryptKey(self):
		try:
			self.decryptedKeyOnPopup.set(wallet_enc.pw_decode(self.encryptedPrivKey, self.walletPass.get()))
		except:
			top = tk.Toplevel()
			top.title("Error!")
			tk.Label(top, text="Incorrect password.").pack(padx=10, pady=10)
			button = tk.Button(top, text="Dismiss", command=top.destroy)
			button.pack(padx=10, pady=10)

	def showPopup(self, event):
		print event.widget.serialnum
		
		qrPopup = QRPopup()

		self.encryptedPrivKey = event.widget.privkey

		top = tk.Toplevel()
		top.title("Decrypted key")
		top.geometry("550x240")
		
		passGroup = tk.LabelFrame(top, text="Encrypted wallet password")
		passFrame = tk.Frame(passGroup)
		self.walletPass = tk.StringVar()
		tk.Label (passFrame, text='Enter password: ').pack(side=tk.LEFT,padx=10,pady=10)
		tk.Entry(passFrame, width=10, textvariable=self.walletPass, show="*").pack(side=tk.LEFT,padx=10,pady=10)
		passFrame.pack()
		
		passGroup.pack(padx=10, pady=10)

		decBut = tk.Button(top, text="Decrypt", command=self.decryptKey)
		decBut.pack(padx=10, pady=10)
		
		resultFrame = tk.Frame(top)
		tk.Label(resultFrame, text="Decrypted key").pack(side=tk.LEFT, padx=10, pady=10)
		self.decryptedKeyOnPopup = tk.StringVar()
		msg = tk.Entry(resultFrame, textvariable=self.decryptedKeyOnPopup, width=52)
		msg.pack(side=tk.LEFT)
		resultFrame.pack(padx=10, pady=10)

		
		buttonFrame = tk.Frame(top)
		qrBut = tk.Button(buttonFrame, text="Show QR Code")
		qrBut.bind("<Button-1>", qrPopup.showDecKeyPopup)
		qrBut.pack(padx=10, pady=10, side=tk.LEFT)
		qrBut.decKeyOnPopup = self.decryptedKeyOnPopup
		button = tk.Button(buttonFrame, text="Dismiss", command=top.destroy)
		button.pack(padx=10, pady=10, side=tk.LEFT)
		buttonFrame.pack()


class QRPopup:

	def showAlert(self, alertMsg):
		top = tk.Toplevel()
		top.geometry("400x90")
		top.title("Alert!")

		tk.Label(top, text=alertMsg).pack(padx=10, pady=10)
		
		button = tk.Button(top, text="Dismiss", command=top.destroy)
		button.pack(padx=10, pady=10)




		


	def showDecKeyPopup(self, event):
		self.show1CodePopup(event.widget.decKeyOnPopup.get())
		
	def showPopup(self, event):
		if event.widget.pubkey != "" and event.widget.privkey != "":
			self.show2CodePopup(event.widget)
		elif event.widget.pubkey != "":
			self.show1CodePopup(event.widget.pubkey)
		elif event.widget.privkey != "":
			self.show1CodePopup(event.widget.privkey)

	
	def show2CodePopup(self, widget):
		top = tk.Toplevel()
		top.title("QR Code")
	
		finalImg = Image.new("RGB", (800, 420), "white")
		
		qr = qrcode.QRCode(
		    version=None,
		    error_correction=qrcode.constants.ERROR_CORRECT_M,
		    box_size=10,
		    border=0,
		)

		qr.add_data(widget.pubkey)
		qr.make(fit=True)

		qrImg = qr.make_image()
		
		font = ImageFont.truetype("/usr/share/fonts/ttf/ubuntu-font-family-0.80/UbuntuMono-R.ttf", 14)
		draw = ImageDraw.Draw(finalImg)
		draw.text((10, 400),"Public: "+widget.pubkey, font=font, fill=(0,0,0))

		finalImg.paste(qrImg, (30, 30))



		qr = qrcode.QRCode(
		    version=None,
		    error_correction=qrcode.constants.ERROR_CORRECT_M,
		    box_size=10,
		    border=0,
		)

		qr.add_data(widget.privkey)
		qr.make(fit=True)

		qrImg = qr.make_image()
			
		font = ImageFont.truetype("/usr/share/fonts/ttf/ubuntu-font-family-0.80/UbuntuMono-R.ttf", 14)
		draw = ImageDraw.Draw(finalImg)
		textToPrint = "Private: "+widget.privkey

		textSize = draw.textsize(textToPrint, font=font)
		
		charInd = 0
		lineInd = 0
		while(textSize[0] > 400):
			textInner = ""
			textSizeInner = draw.textsize(textInner, font=font)
			while(textSizeInner[0] < 390):
				textInner = textInner + textToPrint[charInd]
				textSizeInner = draw.textsize(textInner, font=font)
				charInd += 1

				
			draw.text((380, 360+(lineInd*15)),textInner, font=font, fill=(0,0,0))
			
			textSize = draw.textsize(textToPrint[charInd:], font=font)
			lineInd += 1
		
		draw.text((380, 360+(lineInd*15)),textToPrint[charInd:], font=font, fill=(0,0,0))
		finalImg.paste(qrImg.resize((300, 300)), (400, 30))



		finalImg.save("qrimg2.gif", "gif")
		
		
		
		
				
		qrPI = tk.PhotoImage(file="qrimg2.gif")
		label = tk.Label(top, image=qrPI)
		label.image = qrPI
		label.pack(padx=25, pady=25)	
		
		butFrame = tk.Frame(top)
		saveBut = tk.Button(butFrame, text="Save to Desktop")
		saveBut.bind("<Button-1>", self.saveDouble)
		saveBut.qrImg = finalImg
		saveBut.widgetData = widget
		saveBut.pack(padx=10, pady=10, side=tk.LEFT)

		button = tk.Button(butFrame, text="Dismiss", command=top.destroy)
		button.pack(padx=10, pady=10, side=tk.TOP)

		butFrame.pack(padx=10, pady=10)
	
	
	def show1CodePopup(self, dataToEncode):
		top = tk.Toplevel()
		top.title("QR Code")
		
		qr = qrcode.QRCode(
		    version=None,
		    error_correction=qrcode.constants.ERROR_CORRECT_M,
		    box_size=10,
		    border=0,
		)

		qr.add_data(dataToEncode)
		qr.make(fit=True)

		qrImg = qr.make_image()
		qrImg.save("qrimg1.gif", "gif")
				
		qrPI = tk.PhotoImage(file="qrimg1.gif")
		label = tk.Label(top, image=qrPI)
		label.image = qrPI
		label.pack(padx=25, pady=25)	
		
		butFrame = tk.Frame(top)
		saveBut = tk.Button(butFrame, text="Save to Desktop")
		saveBut.bind("<Button-1>", self.saveSingle)
		saveBut.qrImg = qrImg
		saveBut.qrData = dataToEncode
		saveBut.pack(padx=10, pady=10, side=tk.LEFT)

		button = tk.Button(butFrame, text="Dismiss", command=top.destroy)
		button.pack(padx=10, pady=10, side=tk.TOP)

		butFrame.pack(padx=10, pady=10)
	
	def saveSingle(self, event):
		paddedImg = Image.new("RGB", (390, 420), "white")
		paddedImg.paste(event.widget.qrImg, (30, 30))
		font = ImageFont.truetype("/usr/share/fonts/ttf/ubuntu-font-family-0.80/UbuntuMono-R.ttf", 14)
		draw = ImageDraw.Draw(paddedImg)
		draw.text((10, 400),event.widget.qrData, font=font, fill=(0,0,0))
		paddedImg.save("/home/pi/Desktop/QRCode1.png")		
		self.showAlert("Saved to the Desktop with filename QRCode1.png")	
	
	def saveDouble(self, event):
		event.widget.qrImg.save("/home/pi/Desktop/QRCode2.png")
		self.showAlert("Saved to the Desktop with filename QRCode2.png")	


class Tab1(tk.Frame):
	
	

	def __init__(self, root):
		tk.Frame.__init__(self, root)
		
		pUtil = PiperUtil()

		printGroup = tk.Frame(self)
		
		qtyFrame = tk.Frame(printGroup)
				
		
		self.walletQuantity = tk.StringVar()
		tk.Label (qtyFrame, text='Number of copies of wallet to print ').pack(side=tk.LEFT,padx=10,pady=10)
		qtyField = tk.Entry(qtyFrame, width=10, textvariable=self.walletQuantity)
		qtyField.pack(side=tk.LEFT, padx=10, pady=10)
		self.walletQuantity.set("1")
		
		qtyFrame.pack()
		
		
		rdoFrame = tk.Frame(printGroup)
		self.remKey = tk.IntVar()
		tk.Label (rdoFrame, text='Remember public key ').pack(side=tk.LEFT,padx=10,pady=10)
		remPubKeyBtn = tk.Radiobutton(rdoFrame, text="Yes", variable=self.remKey, value=1)
		remPubKeyBtn.pack(side=tk.LEFT)
		remPubKeyBtn.select()
		tk.Radiobutton(rdoFrame, text="No", variable=self.remKey, value=2).pack(side=tk.LEFT)
		rdoFrame.pack()
		

		rdoFrame2 = tk.Frame(printGroup)
		self.remPrivKey = tk.IntVar()
		tk.Label (rdoFrame2, text='Remember private key ').pack(side=tk.LEFT,padx=10,pady=10)
		remPrivKeyBtn = tk.Radiobutton(rdoFrame2, text="Yes", variable=self.remPrivKey, value=1)
		remPrivKeyBtn.pack(side=tk.LEFT)
		remPrivKeyBtn.select()
		tk.Radiobutton(rdoFrame2, text="No", variable=self.remPrivKey, value=2).pack(side=tk.LEFT)
		rdoFrame2.pack()

		
		rdoFrame3 = tk.Frame(printGroup)
		self.encKey = tk.IntVar()
		tk.Label (rdoFrame3, text='Encrypt private key ').pack(side=tk.LEFT,padx=10,pady=10)
		tk.Radiobutton(rdoFrame3, text="Yes", variable=self.encKey, value=1, command=pUtil.setEncryptYes).pack(side=tk.LEFT)
		encNoBtn = tk.Radiobutton(rdoFrame3, text="No", variable=self.encKey, value=2, command=pUtil.setEncryptNo)
		encNoBtn.pack(side=tk.LEFT)
		encNoBtn.select()
		rdoFrame3.pack()
		
		
		self.passGroup = tk.LabelFrame(printGroup, text="Encrypted wallet password")
		passFrame = tk.Frame(self.passGroup)
		self.walletPass = tk.StringVar()
		tk.Label (passFrame, text='Enter password: ').pack(side=tk.LEFT,padx=10,pady=10)
		tk.Entry(passFrame, width=10, textvariable=self.walletPass, show="*").pack(side=tk.LEFT,padx=10,pady=10)
		passFrame.pack()
		
		verFrame = tk.Frame(self.passGroup)
		self.verPass = tk.StringVar()
		tk.Label (verFrame, text='Verify password: ').pack(side=tk.LEFT,padx=10,pady=10)
		tk.Entry(verFrame, width=10, textvariable=self.verPass, show="*").pack(side=tk.LEFT,padx=10,pady=10)
		
		verFrame.pack()
		
		self.printButton = tk.Button(printGroup, text='Print', command=pUtil.printWallet)
		
		self.printButton.pack(side=tk.TOP)
		
		
		printGroup.pack(padx=10, pady=10)


class Tab2(tk.Frame):
	def __init__(self, root):
		tk.Frame.__init__(self, root)
		#tk.Label(self, text="Test label2").pack()

		pUtil = PiperUtil()


		bulkGroup = tk.Frame(self)

		bulkQtyFrame = tk.Frame(bulkGroup)

		self.bulkQuantity = tk.StringVar()

		tk.Label (bulkQtyFrame, text='Number of wallets to print using settings from Print Wallet tab ').pack(side=tk.LEFT,padx=10,pady=10)
		tk.Entry(bulkQtyFrame, width=10, textvariable=self.bulkQuantity).pack(side=tk.LEFT,padx=10,pady=10)
		self.bulkQuantity.set(2)
		bulkQtyFrame.pack()

		printBulkButton = tk.Button(bulkGroup, text="Print Bulk", command=pUtil.printBulkWallet)
		printBulkButton.pack()


		bulkGroup.pack(padx=10, pady=10)


class Tab3(tk.Frame):
	def __init__(self, root):
		tk.Frame.__init__(self, root)
		self.viewKeysCanvas = tk.Canvas(self)
		self.viewKeysGroup = tk.Frame(self.viewKeysCanvas)
		self.viewKeysScrollbar = tk.Scrollbar(self, orient="vertical",
								command=self.viewKeysCanvas.yview)
		self.viewKeysCanvas.configure(yscrollcommand=self.viewKeysScrollbar.set)
		self.viewKeysScrollbar.pack(side="right", fill="y")
		self.viewKeysCanvas.pack(fill="both", expand=True)
		self.viewKeysCanvas.create_window(0, 0, window=self.viewKeysGroup, anchor="nw")
		self.viewKeysGroup.bind("<Configure>", self.on_frame_configure)
		self.viewKeysRefs = []
		self.populate()
	
	def populate(self):

		pUtil = PiperUtil()
		decKeyPopup = DecryptedKeyPopup()
		qrPopup = QRPopup()
		con = None
		try:
			con = sqlite3.connect('keys.db3')#'/home/pi/Printer/keys.db3')
			cur = con.cursor()    
			cur.execute("SELECT serialnum, public, private FROM keys")
			rows = cur.fetchall()
			
			for aKey in self.viewKeysRefs:
				aKey.destroy()

			self.viewKeysRefs = []
			
			
			for row in rows:
				aKeyGroup = tk.LabelFrame(self.viewKeysGroup, text="Serial num: "+str(row[0]))
				
				buttonFrame = tk.Frame(aKeyGroup)
				
				reprintBut = tk.Button(buttonFrame, text="Reprint")
				reprintBut.bind("<Button-1>", pUtil.reprint)
				reprintBut.pack(padx=10, side=tk.LEFT)
				reprintBut.serialnum = row[0]
				reprintBut.pubkey = row[1]
				reprintBut.privkey = row[2]

				qrBut = tk.Button(buttonFrame, text="Show QR codes")
				qrBut.pack(padx=10, side=tk.LEFT)
				qrBut.bind("<Button-1>", qrPopup.showPopup)
				qrBut.pack(padx=10, side=tk.LEFT)
				qrBut.serialnum = row[0]
				qrBut.pubkey = row[1]
				qrBut.privkey = row[2]
				
				if(row[1] != ""):
					keyFrame = tk.Frame(aKeyGroup)
					tk.Label(keyFrame, text="Public key: ").pack(padx=10, pady=10, side=tk.LEFT)
					keystr = tk.StringVar()
					tk.Entry(keyFrame, textvariable=keystr, width=52).pack(padx=10, pady=10, side=tk.LEFT)
					keystr.set(row[1])
					keyFrame.pack(padx=10, pady=10, side=tk.TOP)
				if(row[2] != ""):
					keyFrame = tk.Frame(aKeyGroup)
					tk.Label(keyFrame, text="Private key: ").pack(padx=10, pady=10, side=tk.LEFT)
					keystr=tk.StringVar()
					tk.Entry(keyFrame, textvariable=keystr, width=52).pack(padx=10, pady=10, side=tk.LEFT)
					keystr.set(row[2])
					keyFrame.pack(padx=10, pady=10, side=tk.TOP)

					if(len(str(row[2])) > 58):
						#the key is encrypted.  show a button to decrypt it
						aBut = tk.Button(buttonFrame, text="Decrypt Key")
						aBut.bind("<Button-1>", decKeyPopup.showPopup)
						aBut.serialnum= str(row[0])
						aBut.pubkey = row[1]
						aBut.privkey = row[2]
						aBut.pack(padx=10, side=tk.LEFT)
				buttonFrame.pack(padx=10, pady=10)		
				aKeyGroup.pack(padx=10, pady=10)
				self.viewKeysRefs.append(aKeyGroup)
				
				
		except sqlite3.Error, e:
			print "Error %s:" % e.args[0]
			sys.exit(1)
		finally:
			if con:
				con.commit()
				con.close()

	
	def on_frame_configure(self, event):
		"""Reset the scroll region to encompass the inner frame"""
		self.viewKeysCanvas.configure(scrollregion=self.viewKeysCanvas.bbox("all"))





class Tab4(tk.Frame):
	def __init__(self, root):
		tk.Frame.__init__(self, root)

		pUtil = PiperUtil()


		heatTimeFrame = tk.Frame(self)
		tk.Label (heatTimeFrame, text='Heat Time:').pack(side=tk.LEFT,padx=10,pady=10)
		self.heatTime = tk.Scale(heatTimeFrame, from_=30, to=255, length=255, orient=tk.HORIZONTAL)
		self.heatTime.pack(side=tk.LEFT, padx=10, pady=10)
		heatTimeFrame.pack(padx=10, pady=10)
		
		tk.Label(self, text="Greater heat time means a darker print.  The default value for 20 year paper is 120.").pack(padx=10, pady=10)

		
		coinTypeFrame = tk.Frame(self)

		tk.Label(coinTypeFrame, text="Coin type:").pack(side=tk.LEFT, padx=10, pady=10)
		self.coinType = tk.StringVar()

		tk.Radiobutton(coinTypeFrame, text="Bitcoin", variable=self.coinType, value="bitcoin").pack(side=tk.LEFT, padx=5, pady=10)
		tk.Radiobutton(coinTypeFrame, text="Litecoin", variable=self.coinType, value="litecoin").pack(side=tk.LEFT, padx=5, pady=10)

		coinTypeFrame.pack()

		addressPrefixFrame = tk.Frame(self)
		tk.Label(addressPrefixFrame, text="Address prefix").pack(side=tk.LEFT, padx=10, pady=10)
		self.addrPrefix = tk.StringVar()
		tk.Entry(addressPrefixFrame, textvariable=self.addrPrefix).pack(side=tk.LEFT, padx=10, pady=10)
		addressPrefixFrame.pack()
		
		tk.Label(self, text="Address prefix is 1 for bitcoin and L for litecoin or key generation will fail.").pack(padx=10)
		tk.Label(self, text="We do not recommend a prefix longer than 3 characters.  ").pack(padx=10)
		tk.Label(self, text="A prefix just 3 characters long can take up to 30 seconds to generate (for example 1CC).").pack(padx=10)
		tk.Label(self, text="A prefix 4 characters long can take up to 10 minutes to generate (for example 1cat).").pack(padx=10)

		encTypeFrame = tk.Frame(self)

		tk.Label(encTypeFrame, text="Encryption type:").pack(side=tk.LEFT, padx=10, pady=10)
		self.encType = tk.StringVar()

		tk.Radiobutton(encTypeFrame, text="BIP0038", variable=self.encType, value="bip0038").pack(side=tk.LEFT, padx=10, pady=10)
		tk.Radiobutton(encTypeFrame, text="AES", variable=self.encType, value="aes").pack(side=tk.LEFT, padx=10, pady=10)

		encTypeFrame.pack()


		setButton = tk.Button(self, text="Apply settings", command=self.applySettings)
		setButton.pack(padx=10, pady=10)
		tk.Label(self, text="These settings will be stored and used when printing in headless mode as well.").pack(padx=10)
		
		con = None
                try:
                        con = sqlite3.connect('/home/pi/Printer/keys.db3')
                        cur = con.cursor()
                        cur.execute("SELECT heatTime, coinType, addrPrefix, encType FROM piper_settings LIMIT 1;")
                        row = cur.fetchone()
                        self.heatTime.set(row[0])
			self.coinType.set(row[1])
			self.addrPrefix.set(row[2])
			self.encType.set(row[3])
                except sqlite3.Error, e:
                        print("Error %s:" % e.args[0])
                        sys.exit(1)
                finally:
                        if con:
                                con.commit()
                                con.close()
                                    



	def applySettings(self):

		#first, check that BIP0038 and litecoin are not both set
		if(self.coinType.get() == "litecoin" and self.encType.get() == "bip0038"):
			self.showMessage("Error!!","BIP0038 is not compatible with litecoin.  Settings not saved.") 
			self.encType.set("aes")	
			return


		#second, check that prefix is valid
		

		if(self.coinType.get() == "litecoin"):
			if(len(self.addrPrefix.get()) == 0 or self.addrPrefix.get()[0] != "L"):
				self.showMessage("Error!!","Invalid address prefix.  Litecoin addresses must begin with L.") 
				return
			process = Popen(["./vanitygen-litecoin", "-q", "-n", "-L", "-t","1","-s", "/dev/random", self.addrPrefix.get()], stderr=PIPE)
						
		else:
			if(len(self.addrPrefix.get()) == 0 or self.addrPrefix.get()[0] != "1"):
				self.showMessage("Error!!","Invalid address prefix.  Bitcoin addresses must begin with 1.") 
				return

			process = Popen(["./vanitygen", "-q","-n", "-t","1","-s", "/dev/random", self.addrPrefix.get()], stderr=PIPE)

		
		results = process.stderr.read().lower()
		#print results
		if "prefix" in results:		
			prefixValid = False
		else:
			prefixValid = True

		if (prefixValid == False):
			self.showMessage("Error!!","Invalid address prefix.  Not all characters are valid.") 
			return

		con = None
		try:
			con = sqlite3.connect('/home/pi/Printer/keys.db3')
		        con.execute("UPDATE piper_settings SET heatTime=?, coinType=?, addrPrefix=?, encType=?", (self.heatTime.get(),self.coinType.get(), self.addrPrefix.get(),self.encType.get()))
		except sqlite3.Error, e:
			print "Error %s:" % e.args[0]
			sys.exit(1)
		finally:
			if con:
				con.commit()
				con.close()
		self.showMessage("Success!","Settings saved.") 


	def showMessage(self, titleMsg, alertMsg):
		top = tk.Toplevel()
		top.geometry("400x90")
		top.title(titleMsg)

		tk.Label(top, text=alertMsg).pack(padx=10, pady=10)
		
		button = tk.Button(top, text="Dismiss", command=top.destroy)
		button.pack(padx=10, pady=10)









def rClicker(e):
    ''' right click context menu for all Tk Entry and Text widgets
    '''

    try:
        def rClick_Copy(e, apnd=0):
            e.widget.event_generate('<Control-c>')

        def rClick_Cut(e):
            e.widget.event_generate('<Control-x>')

        def rClick_Paste(e):
            e.widget.event_generate('<Control-v>')

        e.widget.focus()

        nclst=[
               (' Cut', lambda e=e: rClick_Cut(e)),
               (' Copy', lambda e=e: rClick_Copy(e)),
               (' Paste', lambda e=e: rClick_Paste(e)),
               ]

        rmenu = tk.Menu(None, tearoff=0, takefocus=0)

        for (txt, cmd) in nclst:
            rmenu.add_command(label=txt, command=cmd)

        rmenu.tk_popup(e.x_root+40, e.y_root+10,entry="0")

    except tk.TclError:
        print ' - rClick menu, something wrong'
        pass

    return "break"


def rClickbinder(r):

    try:
        for b in [ 'Text', 'Entry', 'Listbox', 'Label']: #
            r.bind_class(b, sequence='<Button-3>',
                         func=rClicker, add='')
    except tk.TclError:
        print ' - rClickbinder, something wrong'
        pass







pUtil = PiperUtil()

root = tk.Tk()
sizex, sizey, posx, posy = 700, 475, 100, 10
root.wm_geometry("%dx%d+%d+%d" % (sizex, sizey, posx, posy))
root.title('Piper Wallet')

note = ttk.Notebook(root)
tab1 = Tab1(note)
tab2 = Tab2(note)
tab3 = Tab3(note)
tab4 = Tab4(note)

note.add(tab1, text="Print Wallet")
note.add(tab2, text="Bulk Wallets")
note.add(tab3, text="View Keys")
note.add(tab4, text="Settings")
#note.add(tab4, text = "Encryption Utility")
note.bind_all("<<NotebookTabChanged>>", pUtil.tabChangedEvent)


note.pack(expand=True, fill="both")


rClickbinder(root)

root.mainloop()
