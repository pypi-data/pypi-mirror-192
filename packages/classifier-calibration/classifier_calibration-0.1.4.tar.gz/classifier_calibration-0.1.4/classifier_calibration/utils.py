import math
import pandas as pd


def bin_probabilities(pred_probs,labels,num_bins,num_classes,num_samples):
    """Group predictions into bins according to the interval the associated probability falls into.
    
    Divide [0,1] into num_bins intervals of equal length such that the m_th interval is given by [(m-1)/num_bins, m/num_bins)
    Given a set of predicted probabilities, group the predictions into bins according to the interval the predicted probability lies within.
    Keep track of true labels associated with predicitons in each bin.

    Parameters
    ----------
    pred_probs : ndarray
        Array-like object of shape (num_samples, num_classes) where ij position is predicted probability of data point i belonging to class j.

    labels : ndarray
        This 1-D array of length num_samples contains the true label for each data point in the sample.

    num_bins : int
        Number of bins (of equal length) the interval [0,1] is divided into.
        
    num_classes : int
        Number of classes in the problem.
        
    num_samples : int
        Number of data points in the sample.
        

    Returns
    -------
    binned_probability_dict: dict
        Nested dictionary to keep track of, for each class, the predicted probabilities grouped into each bin as well as the number of actual occurences 
        of the given class in each bin. 
        
        Primary keys are each of the classes in the problem, value of each of these keys is another nested dictionary. 
        Secondary keys are each of the bins the interval [0,1] is divided into, value of each of these keys is another nested dictionary. 
        Each of these final dictionaries contains two keys, 'probs' whose value is a list of all predicted probabilities grouped within the bin, 
        and 'num_occurences' whose value is the number of actual occurences of the given class in the data points associated with the bin.
    

    """
    pred_probs_df = pd.DataFrame(data=pred_probs,columns=[i for i in range(pred_probs.shape[1])]) # turn array into dataframe so each column is predicted probabilities of given class
    binned_probability_dict = {i:{j:{'probs':[],'num_occurrences':0} for j in range(num_bins)} for i in range(num_classes)} 

    for i in range(num_classes):
        class_i_predicted_probabilities = list(pred_probs_df[i]) # prob of each sample belonging to class i
        is_class_i = list(labels==i)
        for j in range(num_samples): 
            if class_i_predicted_probabilities[j] == 1:
                binned_probability_dict[i][num_bins-1]['probs'].append(class_i_predicted_probabilities[j])
                binned_probability_dict[i][num_bins-1]['num_occurrences'] += is_class_i[j] 
            else:
                bin_index = math.floor((100*class_i_predicted_probabilities[j])/(100/num_bins)) # identifies which bin the predicted probability lies within and returns its index
                binned_probability_dict[i][bin_index]['probs'].append(class_i_predicted_probabilities[j]) 
                binned_probability_dict[i][bin_index]['num_occurrences'] += is_class_i[j]
    
    return binned_probability_dict
