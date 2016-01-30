from path import Path

PROJECT_ROOT = Path(__file__).dirname()

ELASTIC_INDEX_NAME = 'mir'

CACHE_DIR = PROJECT_ROOT / 'cache'
CRAWLER_INITIAL_URLS = [
    'https://www.researchgate.net/publication/278332447_MCMC_for_Variationally_Sparse_Gaussian_Processes',
    'https://www.researchgate.net/publication/285458515_A_General_Framework_for_Constrained_Bayesian_Optimization_using_Information-based_Search',
    'https://www.researchgate.net/publication/284579255_Parallel_Predictive_Entropy_Search_for_Batch_Global_Optimization_of_Expensive_Objective_Functions',
    'https://www.researchgate.net/publication/283658712_Sandwiching_the_marginal_likelihood_using_bidirectional_Monte_Carlo',
    'https://www.researchgate.net/publication/281895707_Dirichlet_Fragmentation_Processes',
    'https://www.researchgate.net/publication/273488773_Variational_Infinite_Hidden_Conditional_Random_Fields',
    'https://www.researchgate.net/publication/279633530_Subsampling-Based_Approximate_Monte_Carlo_for_Discrete_Distributions',
    'https://www.researchgate.net/publication/279309917_An_Empirical_Study_of_Stochastic_Variational_Algorithms_for_the_Beta_Bernoulli_Process',
    'https://www.researchgate.net/publication/278048012_Neural_Adaptive_Sequential_Monte_Carlo',
    'https://www.researchgate.net/publication/277959103_Dropout_as_a_Bayesian_Approximation_Appendix',
]

CRAWLER_IN_DEGREE = 10
CRAWLER_OUT_DEGREE = 10
