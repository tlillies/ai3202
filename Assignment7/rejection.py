import helpers

print("Rejection Sampling\n")

raw_samples = helpers.getSamples()
samples = []

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
    test.append(helpers.check(sample))


#### P(c = true) ####
count = 0.0
for sample in raw_samples:
    if sample  =< C_TRUE:
        count += 1

value = count/len(test)
print('P(c = true) = {0}'.format(value))


#### P(c = true | r = true) ####
value = 0.0
count = 0.0
count_total = 0.0
for sample in test:
    if sample['r'] == True:
        if sample['c'] == True:
            count += 1
        count_total += 1

value = count/count_total
print('P(c = true | r = true) = {0}'.format(value))


#### P(s = true | w = true) ####
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
