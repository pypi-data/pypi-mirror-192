from sklearn.metrics import roc_auc_score


class MAE():

    def __init__(self):
        self.name = 'roc_auc'
        self.input_type = 'float'
        self.output_type = None
        self.kwargs = None
        

    def parse_data(self, data):
        
        return data



    def compute(self, references, prediction_scores, average="macro", sample_weight=None,
                max_fpr=None, multi_class="raise", labels=None):
        score = roc_auc_score(y_true=references, y_pred=prediction_scores, average=average, sample_weight=sample_weight,
                               multi_class=multi_class, max_fpr=max_fpr, labels=labels)
        
        score = {
            self.name : float(score)
            }
 

        return score