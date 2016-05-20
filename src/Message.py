class Message:
    class Types(object):
        stat_transmission = 1
        answer = 2
        end = 3

    def __init__(self, id_sender, type_msg, data=None):
        self.id_sender = id_sender
        self.type = type_msg
        self.data = data


class MessageBody(object):
    def __init__(self, size_ilot, nb_individuals):
        self.size_ilot, = size_ilot
        self.nb_individuals = nb_individuals
