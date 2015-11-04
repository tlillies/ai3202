C_TRUE = 0.5

S_TRUE_C_TRUE = .1
S_TRUE_C_FALSE = .5

R_TRUE_C_TRUE = .8
R_TRUE_C_FALSE = .2

W_TRUE_S_TRUE_R_TRUE = 0.99
W_TRUE_S_TRUE_R_FALSE = 0.90
W_TRUE_S_FALSE_R_TRUE = 0.90
W_TRUE_S_FALSE_R_FALSE = 0.00

def priorCheck(sample):
    ret =  {}
    if sample['c'] <= C_TRUE:
        ret['c'] = True
        s_test = S_TRUE_C_TRUE
        r_test = R_TRUE_C_TRUE
    else:
        ret['c'] = False
        s_test = S_TRUE_C_FALSE
        r_test = R_TRUE_C_FALSE


    if sample['s'] <= s_test:
        ret['s'] = True
    else:
        ret['s'] = False

    if sample['r'] <= r_test:
        ret['r'] = True
    else:
        ret['r'] = False

    if ret['r'] == True and ret['s'] == True:
        w_test = W_TRUE_S_TRUE_R_TRUE
    if ret['r'] == True and ret['s'] == False:
        w_test = W_TRUE_S_TRUE_R_FALSE
    if ret['r'] == False and ret['s'] == True:
        w_test = W_TRUE_S_FALSE_R_TRUE
    if ret['r'] == False and ret['s'] == False:
        w_test = W_TRUE_S_FALSE_R_FALSE

    if sample['w'] <= w_test:
        ret['w'] = True
    else:
        ret['w'] = False

    return ret

def getSamples():
    samples_file = open('random_samples')
    samples_strings = samples_file.read().split(',')
    samples = []

    for i in range(len(samples_strings)):
        samples.append(float(samples_strings[i]))

    print "SAMPLES: \n"
    print samples
    print ""
    return samples



