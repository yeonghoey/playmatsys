from scipy.stats import norm

def build_points(mean, stddev):
    rmin = int(mean-(3*stddev))
    rmax = int(mean+(3*stddev))
    return [(x, norm(mean, stddev).pdf(x)) for x in xrange(rmin, rmax)]
