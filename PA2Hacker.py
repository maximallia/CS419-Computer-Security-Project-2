import sys, string

LETTERS =      'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
freq_letters = 'ETAOINSRHDLUCMFYWGPBVKXQJZ'

found = {} #letters found by deduction
answer = ''

def main():

    encrypted_message = ''

    stored_letters= {}

    with open('words.txt', 'r') as wordL:
        temp = wordL.read()
        wordList = temp.split('\n')

    if len(sys.argv) == 1:
        file_p = input("Enter file path: ")
        with open(file_p, 'r') as f:
            encrypted_message = f.read()
            

    else: #filepath entered in command
        with open(sys.argv[1], 'r') as f:
            encrypted_message = f.read()

    #print(encrypted_message)

    #appeared = {}

    findA_I(encrypted_message)
    print(found)

    for index, char in enumerate(encrypted_message):

        #print("index: ")
        if char.upper() in LETTERS:
            if char.lower() not in stored_letters:
                stored_letters[char.lower()] = 1
            else:
                stored_letters[char.lower()] += 1

        else: #a symbol, next line, number
            continue

    #print(stored_letters)



    #sort the dictionary by greatest value
    sort_letters = sorted(stored_letters, key = stored_letters.get, reverse=True)
    print(sort_letters)

    set_E(sort_letters)
    print(found)

    message_arr = formWordArr(encrypted_message)
    #print(message_arr)

    deduce_one(message_arr, wordList)
    print(found)

    translate = decryptMessage(sort_letters, freq_letters, encrypted_message)

    #print(wordList[0])
    tryWord(sort_letters, message_arr, wordList)

    print(found)

    final = matchLetters(LETTERS)

    print('\nKey produced:')
    print(final)

    #only for tests
    #REMEMBER TO ''' when submitting
    print('Actual key:')
    key_sol = 'QWERTYUIOPASDFGHJKLZXCVBNM'

    print(key_sol)

    results = letter_acc(final, key_sol)

    print('\nDifference between expected to actual:')
    print(results)

    #print(translate)
    return



def letter_acc(final, key):

    total = 0

    for i in range(len(key)):

        if key[i] == final[i]:
            total+=1
    
    return total/len(key)



def matchLetters(LETTERS):

    final = ''
    flag = 0
    for char in LETTERS:
        for i in found:
            flag = 0
            if found[i].upper() == char.upper():
                final += i
                flag=1
                break
        #if missing
        if flag==0:
            final+='_'
    
    return final



def missingWord(message_arr):

    missing_word = {}
    missing_letter = {}

    temp = ''

    #print(message_arr)

    for word in message_arr:

        translated = ''
        end = len(word)

        for char in word:

            if char.upper() in found:
                translated += found[char.upper()]
                continue

            else:

                translated += '_'

                temp = char

                if char.upper() not in missing_letter:
                    missing_letter[char.upper()] = 1

                elif char.upper() in missing_letter:
                    missing_letter[char.upper()] += 1

                #print(missing)
        
        if '_' in translated and translated not in missing_word:
            missing_word[translated] = temp.upper()
        
        #print(missing_word)
        #print(missing_letter)

    missing_letter = sorted(missing_letter, key = missing_letter.get, reverse=True)

    return missing_word, missing_letter


def find_key():

    #find missing key
    no_key = ''
    flag = 0
    for letter in  LETTERS:
        for char in found:
            if found[char.upper()] == letter.upper():
                flag = 1
                break
            
        if flag == 1:
            flag = 0
            continue
        else:
            no_key += letter.upper()
    
    return no_key


#set the order of comparing missing words
#groups thme with similar missing letter
#start with words with only one letter missing
def set_first(missing_word):

    first = {}
    for word in missing_word:

        total_missing = 0
        #check number of '_'
        for i in word:
            if i == '_':
                total_missing += 1
                #print(total_missing)

        if total_missing != 1:
            continue
        else:
            first[word] = missing_word[word]
    
    first = {key: first[key] for key in sorted(first, key = lambda ele: min(first[ele]),
       reverse = False)}
    return first


