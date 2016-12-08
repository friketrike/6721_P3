import random as r
import math as m
import copy

class Model:
    def __init__(self, model_dict=None):
        if model_dict == None:
            self.a = r.randint(-15, 15)
            if self.a == 0:
                self.a_exp = 1
            else:
                self.a_exp = round(r.gauss(1, 2))
            self.b = r.randint(-16, 16)
            self.c = r.randint(0,15)
            if self.c == 0:
                self.c_exp = 1
            else:
                self.c_exp = round(r.gauss(1,2))
        else:
            self.a = model_dict['a']
            self.a_exp = model_dict['a_exp']
            self.b = model_dict['b']
            self.c = model_dict['c']
            self.c_exp = model_dict['c_exp']

    def to_string(self):
        hx2car = lambda x: hex(x)[2] if x >= 0 else hex(x)[0]+hex(x)[3]
        str = '(' +hx2car(self.a) + '^' + hx2car(self.a_exp) +') + ' + hx2car(self.b) + \
              '*sqrt(' +hx2car(self.c) + '^' + hx2car(self.c_exp) + ')\n'
        return str


class Problem:
    def __init__(self, n=None):
        if not n:
            n = 8
        self.iteration = 0
        self.n = n
        self.models = []
        for i in range(n):
            self.models.append(Model())
        self.min_losses = [min(self.loss_test())]
        self.display = False

    @staticmethod
    def transform(model):
        expand_a = model.a**model.a_exp
        expand_c = model.c**model.c_exp
        number = expand_a + (model.b*m.sqrt(expand_c))
        return abs(number)

    def loss_test(self, expression=None):
        if not expression:
            expression = lambda x: x**2 + 2*x - 11
        loss_vals = []
        for model in self.models:
            x = self.transform(model)
            result = expression(x)
            loss_vals.append(abs(result))
        return loss_vals

    def generations(self, n):
        for i in range(n):
            self.generation()
            if self.min_losses[-1] < 1.78e-15:
                print('converged in ', self.iteration)
                break

    def generation(self):
        self.iteration += 1
        loss_vals = self.loss_test()
        poche = max(loss_vals)
        chouette = min(loss_vals)
        idxs = []
        loss_vals_copy = copy.deepcopy(loss_vals)
        for _ in range(m.floor(self.n/2)):
            idx = loss_vals.index(min(loss_vals))
            idxs.append(idx)
            loss_vals[idx] = poche
        the_chosen = []
        for idx in idxs:
            the_chosen.append(self.models[idx])
        self.models = the_chosen
        num_parents = self.models.__len__()
        idxs1 = list(range(num_parents))
        idxs2 = list(range(num_parents))
        r.shuffle(idxs1)
        r.shuffle(idxs2)
        for idx1, idx2 in zip(idxs1, idxs2):
            mama = self.models[idx1]
            papa = self.models[idx2]
            self.models.append(self.recombine(mama, papa))

        self.min_losses.append(chouette)
        if self.display:
            print('Iteration: ', self.iteration, ', best loss: ', chouette)
            print('all losses: ', loss_vals_copy)
            idx = loss_vals_copy.index(min(loss_vals_copy))
            print('and the closest fit is model no ', idx, ' which is ', self.models[idx].to_string())
            expression = lambda x: x ** 2 + 2 * x - 11
            print('plugging the found value into the given expression yields: ',
                  expression(self.transform(self.models[idx])))

    @staticmethod
    def recombine(mama, papa):
        a = mama.a + round(r.gauss(0,2))
        a = a if -15 <= a else -15
        a = a if 15 >= a else 15
        if a == 0:
            a_exp = 1
        else:
            a_exp = papa.a_exp + round(r.gauss(0, 2))
            a_exp = a_exp if -15 <= a_exp else -15
            a_exp = a_exp if 15 >= a_exp else 15
        b = mama.b + round(r.gauss(0,2))
        b = b if -15 <= b else -15
        b = b if 15 >= b else 15
        c = mama.c + round(r.gauss(0,2))
        c = c if 0 <= c else 0
        c = c if 15 >= c else 15
        if c == 0:
            c_exp = 1
        else:
            c_exp = papa.c_exp + round(r.gauss(0, 2))
            c_exp = c_exp if -15 <= c_exp else -15
            c_exp = c_exp if 15 >= c_exp else 15
        model_dict = {'a':a, 'a_exp':a_exp, 'b':b, 'c':c, 'c_exp':c_exp}
        return Model(model_dict)







