import sys, os, re, copy
LETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
def main():
    
    myMessage = ''
    #'H&M, a Swedish fast-fashion retailer, faces the most immediate trouble. As of March 30th, a week after it was attacked online, its garments were still unavailable on China’s most popular e-commerce apps. Its stores have disappeared from smartphone maps. Landlords in several shopping malls have terminated its leases. Its Chinese business, worth $1bn in revenues, representing 5% of its global sales in 2020, is in jeopardy.'
    #'To be, or not to be, that is the question.'

           #'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    myKey = 'QWERTYUIOPASDFGHJKLZXCVBNM'

    if len(sys.argv) == 1:
        file_p = input("Enter file path: ")
        with open(file_p, 'r') as f:
            myMessage = f.read()
            

    else:
        with open(sys.argv[1], 'r') as f:
            myMessage = f.read()

    checkValidKey(myKey)

    translated = encryptMessage(myKey, myMessage)

    print(translated)
    
def checkValidKey(key):
    keyList = list(key)
    lettersList = list(LETTERS)
    keyList.sort()
    lettersList.sort()
    if keyList != lettersList:
        sys.exit('This is not a valid monoalphabetic substitution cipher key!')
        
def encryptMessage(key, message):
    translated = ''
    charsA = LETTERS
    charsB = key
    for symbol in message:
        if symbol.upper() in charsA:
            symIndex = charsA.find(symbol.upper())
            if symbol.isupper():
                translated += charsB[symIndex].upper()
            else:
                translated += charsB[symIndex].lower()
        else:
            # symbol is not in LETTERS, just add it translated += symbol
            translated += symbol
            
    return translated



if __name__ == "__main__":
    main()