import globals


class Individual(object):
    """ Un individu est composé de :
        - vector: Un vecteur de dimension n-1 (permettant le calcul du fitness
        - fecondation: Le vecteur de translation avec le troisième indivu ayant servi à sa création
        - fitness: Le fitness de l'individu """

    def __init__(self, vector, fecondation=None, fitness=None):
        """ Constructeur de la classe
        :param vector: Vecteur déjà initialisé représentant un individu
        :param fecondation: Vecteur parent (ayant amené à la création)
        :param fitness: Fitness de l'individu
        """
        self.vector = vector
        self.fitness = fitness
        self.fecondation = fecondation

    def evaluation(self):
        """ Evaluation du fitness d'un individu """
        self.fitness = self.fitness or globals.f(self.vector)
        return self.fitness

    @staticmethod
    def make_individual(vector, fecondation=None):
        return Individual(vector, fecondation)
