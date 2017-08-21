import cv2
import operator
import random
import numpy as np
import matplotlib.pyplot as plt
from scipy import misc

# calculate fitness
def calOstu(th, hist):
    omega1 = float(sum(hist[0:th])) / sum(hist) 
    omega2 = 1 - omega1
    ip = 0
    for i in xrange(th):
        ip += i * hist[i]
    miu1 = float(ip) / sum(hist)
    ip = 0
    for i in xrange(th, 255):
        ip += i * hist[i]
    miu2 = float(ip) / sum(hist)
    miu = miu1 + miu2
    g = omega1 * (miu1 - miu) ** 2 + omega2 * ((miu2 - miu) ** 2)
    return g

# calculate cumulative probability
def calCumPro(totalg, chromosomes):
    newgener = []
    # calculate probability
    for chrom in chromosomes:
        newgener.append([chrom[0], chrom[1] / totalg])
    # calculate  cumulative probability
    for i in xrange(1, len(chromosomes)):
        newgener[i][1] += newgener[i-1][1]
    return newgener

# choose chromosomes to evolve
def chooseChrom(chromosomes):
    _sum = 0
    for i in xrange(len(chromosomes)):
        _sum += chromosomes[i][1]
    chromosomes = calCumPro(_sum, chromosomes)
    ps = []
    # get picking-up probability randomly
    for i in xrange(len(chromosomes)):
        ps.append(random.random())
    newgener = []
    # pick up chromosomes
    for p in ps:
        for chrom in chromosomes:
            if p <= chrom[1]:
                newgener.append(chrom)
                break
            else:
                continue
        continue
    return newgener

# exchange chromosomes
def exchange(exRate, length, chromosomes):
    exNum = int(exRate * len(chromosomes))
    # make sure even number of chromosomes
    if exNum % 2 == 1:
        exNum -= 1
    # pick up random exNum chromosomes to exchange
    ixes = random.sample(xrange(len(chromosomes)), exNum)
    newgener = []
    # copy other chromosomes
    for i in xrange(len(chromosomes)):
        if i not in ixes:
            newgener.append(chromosomes[i])
    # do exchange
    for i in range(0, len(ixes), 2):
        seg_h1 = chromosomes[ixes[i]][0] >> length << length
        seg_t1 = chromosomes[ixes[i]][0] - seg_h1
        seg_h2 = chromosomes[ixes[i+1]][0] >> length << length
        seg_t2 = chromosomes[ixes[i+1]][0] - seg_h2
        newgener.append([seg_h1 + seg_t2, 0])
        newgener.append([seg_h2 + seg_t1, 0])
    return newgener

# varying chromosomes
def vary(varyRate, chromosomes):
    vrNum = int(varyRate * len(chromosomes))
    ixes = random.sample(xrange(len(chromosomes)), vrNum)
    for i in xrange(len(chromosomes)):
        if i in ixes:
            randint = random.randint(0, 31)
            if chromosomes[i][0] > randint:
                chromosomes[i][0] -= randint
            else:
                chromosomes[i][0] = randint - chromosomes[i][0]
# old algorithm, works inefficiently
#    chromosomes[i][0] = (~(chrom - (chrom >> bits << bits)) \
#            & (2 ** bits - 1)) + (chrom >> bits << bits)
    return chromosomes

# binarize image
def binarize(path, th, img):
    binarized_img = [[0 if x > th else 255 for x in r] for r in img]
    bin_path = path.split('.')[1] + '_bin.jpg'
    misc.imsave(bin_path, binarized_img)    
    img = cv2.imread(bin_path, 0)
    return bin_path

# calculate best threshold by a naive way
def naiveFindBestThreshold(path):
    th = 0
    g = 0
    thtemp = 0
    gtemp = 0
    img = cv2.imread(path, 0)
    hist = np.bincount(img.ravel(),minlength=256)
    for thtemp in xrange(256):
        gtemp = calOstu(thtemp, hist)
        if gtemp > g:
            th = thtemp
            g = gtemp
    bin_path = binarize(path, th,img)
    return bin_path, th

def main(path, cnt, population, cross_ratio, vary_ratio):
    img = cv2.imread(path, 0)
    hist = np.bincount(img.ravel(),minlength=256)
    generation = 1
    s = random.sample(xrange(256), population)
    chromosomes = [[x, 0] for x in s]
    _sum = 0
    length = 4
    lstbest = 0
    count = 0
    exRate = cross_ratio
    varyRate = vary_ratio
    degen = True
    while True:
        print "generation %d:" % generation
        for i in xrange(len(chromosomes)):
            # show chromosome status
            print '{0:08b}'.format(chromosomes[i][0])
            chromosomes[i][1] = calOstu(chromosomes[i][0], hist)
            if chromosomes[i][1] >= lstbest:
                # A better chromosome appears
                if chromosomes[i][1] > lstbest:
                    count = 0
                # not worse
                lstbest = chromosomes[i][1]
                th = chromosomes[i][0]
                degen = False
        # if worse, use last generation
        if degen == True:
            for i in xrange(len(chromosomes)):
                chromosomes[i][0], chromosomes[i][1] = lstgen[i][0], lstgen[i][1]
        else:
            # default set degeneration to True
            degen = True
        # best chromosome stay fixed for 1000 generations, terminate loop
        if count == cnt:
            break
        # calculate sum of between-class variance
        count += 1
        # backup this generation
        lstgen = []
        for chromo in chromosomes:
            lstgen.append([chromo[0], chromo[1]])
        # choose chromosomes to exchange
        chromosomes = chooseChrom(chromosomes)
        # do exchange
        chromosomes = exchange(exRate, length, chromosomes)
        # do vary
        chromosomes = vary(varyRate, chromosomes)
        generation += 1
    print "best threshold: " + str(th)
    bin_path = binarize(path, th, img)
    return bin_path, generation, th

if __name__ == '__main__':
    # test
    main('rice.jpg', 200, 16, 0.8, 0.2)
