import pandas as pd

class TopicReport():
    
    def __init__(self, lda):
        self.lda = lda
        
    def report(self, topicno, words=True, formatted=True):
        
        data = dict()
        
        if words:
            topwords = self.top_words(topicno)
            data['words'] = " ".join(topwords)
        
        if formatted:
            txt = "==TOPIC NO %d==" % topicno
            if words:
                txt += "\n" + data['words']
                
            print(txt)
        else:
            return data
        
    def report_all(self, words=True, formatted=True):
        for topicno in range(self.lda.num_topics):
            self.report(topicno, words, formatted)
            if formatted:
                print()
        
    def top_words(self, topicno, n=20):
        data = [word for word, prob in self.lda.show_topic(topicno, topn=n)]
        return data
    
    def top_docs(self, topicn, docmat, names, n=10):
        '''
        Return the documents that are most representative of a topic in a provided matrix.
        
        '''
        probs = docmat[:, topicn]
        ind = [x.split('_', 1)[-1].replace('-', '.').replace('_', ' ') for x in names]
        top_probs = pd.Series(probs, index=ind).sort_values(ascending=False).head(n).index.tolist()
        return top_probs
    
    def general_words(self, n=40, formatted=True):
        ''' 
        Return words with the highest auto-weighted ETA prior. That is, 
        the words most likely to occur in any given bill, lacking any other 
        information.
        '''
        a = pd.Series(self.lda.eta).sort_values(ascending=False)[:n]
        data = [self.lda._dictionary[x] for x in a.index]
        if formatted:
            print(" ".join(data))
        else:
            return data