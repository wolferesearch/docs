import pandas as pd
import json
import pandas as pd
import json


TEST_DATA_SET = {"SAMPLE1": ['Investors thought Wendy’s 15.5% 2022 restaurant-margin target was somewhat conservative.',
               'We expect solid results from DASH. Nice beat/strong guide should be rewarded but upside is likely to balanced given high expectations.',
               'Technicals and incremental news flow will likely continue to drive trading through year end. We wouldn’t be surprised to see some more near-term upside, including the SPX trading into the 4050-4100 range.',
               'While the moves across markets were epic, we believe that our intermediate-term bearish base case remains intact. This includes core inflation remaining very persistent, the Fed hiking to 5-6%, and a recession hitting in 2023.',
               'We believe that earnings and guidance are likely to begin to come under pressure in the coming quarters. Our sense is that companies beating on the top- and bottom-lines and providing constructive outlooks should have an increased chance of outperforming their peers in the months ahead.',
               'Our business in global market will likely to benefit with the China opening and economy recovery scenario.',
               'To better meet the business development requirement, we have accelerated the application of our Fintech. As we have already introduced like AI and blockchain and all the other advanced technology, we have made a lot of explorations and applications in AI and achieved a lot of outcome in empowering our business.'
            ]}

class NLPApi:
    """
        QES Financial Natural Language Processing - API provides a suite of NLP toolkits with state-of-the-art deep learning pretrained language models (PLMs) designed for applications in finance and investment domain.

        The QesNLP API service consists of the following three functionality modules.
        - Preprocessing Module - preprocess the raw text input into parsed machine-readable NLP data structure, including tokenization, summarization, entity recognition, and keyphrases identification.
        - Embedding Module - embed the input text document/sentence into contextual vectors based on the NLP pre-trained language models. The contextualized vectors fit in with the standard machine learning algorithms and could empower the downstream NLP tasks.
        - Exposure Module - This module renders the thematic distance between text document to well-defined theme by leveraging the contextual embeddings of both text documents and theme clusters. 
        - Sentiment Classification Module - This module supports downstream NLP classification tasks, such as sentiment analysis.
    """
    
    def __init__(self, connection):
        self.connection = connection

    def _check_error_(self, response):
        if response.status_code != 200:
            raise Exception("Service request failed due to {}",str(response.text))
        return response
    
    def _payload_(self, texts: list):
        return {
            "texts": texts
        }
    
    def _post_(self,svc, texts: list):
        #print(svc)
        response = self.connection._post_(svc = svc, body = self._payload_(texts))
        self._check_error_(response)
        return response
    
    def _to_text(self,response):
        return response.content.decode("utf-8")
    
    def _to_json(self,response):
        return json.loads(self._to_text(response))
        
    def compute_sentiment(self, list_of_texts: list, model='analyst-tone'):
        """Computes Sentiment of the inputted Text.

        Parameters
        ----------
        list_of_texts: list
            List of Text that needs to be analyzed. 
        model: str
            One of the following options
            - analyst-tone: FinBERT-analyst-tone model is fine-tuned on 10,000 manually annotated (positive, negative, neutral) sentences from analylst reports. This model achieves superior performance on financial tone anlaysis task. 
            - news_sentiment: nBERT-news-sentiment model is fine-tuned on 10,000 manually annotated (positive, negative, neutral) sentences from financial news. This model achieves superior performance on financial sentiment anlaysis task.
            - twitter-sentiment:The BERT-twitter model is fine-tuned on trained on ~58M English tweets and fine-tuned for sentiment analysis with the TweetEval benchmark, a unified benchmark for tweet classification consisting of seven heterogeneous tasks that are core to social media NLP research such as Sentiment Analysis and Emotion Recognition.

        Returns: pandas.DataFrame
        -------
        Returns a data frame containting score for sentiment. 
        """

        response = self._post_(svc = 'sentiment/{}'.format(model), texts = list_of_texts)
        return pd.DataFrame(self._to_json(response)['metrics'])
    
    def compute_social_emotion(self, list_of_texts: list):
        """Computes Forward-looking statements (FLS) inform investors of managers’ beliefs and opinions about firm's future events or results.
        
        Parameters
        ----------
        list_of_texts: list
            List of Text that needs to be analyzed. 

        Returns: pandas.DataFrame
        -------
        Returns a data frame containting score for different social emotions.
            - joy
            - anger
            - sadness
            - optimism
        """
        return self.compute_sentiment(list_of_texts, model = 'twitter-emotion')
     
    def compute_forward_looking_tone(self, list_of_texts: list):
        """Computes if a given text document statement is forward-looking or not. 
        Forward-Looking Statements (FLS) are typically declarations made by company management that convey their beliefs, expectations, or predictions about the company's future events or results.
        
        Parameters
        ----------
        list_of_texts: list
            List of Text that needs to be analyzed. 
        Returns: pandas.DataFrame
        -------
        Returns a data frame containting score for different forward looking metrics.
            - not forward looking
            - non-specific forward-looking
            - specific forward-looking 
        """
        return self.compute_sentiment(list_of_texts, model = 'forward-looking')
        
    
    def get_key_entity(self, list_of_texts: list):
        """Extracts Key Entities from inputted list of Texts.

        Parameters
        ----------
        list_of_texts: list
            List of Text that needs to be analyzed. 
        Returns: list
        -------
        Returns the list of key entities. For each element in the input text, a correponding list of tuples is returned.
        """
        response = self._post_(svc = 'preprocess/keyentity', texts = list_of_texts)
        return self._to_json(response)['keyphrases']

    def get_key_phrases(self, list_of_texts: list):
        """Extracts Key Phrases from inputted list of Texts

        Parameters
        ----------
        list_of_texts: list
            List of Text that needs to be analyzed. 
        Returns: list
        -------
        Returns the list of key phrases (n-grams). For each element in the input text, a correponding list of tuples is returned.
        """
        response = self._post_(svc = 'preprocess/keyphrase', texts = list_of_texts)
        return self._to_json(response)['keyphrases']
    
    def summarize(self, list_of_texts: list):
        """Summarize the Text

        Parameters
        ----------
        list_of_texts: list
            List of Text that needs to be analyzed. 
        Returns: list
        -------
        Returns summarized form of the inputted text. 
        """
        response = self._post_(svc = '/preprocess/summarize', texts = list_of_texts)
        return self._to_json(response)['summary']['summary_text']    
    
    def get_embedding(self, list_of_texts: list):
        """Gets Numerical embedding of the text. Embeddings are commonly used for:

        - Search (where results are ranked by relevance to a query string)
        - Clustering (where text strings are grouped by similarity)
        - Recommendations (where items with related text strings are recommended)
        - Anomaly detection (where outliers with little relatedness are identified)
        - Diversity measurement (where similarity distributions are analyzed)
        - Classification (where text strings are classified by their most similar label)

        An embedding is a vector (list) of floating point numbers. The distance between two vectors measures their relatedness. Small distances suggest high relatedness and large distances suggest low relatedness.

        Parameters
        ----------
        list_of_texts: list
            List of Text that needs to be analyzed. 
        Returns: list
        -------
        Generates embedding for the text. Returns list of double vector. Is useful for comparing two texts using L2 distance
        """        
        response = self._post_(svc = '/embed', texts = list_of_texts)
        return self._to_json(response)['embedding']
           
    def get_general_theme_exposure(self, list_of_texts: list):
        """Gets exposure to pre-defined general themes. 

        Parameters
        ----------
        list_of_texts: list
            List of Text that needs to be analyzed. 
        Returns: pandas.DataFrame
        -------
        Exposure (0-1) of the the input text to each of the pre-defined themes. 
        """
        response = self._post_(svc = '/exposure/General', texts = list_of_texts)
        return pd.DataFrame(self._to_json(response)['exposures'])

    def get_china_theme_exposure(self, list_of_texts: list):
        """Gets exposure to pre-defined China A themes

        Parameters
        ----------
        list_of_texts: list
            List of Text that needs to be analyzed. 
        Returns: pandas.DataFrame
        -------
        Exposure(0-1) of the input text to each of the pre-defined China Reopen themes. 
        """
        response = self._post_(svc = '/exposure/China', texts = list_of_texts)
        return pd.DataFrame(self._to_json(response)['exposures'])