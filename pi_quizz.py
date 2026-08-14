

class PiQuizz:
    """ objectif: class qui permet de gerer sans affichage plusieur mode de jeu en rapport avec les décimale de pi
    """

    def __init__(self, param: dict = {"type": "classic", "live": 3}, end_func = lambda x: print(x)):
        """ objectif: initialiser la classe en lui transmettant le type de partie et ses paramètre
        - param (dict): dictionnaire contenant toutes les info concernant la partie lancé, sous ce format =>
        {type: ..., len: (..., ...), jump: ..., live: ..., time: ...}
        => si des clé ne sont pas présente, cela veut dire qu'elles n'ont pas d'importance
        
        - end_func (fonction avec soit True ou False): finction appelé en fin de  partie (True si victoire et False si échec)
        """

        self.end_func = end_func
        self.param = param

        self.PI = "1415926535897932384626433832795028841971693993751059209749445923078164062862089986280348253421170679"

        self.pos = self.param.get("len", [0])[0]
        self.limit = self.param.get("len", (0, None))[1]
        self.jump = self.param.get("jump", 0)
        self.live = self.param.get("live", 3)

    def get_previus_digits(self, num_of_digit: int = 1):
        """ objectif: renvoyer les digit précdent à celui que l'on devine en ce moment
        param:
            - num_of_digit (int > 0): le nombre digit à renvoyer
        renvoie: les num_of_digit précédent  
        """

        assert type(num_of_digit) == int, "num_of_digit doit être un entier"
        assert num_of_digit > 0, "num_of_digit doit être strictement positif"
        
        if self.pos <= num_of_digit:
            return self.PI[:self.pos]
        return self.PI[self.pos - num_of_digit: self.pos]
    
    def input(self, user_input: str):
        """ objectif: récupérer l'input de l'user et vérifier s'il est correct
        param:
            - user_input (digit type str, len = 1): réponse de l'utilisateur
        
        aucun renvoie 
        """

        assert type(user_input) == str, "user_input doit être un str"
        assert len(user_input) == 1, "la longueur de user_input doit être de 1"
        assert user_input.isdigit(), "user_input doit être un str de digit"

        num = self.PI[self.pos]
        if num == user_input:
            self.pos += 1
            if self.pos == self.limit:
                self.end_func(True)
            else:
                return True
        else:
            self.live -= 1
            if self.live == 0:
                self.end_func(False)
            else:
                return False

        