#check for names in list
def checkNames(temp_word, wordList, keys):

    name_list=[]
    flag =0
    for word in temp_word:

        for key in keys:
            temp = word.replace('_', key)
            #print(temp)
            for target in wordList:
                if target.upper() == temp.upper():
                    flag = 1
                    break
        if flag==0:
            name_list.append(word)

        else:
            flag= 0

    return name_list


#inputs possible letter to rest of miss_words in list
#if works return 1
# fails, return 0
#skip names
def checkLetter(test_word, wordList, temp_letter, name_list):

    total = 0
    score = 0

    flag = 0

    name_found=0

    new_word = []



    for word in test_word:

        if name_list != []:
            for name in name_list:
            
                if word.upper() == name.upper():
                    name_found = 1
                    break
        
        if name_found == 1:
            name_found = 0
            continue

        else:
            new_word.append(word)

    for word in new_word:

        total += 1

        if flag == 0:
            temp = word.replace('_', temp_letter)

            #print(temp)

            works=0

            for target in wordList:
                if temp.upper() == target.upper():


                    works = 1
                    score+=1

                    break
            
            if works==0:

                continue

    
        elif flag == 1:
            flag = 0

    if score/total < 0.90:
        works = 0

    else:
        works = 1

    return works


def tryWord(sort_letters, message_arr, wordList):

    if len(found)==len(LETTERS):
        return

    #find list of words with missing letters
    missing_word, missing_letter = missingWord(message_arr)

    print('\n MISSING WORD:')
    print(missing_word)
    print('\n MISSING_letter\n')
    print(missing_letter)
    print('\n FOUND:')
    print(found)
    
    no_key = find_key()

    #keys all found

    print('no_key')
    print(no_key)
    print()

    #no more missing words and letter
    #locate the unused encrypted letter
    ender = 0
    if missing_word == {} and missing_letter==[]:

        temp_letters = LETTERS
        for char in found:
            if char in temp_letters.upper():


                temp_letters = temp_letters.replace(char.upper(), '')
        
        if len(no_key) == 1:
            found[temp_letters.upper()] = no_key

            return
        
        elif len(no_key)>1:
            i=0
            for char in temp_letters:
                found[char.upper()] = no_key[0]
                i+=1

                if i == len(no_key):
                    print('ERROR! found words do not match no_key')
                
            return
        
        return


    #start with letter with most missing
    #find word with least missing letter
    first = set_first(missing_word)


    print('\n FIRST:')
    print(first)

    prev_letter = ''
    
    test_word = {}


    #find most common single _ word
    track={}
    for key,value in first.items():
        if value not in track and key.count('_')==1:
            track[value]=0
        else:
            track[value]+=1
    
    prev_letter = max(track, key=track.get)
    print('\n TARGET_LETTER')
    print(prev_letter)

    #create dict of target_letter with most single _
    
    for word in first:
        
        if first[word]== prev_letter and test_word == {}:

            print(word)
            list = [word]

            test_word[prev_letter] = list

        elif prev_letter == first[word]:
            test_word[prev_letter].append(word)
        
        elif test_word != {} and prev_letter != first[word]:
            break

    print('TEST_WORD:')
    print(test_word)
    print()

    temp_letter = ''

    #for key in no_key: 

    result = 0

    skip=0

    #for names not in word.txt

    temp_list =test_word[prev_letter]

    name_list = []

    name_list = checkNames(temp_list, wordList, no_key)



    for word in temp_list:

        for key in no_key:

            temp_letter = ''

            
            for target in wordList:

                if len(word) == len(target):

                    temp_word = word.replace('_', key)

                    if temp_word.upper() == target.upper():

                        temp_letter = key
                        #print(temp_letter)

                        if len(found)==len(LETTERS):
                            return
 
                        result = checkLetter(temp_list, wordList, temp_letter, name_list)
                        #print(result)

                        if result==1:
                            found[prev_letter.upper()] = temp_letter

                            #print(found)
                            
                            result=0

                            tryWord(sort_letters, message_arr, wordList)
            


    return


