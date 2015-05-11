from scipy.stats import norm

def points(rmin, rmax, mean, sd):
   return [(x, norm(mean, sd).pdf(x)) for x in range(rmin, rmax)]
