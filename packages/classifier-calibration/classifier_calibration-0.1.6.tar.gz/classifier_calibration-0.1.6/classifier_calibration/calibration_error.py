"""Main module."""

from classifier_calibration.utils import bin_probabilities
    
    

def classwise_ece(pred_probs,labels,num_bins=20,return_weights=False):
    """ Calculate the classwise expected calibration error of a set of probabilistic predictions (which aims to penalise distance between predicted probabilities and true probabilities)

    Parameters
    ----------
    pred_probs : ndarray
        Array-like object of shape (num_samples, num_classes) where ij position is predicted probability of data point i belonging to class j.
        
    labels : ndarray
        This 1-D array of length num_samples contains the true label for each data point in the sample.
        
    num_bins : int
        Number of bins the interval [0,1] is divided into. (Default value = 20)

    return_weights : Bool, optional
        If True, returns a dictionary containing, for each class, the weights of each bin (proportion of data points whose predicted probability lies within the bin's limits).
        (Default value = False)

    Returns
    -------
    loss : float
        Value of the classwise expected calibration error. This is an element of [0,1]. 

    """
    if type(num_bins)!=int or num_bins<=0:
        print('num_bins must be a positive integer!')
        return

    num_samples, num_classes = pred_probs.shape

    # For each class, group predicted probabilities into corresponding bins
    binned_probability_dict = bin_probabilities(pred_probs=pred_probs,labels=labels,num_bins=num_bins,num_classes=num_classes,num_samples=num_samples)
    
    #calculate loss and record distribution of bin weights 
    loss = 0
    weights_dict = {}
    for i in range(num_classes):
        weight_list = []
        for key in binned_probability_dict[i].keys():
            num_trials = len(binned_probability_dict[i][key]['probs'])
            if num_trials>0:
                expected_num_occurrences = sum(binned_probability_dict[i][key]['probs'])
                actual_num_occurrences = binned_probability_dict[i][key]['num_occurrences']
                expected_occurence_rate = expected_num_occurrences/num_trials
                actual_occurence_rate = actual_num_occurrences/num_trials
                deviation = abs(expected_occurence_rate - actual_occurence_rate)
                weight = num_trials/num_samples
                weight_list.append(weight) # this will be used to check distribution of predictions - i.e. how many samples in each bin
                weighted_deviation = weight*deviation
                loss += weighted_deviation
            else:
                weight_list.append(0)
        weights_dict[i] = weight_list
    loss /= num_classes
    
    
    if return_weights == True:
        return loss, weights_dict
    else:
       return loss