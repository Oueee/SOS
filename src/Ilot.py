import numpy
from individu import Individual
from random import shuffle
from random import choice


class Ilot(object):
    """ Un ilot est compose de :
        - individus: une liste d'individu
        - individu_sum: la somme de la norme de chaque individu
        - nb_individu: le nombre d'individu de l'ilot
    """

    def __init__(self, vector_dimension, ilot_size):
        """ Constructeur de la classe
            Crée un ilot de taille ilot_size avec des individus de dimension vector_dimension
            :param vector_dimension: Dimension d'un individu
            :param ilot_size: Taille d'un ilot
        """
        self.indivuduals = list(map(Individual.make_individual, numpy.random.rand(ilot_size, vector_dimension)))
        self.indivudual_sum = 0
        self.nb_individuals = ilot_size

    def _tournament_(self, chunk, offset, maximum=True):
        """ Réalise un tournoi chunk-aire à partir de l'élément offset de self.individuals
        :param maximum: Précise si l'optimal est un maximum ou un minimum
        :param chunk: Nombre d'individus par tournoi
        :param offset: Indice de démarrage dans la liste d'individus
        """
        chunk_offset = chunk * offset
        # Si le décalage dépasse le maximum, on s'arrête.
        if chunk_offset <= len(self.indivuduals):
            sublist = sorted(self.indivuduals[chunk:chunk_offset], key=lambda x: x.fitness, reverse=maximum)
            both_best = sublist[0:2]
            random_3rd = choice(sublist[2:len(sublist)])

            # Ajoute le vecteur résultant du 2eme meilleur vers le 1er au 3ème vecteur random
            to_added =\
                Individual.make_individual(
                    numpy.add(numpy.subtract(both_best[0], both_best[1]), random_3rd), random_3rd)

            sublist[-1] = to_added
            self.indivuduals[chunk:chunk_offset] = sublist

    def selection(self, chunk=7, parallelized=True):
        """ Réalise la sélection (le x tournoi à réaliser pour parcourir l'ilot complet)
        :param chunk: Nombre d'individus par tournoi
        :param parallelized: Précise si l'on doit utiliser la parallélisation ou non
        """
        # Mixe les individus entre eux avant le tournoi
        shuffle(self.indivuduals)

        self.indivudual_sum = 0
        for i in range(len(self.indivuduals) / chunk):
            self._tournament_(chunk, i)

    def get_size(self):
        """ Getter pour la taille d'un ilot en nombre d'individus """
        return self.nb_individuals

    def get_stats(self):
        """ Getter pour les stats utilisées pour la comparaison """
        dico = {}
        sum_map = list(map(numpy.linalg.norm, self.indivuduals))  # norme des vecteurs
        dico['sum'] = sum(sum_map[:1], sum_map[0])  # somme les normes entre elles
        dico['size'] = self.nb_individuals
        return dico

    def compare(self, stats):
        return self.get_stats()['sum'] > stats['sum']
