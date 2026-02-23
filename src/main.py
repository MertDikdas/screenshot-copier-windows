from src.sender import handleSender
from src.reciever import handleReciever

def main():
    choice = "A"
    while(choice!="S" and choice!="R"):
        choice = input("Are you sender or reciever(S/R)")
    if choice=="S":
        handleSender()
    elif choice=="R":
        handleReciever()
    

if __name__ == "__main__":
    main()