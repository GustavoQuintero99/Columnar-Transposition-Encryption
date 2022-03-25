# Char priority class will hold the priority of every character based on its ASCII value
# and hold the column message to be extracted later on 
class CharPriority:
    def __init__(self, char):
        self.message = []
        self.char = char
        self.prio = ord(char)
    def increasePriority(self):
        self.prio += 1
    def appendChar(self, char):
        self.message.append(char)

# Main encryption engine where all the logic of the encryption and decryption will occur
class EncryptEngine:
    def __init__(self, key, message):
        self.charPriorityArray = []
        self.key = key
        self.message = message

    # This method will sort an array of CharPriority objects based on the priority assigned
    # to every value 
    # Time complexity O(n squared) | Space complexity O(n)
    def sortByPriority(self)->None:
        rightPointer = len(self.charPriorityArray) -1
        leftPointer = 0
        while rightPointer != 0:
            if self.charPriorityArray[leftPointer].prio > self.charPriorityArray[leftPointer + 1].prio:
                self.charPriorityArray[leftPointer], self.charPriorityArray[leftPointer + 1] = self.charPriorityArray[leftPointer + 1], self.charPriorityArray[leftPointer]
            leftPointer += 1
            if leftPointer == rightPointer:
                leftPointer = 0
                rightPointer -= 1

    # Will increase the ASCII value or decrease the priority (for this specific situation)
    # running over the priority array once
    # Time complexity O(n) | Space complexity O(1)
    def decreasePriorityOfAnyBiggerThan(self, char)->None:
        char = ord(char)
        for charPrio in self.charPriorityArray:
            if ord(charPrio.char) > char:
                charPrio.increasePriority()

    # Will generate the PriorityArray conserving the original order of the key, but giving
    # the correct priority for each char 
    # Time complexity O(n squared) | Space complexity O(n)
    def generateCharPriorityOfKey(self)->None:
        priorityBooster = 0
        seenChars = set()

        for char in self.key:
            if char in seenChars:
                priorityBooster += 1
                self.decreasePriorityOfAnyBiggerThan(char)
            else:
                seenChars.add(char)

            currentCharPriority = CharPriority(char)
            currentCharPriority.prio += priorityBooster
            self.charPriorityArray.append(currentCharPriority)

    # Main encryption engine, will read the message and use the charPriorityArray to place
    # every char of the message into every column, then extract the information based on 
    # the priority of every column, creating a new file "encryptedmessage.txt"
    # Time complexity O(n squared) | Space complexity O(n)
    def encryptMessage(self)->None:
        index = 0
        maxIndex = len(self.charPriorityArray) - 1
        for char in self.message:
            self.charPriorityArray[index].appendChar(char)
            index += 1
            if index > maxIndex:
                index = 0

        self.sortByPriority()
        newMessage = []
        for each in self.charPriorityArray:
            newMessage += each.message
        newMessage = "".join(newMessage)
        
        newEncryptedFile = open("encryptedmessage.txt", "x")
        newEncryptedFile.write(newMessage)
        newEncryptedFile.close()

    # Main decryption engine, will read the encrypted message, calculate the sorted weighted
    # position of every char of the key, assign the values of the original encrypted position
    # then re accommodate the values on the original key order and extract the decrypted information
    # Time complexity O(n squared) | Space complexity O(n)
    def decryptMessage(self)->None:
        originalKeyWithObject = self.charPriorityArray[:]
        self.sortByPriority()
        columnLength = round(len(self.message) / len(self.key))
        indexOfRow = 0
        indexOfChar = 0

        for char in self.message:
            self.charPriorityArray[indexOfChar].appendChar(char)
            indexOfRow += 1
            if indexOfRow == columnLength:
                indexOfRow = 0
                indexOfChar += 1

        newMessage = []
        indexOfChar = 0
        indexOfRow = 0
        currentChar = 0
        keyLen = len(self.key) - 1
        while indexOfRow <= columnLength:
            if len(originalKeyWithObject[currentChar].message) - 1 < indexOfRow:
                break
            newMessage.append(originalKeyWithObject[currentChar].message[indexOfRow])
            currentChar += 1
            if currentChar == keyLen + 1:
                currentChar = 0
                indexOfRow += 1

        newMessage = "".join(newMessage)
        newDecryptedFile = open("decryptedmessage.txt", "x")
        newDecryptedFile.write(newMessage)
        newDecryptedFile.close()

def main():
    print("*Note that the filename to encrypt a message must be named as 'message.txt'")
    print("*Note that the filename to decrypt a message must be named as 'encryptedmessage.txt' ")
    print("*Note encrypting a file will produce -> 'encryptedmessage.txt'")
    print("*Note decrypting a file will product -> 'decryptedmessage.txt'")
    print("*Note all the files must be within the very same folder that this algorithm is")
    print("")
    operation = input("Type x for encrypt and y for decrypt: ")

    key = open("key.txt", "r")
    key = key.read()

    if len(key) <= 1:
        raise Exception("Key length must be more than 2")

    # Encrypt operation
    if operation == 'x':
        message = open("message.txt", "r")
        message = message.read()
        if len(message) <= 1:
            raise Exception("Length of the message to be encrypted must be at least of 2")
        Engine = EncryptEngine(key, message)
        Engine.generateCharPriorityOfKey()
        Engine.encryptMessage()
    # Decrypt operation
    elif operation == 'y':
        encryptedMessage = open("encryptedmessage.txt", "r")
        encryptedMessage = encryptedMessage.read()
        if len(encryptedMessage) <= 1:
            raise Exception("Invalid size for the encrypted message")
        Engine = EncryptEngine(key, encryptedMessage)
        Engine.generateCharPriorityOfKey()
        Engine.decryptMessage()
    # Invalid input
    else:
        raise Exception("Invalid key for operation")

if __name__ == '__main__':
    main()