# -*- coding: utf-8 -*-

import numpy
from random import shuffle, choice

from src.individu import Individual
from src.Message import MessageBody
from src.Linker import Linker
from src import globals as gb
import multiprocessing

class Ilot(Linker):
    """ Un ilot est compose de :
        - individus: une liste d'individu
        - individu_sum: la somme de la norme de chaque individu
        - nb_individu: le nombre d'individu de l'ilot
    """

    def __init__(self, vector_dimension, ilot_size, function):
        """ Constructeur de la classe
            Crée un ilot de taille ilot_size avec des individus de dimension vector_dimension
            :param function: la fonction ou trouver le minimum global
            :param vector_dimension: Dimension d'un individu
            :param ilot_size: Taille d'un ilot
        """
        self.indivuduals = list(map(Individual.make_individual, numpy.random.rand(ilot_size, vector_dimension)))
        self.function = function
        self.stats = multiprocessing.Array('d', 2)
        self.stats[0] = ilot_size
        
        super(self.__class__, self).__init__()

    def delete(self):
        super(self.__class__, self).delete()
        del gb.ILOTS_LIST[self.id]

    def _tournament_(self, chunk, offset, maximum=True):
        """ Réalise un tournoi chunk-aire à partir de l'élément offset de self.individuals
        :param maximum: Précise si l'optimal est un maximum ou un minimum
        :param chunk: Nombre d'individus par tournoi
        :param offset: Indice de démarrage dans la liste d'individus
        """
        chunk_offset = chunk * offset
        # Si le décalage dépasse le maximum, on s'arrête.
        if chunk_offset + chunk <= len(self.indivuduals):
            sublist = sorted(self.indivuduals[chunk_offset:chunk_offset+chunk], key=lambda x: x.evaluation(self.function), reverse=maximum)
            both_best = [ind.vector for ind in sublist[0:2]]
            random_3rd = choice(sublist[2:len(sublist)]).vector

            # Ajoute le vecteur résultant du 2eme meilleur vers le 1er au 3ème vecteur random
            to_added =\
                Individual.make_individual(
                    numpy.add(numpy.subtract(both_best[0], both_best[1]), random_3rd), random_3rd)

            sublist[-1] = to_added
            self.indivuduals[chunk_offset:chunk_offset+chunk] = sublist

    def selection(self, chunk=7, parallelized=True):
        """ Réalise la sélection (le x tournoi à réaliser pour parcourir l'ilot complet)
        :param chunk: Nombre d'individus par tournoi
        :param parallelized: Précise si l'on doit utiliser la parallélisation ou non
        """
        # Mixe les individus entre eux avant le tournoi
        shuffle(self.indivuduals)

        self.indivudual_sum = 0
        for i in range(len(self.indivuduals) // chunk):
            self._tournament_(chunk, i)

    def get_stats(self):
        """ Getter pour les stats utilisées pour la comparaison """
        self.stats[1] = list(map(numpy.linalg.norm, self.indivuduals))  # norme des vecteurs
        message_body = MessageBody(sum(self.stats[1][:1], self.stats[1][0]),
                                   self.stats[0])

        return message_body

    def compare(self, stats_other):
        stat = self.get_stats()
        if stat.size_ilot > stats_other.size_ilot:
            self.stat[0] += 1
            return -1
        else:
            self.stat[0] -= 1
            return +1

    def process_answer(self, data):
        """ Process the data given back by another ilot.

        :param data: data given back by an ilot
        """
        self.stats[0] += data

