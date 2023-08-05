from .algorytm import sprawdz

def all(a, b, c):
        plus(a, b)
        minus(a, b)
        razy(a, b)
        przez(a, b)
        reszta(a, b)
        kwadrat(a)
        dzieleniebez(a, b)
        najwieksze(a, b, c)
        najmniejsze(a, b, c)
        sprawdz(a, b)

def plus(n1, n2):
        print(n1 + n2)

def minus(n1, n2):
        print(n1 - n2)

def razy(n1, n2):
        print(n1 * n2)

def przez(n1, n2):
        print(n1 / n2)

def reszta(n1, n2):
        print(n1 % n2)

def kwadrat(n1):
        print(n1 * n1)

def dzieleniebez(n1, n2):
        print(n1 // n2)
    
def najwieksze(n1, n2, n3):
        list = [n1, n2, n3]
        print(f"Najwieksza liczba to: {max(list)}")

def najmniejsze(n1, n2, n3):
        list = [n1, n2, n3]
        print(f"Najmniejsza liczba to: {min(list)}")