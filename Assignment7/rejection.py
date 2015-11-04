import helpers
from random import random

print("Rejection Sampling\n")

#raw_samples = helpers.getSamples()
samples = []

raw_samples = []
for x in range(100000):
    raw_samples.append(random())


for i in range(len(raw_samples)):
    if (i) % 4 == 0:
        sample = {
            "c": raw_samples[i],
            "s": raw_samples[i+1],
            "r": raw_samples[i+2],
            "w": raw_samples[i+3]
        }
        samples.append(sample)

test = []
for sample in samples:
    test.append(helpers.priorCheck(sample))


#### P(c = true) ####
count = 0.0
for sample in raw_samples:
    if sample <= helpers.C_TRUE:
        count += 1

value = count/len(raw_samples)
print('P(c = true) = {0}'.format(value))


#### P(c = true | r = true) ####
value = 0.0
count = 0.0
count_total = 0.0
for i in range(0,len(raw_samples),2):
    c = raw_samples[i]
    r = raw_samples[i+1]

    if c <= helpers.C_TRUE:
        c = True
    else:
        c = False

    if r <= helpers.R_TRUE_C_TRUE and c == True:
        r = True
    elif r > helpers.R_TRUE_C_TRUE and c == True:
        r = False
    elif r <= helpers.R_TRUE_C_FALSE and c == False:
        r = True
    elif r > helpers.R_TRUE_C_FALSE and c == False:
        r = False

    if r == True:
        if c  == True:
            count += 1
        count_total += 1

value = count/count_total
print('P(c = true | r = true) = {0}'.format(value))


#### P(s = true | w = true) ####
# Same as prior
value = 0.0
count = 0.0
count_total = 0.0
for sample in test:
    if sample['w'] == True:
        if sample['s'] == True:
            count += 1
        count_total += 1

value = count/count_total
print('P(s = true | w = true) = {0}'.format(value))

#### P(s = true | c = true, w = true) ####
# same as prior
value = 0.0
count = 0.0
count_total = 0.0
for sample in test:
    if sample['c'] == True and sample['w'] == True:
        if sample['s'] == True:
            count += 1
        count_total += 1

value = count/count_total
print('P(s = true | c = true, w = true) = {0}'.format(value))
