import hashtable
import math

HASH_CELLS = 57
TOO_FULL = 0.5
GROWTH_RATIO = 2

class Markov:
    def __init__(self, k, text, use_hashtable=True):
        """
        Markov Model Class creates markov model using either a 
        hashtable with separate chaining using linked lists or dictionary

        Attributes:
            k (int): order of markov model- generate strings of k/k+1 length for
            each char in text to build markov model
            text (str): input text to model with Markov Model
            use_hashtable (bool): True if using hashtable, False if using dictionary
            model- markov model itself created by markov_builder
        
        Methods:
            markov_builder- args: k, text, use_hashtable- returns markov 
            model as hashtable or dictionary
            log_probability- args: s- returns log probability of string s 
            given markov model- used to identify speaker of text
        """
        self.k = k
        self.text = text
        self.S = len(set([char for char in text]))
        self.model = self.markov_builder(k, self.text, use_hashtable)


    def markov_builder(self, k, text, use_hashtable):
        """Creates markov model using either a hashtable with separate chaining 
        using linked lists or dictionary
        
        Args:
            k (int): order of markov model- generate strings of k/k+1 
            length for each char in text to build markov model
            text (str): input text to model with Markov Model
            use_hashtable (bool): True if using hashtable, False if dict
        """
        model = {}
        
        for i in range(len(text)):
            for j in range(k, k + 2):
                #No Wrap
                if i+j <= len(text):
                    key = text[i:i+j] 
                #Wrap
                else:
                    key = text[i:] + text[:i+j - len(text)]
            
                #Add 1 to val if key already in model, else add key to model
                model[key] = model.get(key, 0) + 1

        #Convert to hashtable if use_hashtable is True
        if use_hashtable:
            hashtable_model = hashtable.Hashtable(HASH_CELLS, 
                                                    0, 
                                                    TOO_FULL, 
                                                    GROWTH_RATIO)
            for key, value in model.items():
                hashtable_model[key] = value
            return hashtable_model
        return model
    
    
    def log_probability(self, s):
        """
        Get the log probability of string "s", given the statistics of
        character sequences modeled by this particular Markov model
        This probability is *not* normalized by the length of the string.
        """
        total_prob = 0

        for i in range(len(s)):
            #Wrap Around K
            if i + self.k > len(s):
                k_str = s[i:] + s[:i+self.k-len(s)]
            #No Wrap K
            else: 
                k_str = s[i:i+self.k]

            #Wrap Around K+1
            if i+self.k + 1 > len(s):
                k_plus1 = s[i:] + s[:i+self.k+1-len(s)]  
            #No Wrap K+1
            else:
                k_plus1 = s[i:i+self.k+1]
            
            #Calculate log prob then add to total log prob
            N = self.model.get(k_str,0)
            M = self.model.get(k_plus1,0)
            log_prob = math.log((M+1)/(N+self.S))
            total_prob += log_prob    
        return total_prob
           

def identify_speaker(speech1, speech2, speech3, k, use_hashtable):
    """
    Given sample text from two speakers (1 and 2), and text from an
    unidentified speaker (3), return a tuple with the *normalized* log probabilities
    of each of the speakers uttering that text under a "order" order
    character-based Markov model, and a conclusion of which speaker
    uttered the unidentified text based on the two probabilities.
    """
    #Speaker Markov Models
    speaker1 = Markov(k, speech1, use_hashtable)
    speaker2 = Markov(k, speech2, use_hashtable)

    #Log Probabilities
    speaker1_prob = speaker1.log_probability(speech3)
    speaker2_prob = speaker2.log_probability(speech3)

    #Normalize probabilities
    speaker1_prob = speaker1_prob / len(speech3)
    speaker2_prob = speaker2_prob / len(speech3)

    #Conclusion
    if speaker1_prob > speaker2_prob:
        return (speaker1_prob, speaker2_prob, 'A')
    else:
        return (speaker1_prob, speaker2_prob, 'B')