#make message into list format
def formWordArr(message):

    new =''

    for char in message:
        if char.upper() in LETTERS:
            new+=char
        else:
            new += ' '
        

    wordArr = new.split()

    return wordArr


def findA_I(encrypted_message):

    prev = ''
    next_ = ''
    temp = ''

    for index, char in enumerate(encrypted_message):
        #print("index: ")
        if char.upper() in LETTERS:

            if index > 0:
                prev = encrypted_message[index-1]
                #print(prev)

            if index < (len(encrypted_message) - 1):
                next_ = encrypted_message[index+1]


            if prev==' ' and next_== ' ': 
                if char.islower(): # most likely to be 'a'
                    found[char.upper()] = 'A'
                    #appeared[char.lower] = 0 #0=a

                    
                
                elif char.isupper() and found!={}: #is 'a' there, most likely to be 'I'
                    found[char.upper()] = 'I'
        
        if 'A' in found and 'I' in found:
            break


def set_E(sorted): #E is usually the most common letter in any article
    found[sorted[0].upper()] = 'E'


def deduce_one(word_Arr, wordList):

    arr = word_Arr
    ret= {}
    flag = 0

    turn = 0

    a=0
    b=0
    c=0
    d=0
    e=0
    f=0
    g=0
    h=0
    i=0
    j=0
    k=0
    l=0
    m=0
    n=0
    o=0
    p=0
    q=0
    r=0
    s=0
    t=0
    u=0
    v=0
    w=0
    x=0
    y=0
    z=0


    #in case we missed any letters
    #run the algor 50 times

    for word in arr:
        if len(word) == 2:

            #search for 2 letter (at) with A, E (the), to deduce
            #start with A in beginning
            #most common 2 letter 'A_' = AS,AT
            if word[0].upper() in found:
                if found.get(word[0].upper()) == 'A' and a==0:
                    ret[word[1].upper()] = "ST"
                    a=1
                    break
    if ret != {}:
        #print(ret)
        for word in arr:
            if len(word) == 3: #THE

                if word[2].upper() in found and found.get(word[2].upper()) == 'E':
                    if word[0].upper() in ret:
                        if ret.get(word[0].upper())[1].upper() == 'T' and t ==0 and h==0:
                            found[word[0].upper()] = 'T'
                            found[word[1].upper()] = 'H'
                            t=1
                            h=1
                            break

    #find S
    #sat, so
    for word in arr:
        if len(word) == 3:

            #search for 2 letter (at) with A, E (the), to deduce
            #start with A in beginning
            #most common 2 letter 'A_' = AS
            if word[1].upper() in found:
                if found.get(word[1].upper()) == 'A' and found.get(word[2].upper()) == 'T' and word[0].upper() not in found and s==0:
                    found[word[0].upper()] = 'S'
                    s=1
                    break
        elif len(word) == 2:
            if word[1].upper() in found:
                if found.get(word[1].upper()) == 'O' and word[0].upper() not in found and s==0:
                    found[word[0].upper()] = 'S'
                    s=1
                    break


    

    #find O
    # too, to
    for word in arr:
        if len(word) == 3:
            if found.get(word[0].upper()) == 'T':
                if word[1].upper() not in found and word[1].upper() == word[2].upper():

                    found[word[1].upper()] = 'O'
                    o=1
                    flag = 1
                    break
        if flag==1:
            flag = 0    
            break   



    #find N
    #then
    for word in arr:

        if len(word) == 4:
            if found.get(word[0].upper()) == 'T' and found.get(word[1].upper()) == 'H'and found.get(word[2].upper()) == 'E' :
                if word[0].upper() not in found and n==0:
                    found[word[0].upper()] = 'N'
                    n=1
                    break


    # to find F
    #if, of
    for word_f in arr:
        if len(word_f)==2:
            if word_f[0].upper() in found:
                if found.get(word_f[0].upper()) == 'O' and f==0:
                    if word_f[1].upper() not in found:

                        for word_f2 in arr:
                            if word_f2[0].upper() in found:
                                if found.get(word_f2[0].upper()) == 'I' :

                                    if word_f2[0].upper() == word_f[0].upper():
                                        found[word_f2[0].upper()] = 'F'
                                        f=1
                                        flag=1
                                        break
        if flag==1:
            flag = 0
            break

    #find R
    #nor, more
    for word in arr:
        if len(word) == 3:

            if word[0].upper() in found:
                if found.get(word[0].upper()) == 'N' and found.get(word[1].upper()) == 'O' and word[2].upper() not in found and r==0 and w==1:
                    found[word[2].upper()] = 'R'
                    r=1
                    break
                elif found.get(word[0].upper()) == 'M' and found.get(word[1].upper()) == 'O' and found.get(word[3].upper()) == 'E' and word[2].upper() not in found and r==0:
                    found[word[2].upper()] = 'R'
                    r=1
                    break

    #find D
    #and
    for word in arr:
        if len(word) == 3:

            if word[0].upper() in found:

                if found.get(word[0].upper()) == 'A':
                    #print(found.get(word[0].upper()))

                    if found.get(word[1].upper()) == 'N':
                        #print(found.get(word[1].upper()))

                        if word[2].upper() not in found and d==0:
                        
                            found[word[2].upper()] = 'D'
                            d=1
                            break


    #find U
    #our, out
    for word in arr:
        if len(word) == 3:
            if word[0].upper() in found:
                if found.get(word[0].upper()) == 'O' and found.get(word[2].upper()) == 'R' and u==0:
                    if word[1].upper() not in found:
                        found[word[1].upper()] = 'U'
                        u=1
                        break
                elif found.get(word[0].upper()) == 'O' and found.get(word[2].upper()) == 'T' and u==0:
                    if word[1].upper() not in found:
                        found[word[1].upper()] = 'U'
                        u=1
                        break

    #find B
    #but
    for word in arr:
        if len(word) == 3:
            if word[1].upper() in found:
                if found.get(word[1].upper()) == 'U' and found.get(word[2].upper()) == 'T' and b==0 and p==1:
                    if word[0].upper() not in found:
                        found[word[0].upper()] = 'B'
                        b=1
                        break
    
    #find V
    #have
    for word in arr:
        if len(word) == 4:
            if word[0].upper() in found:
                if found.get(word[0].upper()) == 'H' and found.get(word[1].upper()) == 'A' and found.get(word[3].upper()) == 'E' and v==0:
                    if word[2].upper() not in found:
                        found[word[2].upper()] = 'V'
                        v=1
                        break

    #find W
    #how, new, now
    flag=0
    for word in arr:
        if len(word) == 3:
            if word[1].upper() in found:
                if found.get(word[0].upper()) == 'H' and found.get(word[1].upper()) == 'O' and w==0:
                    #print(word)
                    if word[2].upper() not in found:
                        flag = 1

                elif found.get(word[0].upper()) == 'N' and found.get(word[1].upper()) == 'E' and w==0:
                    #print(word)
                    if word[2].upper() not in found:
                        flag = 1
                
                if flag==1:
                    found[word[2].upper()] = 'W'
                    flag=0
                    w=0
                    break

    #find M
    #from (very common)
    flag=0
    for word in arr:
        if len(word) == 4:
            if word[2].upper() in found:
                if found.get(word[0].upper()) == 'F' and found.get(word[1].upper()) == 'R' and found.get(word[2].upper()) == 'O' and m==0:
                    #print(word)
                    if word[3].upper() not in found:
                        found[word[3].upper()] = 'M'
                        m=1
                        break


    #find Y
    #yet (collide with get), my, by(works cause the other letters found)
    flag=0
    for word in arr:
        if len(word) == 2:
            if word[0].upper() in found:
                if found.get(word[0].upper()) == 'M' and y==0:
                    #print(word)
                    if word[1].upper() not in found:
                        flag = 1
                        
        
            elif word[0].upper() in found:
                if found.get(word[0].upper()) =='B' and y==0:
                    if word[1].upper() not in found:
                        flag = 1
                        
        if flag ==1:
            found[word[1].upper()] = 'Y'
            flag=0
            y=1
            break

    
    #find G
    #get, go, got
    flag=0
    for word in arr:
        
        if len(word) == 4:
            if word[1].upper() in found:
                if found.get(word[1].upper()) == 'O' and found.get(word[2].upper()) == 'O' and found.get(word[3].upper()) == 'D' and g==0:
                    #print(word)
                    if word[0].upper() not in found:
                        flag = 1
        
        elif len(word) == 2:
            if word[1].upper() in found:
                if found.get(word[1].upper()) == 'O' and g==0 and n==1:
                    #print(word)
                    if word[0].upper() not in found:
                        flag = 1
                        
        elif len(word) == 3:
            if word[1].upper() in found:
                if found.get(word[2].upper()) == 'T' and found.get(word[1].upper()) == 'O' and g==0 and n==1 and s==1:
                    #print(word)
                    if word[0].upper() not in found:
                        flag = 1

        elif len(word) == 3:
            if word[1].upper() in found:
                if found.get(word[2].upper()) == 'T' and found.get(word[1].upper()) == 'E' and g==0 and n==1 and s==1:
                    #print(word)
                    if word[0].upper() not in found:
                        flag = 1

        if flag ==1:
            found[word[0].upper()] = 'G'
            flag=0
            g=1
            break
    


    #find P
    #up, also common, but need U
    for word in arr:
        if len(word) == 2:
            if word[0].upper() in found:
                if found.get(word[0].upper()) == 'U' and u==0:
                    #print(word)
                    if word[1].upper() not in found:
                        found[word[1].upper()] = 'P'
                        u=1
                        break


    #find L
    # all, will
    for word in arr:
        if len(word) == 3:
            if word[0].upper() in found:
                if found.get(word[0].upper()) == 'A':
                    
                    #not D
                    if word[1].upper() not in found and word[1].upper()==word[2].upper() and l==0:
                        found[word[1].upper()] = 'L'
        elif len(word) == 4:
            if word[1].upper() in found:
                if found.get(word[0].upper()) == 'W' and found.get(word[1].upper()) == 'I' and l==0:
                    
                    #not E
                    if word[2].upper() not in found and word[2].upper()==word[3].upper():
                        found[word[2].upper()] = 'L'
                        l=1
                        break

    #find K
    #know, knew
    for word in  arr:
        if len(word) >= 4:

            if word[1].upper() in found:
                if found.get(word[1].upper()) == 'N' and found.get(word[3].upper()) == 'W' and (found.get(word[2].upper()) == 'O' or found.get(word[2].upper()) == 'E') and k==0:
                    #print(word)
                    if word[0].upper() not in found:
                        found[word[0].upper()] = 'K'
                        k=1
                        break

    return


def decryptMessage(sorted, freq, message):

    decipher = ''
    charsA = sorted
    charsB = message

    convert = freq

    final = ''

    for symbol in message:
        if symbol.lower() in charsA:
            symIndex = charsA.index(symbol.lower())
            #print(symIndex)
            
            
            for letter in found:
                if convert[symIndex] == found.get(letter):
                    symIndex += 1
                    break

            if symbol.upper() in found : #the char is 'A' or I
                #print(found.get(symbol))
                if symbol.isupper():
                    decipher += found.get(symbol.upper()).upper()
                else:
                    
                    decipher += found.get(symbol.upper()).lower()

            elif symbol.isupper():
                decipher += convert[symIndex].upper()

            else:
                decipher += convert[symIndex].lower()
        else:
            # symbol is not in LETTERS, just add it translated += symbol
            decipher += symbol
            
    
    return decipher, final


if __name__ == "__main__":
    main()
