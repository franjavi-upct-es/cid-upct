
from mrjob.job import MRJob

class MRWordFrequencyCount(MRJob) :

    def mapper(self, _, line):
        line = line.strip()
        for word in line.split():
            yield word, 1
    def reducer(self, key, values):
        yield key, sum(values)
        
if __name__ == '__main__':
    MRWordFrequencyCount.run()
