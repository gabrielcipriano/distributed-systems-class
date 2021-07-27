from multiprocessing import Pool

def f(par):
    print('entrou')
    key, value = par
    return value

if __name__ == '__main__':
    m = 10
    processos = 1
    keys = []
    values = []

    for i in range(m):
        keys.append(str(i))
        values.append(i)

    with Pool(processos) as p:
        print(p.map(f, zip(keys,values)))