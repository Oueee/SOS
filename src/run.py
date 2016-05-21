import Ilot


if __name__ == "__main__":
    ilot = Ilot.Ilot(2, 14)
    ilot.selection()
    indis = ilot.indivuduals
    print([indi.evaluation() for indi in indis])
