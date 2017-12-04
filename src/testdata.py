import random
totalfl = open('/home/rik/Heena/news/news.dat','r')
trainfl = open('/home/rik/Heena/traindata.txt','w')
testfl = open('/home/rik/Heena/testdata.txt','w')
r = random.sample(range(1,92851),18000)
counter = 1
for line in totalfl:
    if counter in r:
        testfl.write(line)
    else:
        trainfl.write(line)
    counter += 1
print('done')