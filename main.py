#LINKEDQUEUE med peek() function
class Node:
    def __init__(self, value, next_node=None):
        self.value = value
        self.next = next_node

class LinkedQueue:
    def __init__(self):
        self.first = None
        self.last = None

    def enqueue(self, item):
        new_node = Node(item)
        if self.is_empty():
            self.first = new_node
        else:
            self.last.next = new_node
        self.last = new_node

    def dequeue(self):
        if self.is_empty():
            return None
        value = self.first.value
        self.first = self.first.next
        if self.first is None:
            self.last = None
        return value

    def is_empty(self):
        return self.first is None

    #peek() metod
    def peek(self):
        "Titta på första värdeti kön utan att plocka ut det"
        if self.is_empty():
            return None
        return self.first.value

    #Eget Exception method
class Syntaxfel(Exception):
    "Kastas när inmatning bryter mot BNF-regler"
    pass

#Huvudfunktioner
"""När inmatning (tex Fe12) kommer in, anropas read_group() den kommer anropa read_atom(), som direkt anropar read_LETTER() (F).
Sedan read_atom() ser att nästa tecken e är liten boksta och anropar då read_letter().
read_group() ser att nästa tecken 1 är en siffra och anropar read_num() som konsumerar 12
"""
def read_group(q):
    """ <group> ::= <atom> | <atom><num> """
    read_atom(q)
    #Om nästa tecken är en siffra, ska vi läsa ett nummer
    char= q.peek()
    if char is not None and char.isdigit():
        read_num(q)

def read_atom(q):
    """ <atom>  ::= <LETTER> | <LETTER><letter> """
    read_LETTER(q)
    #Tjuvkika: Om nästa tecken är en liten bokstav, hör den till atomen
    char = q.peek()
    if char is not None and char.islower():
        read_letter(q)

def read_LETTER(q):
    """ <LETTER>::= A | B | C | ... | Z """
    char = q.peek()
    if char is not None and char.isupper():
        q.dequeue() #Bokstaven är godkänd, plocka ut ur kön.
    else:
        #Om det är intee en stor bokstav kastas ett fel
        #Tecken ligger kvar i kön så det kan skriva ut i felmeddelandet¨
        raise Syntaxfel("Saknad stor bokstav vid radslutet")

def read_letter(q):
    """ <letter>::= a | b | c | ... | z """
    char = q.peek()
    #Anropa om man vet det är litet bokstav
    if char is not None and char.islower():
        q.dequeue()

def read_num(q):
    """ <num>   ::= 2 | 3 | 4 | ... """
    #Enligt labbeskrivningen (t.ex. H01011) ger en inledande 0:a direkt fel.
    #Vi plockar ut nollan så att resten av strängen (t.ex. 1011) blir kvar i kön.
    if q.peek() == '0':
        q.dequeue()
        raise Syntaxfel("För litet tal vid radslutet")
        
    num_str = ""
    # Så länge det finns siffror kvar i kön, plocka ut dem och bygg vårt tal
    while q.peek() is not None and q.peek().isdigit():
        num_str += q.dequeue()
        
    #När vi läst hela talet, kollar vi om det är >= 2
    if int(num_str) < 2:
        raise Syntaxfel("För litet tal vid radslutet")

#HJÄLPFUNKTION: Bygger kön och fångar fel
import unittest
def check_syntax(molekyl_str):
    """
    Lägger in molekyler i kön, kör syntaxkontrollen och returnerar
    rätt svarsträng enligt labbets tabell
    """
    q = LinkedQueue()
    for char in molekyl_str:
        q.enqueue(char)
    try:
        read_group(q)
        return "Formeln är syntaktiskt korrekt"
    except Syntaxfel as fel:
        #Om ett fel kastas, plockar ut allt som finns i kön
        rest=""
        while not q.is_empty():
            rest += q.dequeue()
        #Om det finns tecken kvar (utanför kön), lägger vi en mellanslag och tecken
        if  rest:
            return str(fel) + " " + rest
        else:
            return str(fel)
        
#TESTPROGRAMMET
class SyntaxTest(unittest.TestCase):

    def test_korrekta_molekyler(self):
        "Giltiga Inmatningar från tabellen"
        self.assertEqual(check_syntax("H2"), "Formeln är syntaktiskt korrekt")
        self.assertEqual(check_syntax("P21"), "Formeln är syntaktiskt korrekt")
        self.assertEqual(check_syntax("Ag3"), "Formeln är syntaktiskt korrekt")
        self.assertEqual(check_syntax("Fe12"), "Formeln är syntaktiskt korrekt")
        self.assertEqual(check_syntax("Xx5"), "Formeln är syntaktiskt korrekt")
        self.assertEqual(check_syntax("H10100"), "Formeln är syntaktiskt korrekt")

    def test_saknad_stor_bokstav(self):
        """ Testar felaktiga inmatningar som börjar med fel tecken. """
        self.assertEqual(check_syntax("a"), "Saknad stor bokstav vid radslutet a")
        self.assertEqual(check_syntax("cr12"), "Saknad stor bokstav vid radslutet cr12")
        self.assertEqual(check_syntax("8"), "Saknad stor bokstav vid radslutet 8")
        self.assertEqual(check_syntax("1011"), "Saknad stor bokstav vid radslutet 1011")

    def test_for_litet_tal(self):
        """ Testar inmatningar där siffran på slutet är < 2 eller börjar på 0. """
        self.assertEqual(check_syntax("Cr0"), "För litet tal vid radslutet")
        self.assertEqual(check_syntax("Pb1"), "För litet tal vid radslutet")
        self.assertEqual(check_syntax("H01011"), "För litet tal vid radslutet 1011")
        self.assertEqual(check_syntax("K01"), "För litet tal vid radslutet 1")
"""
unittest.TestCase är inbbygd i python för att köra tester, Metoder test_... körs auto när du kör filen
self.assertEqual(A, B) kontrollerar värdet A är exakt samma som B. Vi jämför vad vår (check_syntax) producerar med facit
från tabellen i instruktionerna
"""
#Provkör testprogrammet
if __name__ == '__main__':
    unittest.main()