#include <iostream>
#include <vector>
#include <map>
#include <math.h>
#include "mex.h"
#include "model.h"
#include "Mat.h"

using namespace std;

double 
frand()
{
    return 1.0 * rand() / RAND_MAX;
}

void 
normalize(vector<double>& rP)
{
    double sum = 0.0;
    for (size_t i = 0; i < rP.size(); ++i)
	sum += rP[i];
    for (size_t i = 0; i < rP.size(); ++i)
	rP[i] = rP[i] / sum;
}

double
entropy(const vector<double>& p)
{
    double ent = 0.0;
    for (size_t i = 0; i < p.size(); ++i)
	if (p[i] > 0.0)
	    ent -= p[i] * log(p[i]);
    return ent;
}

double 
prob(const Mat& S, const size_t x, const size_t a, const size_t b)
{
#ifdef EXP_INNER_PRODUCT
    return 1.0 / (1.0 + exp(S(x, b) - S(x, a)));
#endif
#ifdef EXP_DIST
    return 1.0 / (1.0 + exp(-S(b, b) + 2 * S(x, b) - 2 * S(x, a) + S(a, a)));
#endif
#ifdef REL_DIST
    double pa = fabs(1.0 + S(x, x) + S(b, b) - 2 * S(x, b));
    double pb = fabs(1.0 + S(x, x) + S(a, a) - 2 * S(x, a));
    return pa / (pa + pb);
#endif
 
}


double
expectedEntropy(const Mat& S, const Mat& P, const size_t numObj,
		 const size_t x, const size_t a, const size_t b)
{
    vector<double> p0(numObj);
    for (size_t i = 0; i < numObj; ++i)
	p0[i] = P(x, i);
    
    vector<double> pa = p0;
    vector<double> pb = p0;

    
    double p = 0.0;
    for (size_t y = 0; y < numObj; ++y){
	double pab = prob(S, y, a, b);
	pa[y] *= pab;
	pb[y] *= (1 - pab);
	p += pab * p0[y];
    }
    normalize(pa);
    normalize(pb);

    return p * entropy(pa) + (1 - p) * entropy(pb);
}

template<class M, class V>
void
getFirstNValues(const M& C, V& r, size_t N)
{
    for (typename M::const_iterator it = C.begin(); it != C.end(); ++it){
	if (r.size() >= N)
	    break;
	r.push_back(it->second);
    }
}

typedef pair<size_t, size_t> Trip;
typedef vector<Trip> Triplets;
void
produce_triplets(const Mat& S, const Mat& P, const size_t numObj, size_t x, 
		 Triplets& rTrips, size_t numTrips)
{
    multimap<double, Trip> entropyToTriplet;
    for (size_t i = 0; i < 1000; ++i){
	size_t a = 0;
	size_t b = 0;
	while (a == b || x == a || x == b){
	    a = rand() % numObj;
	    b = rand() % numObj;
	}
	double ent = expectedEntropy(S, P, numObj, x, a, b);
	if (entropyToTriplet.size() < numTrips ||
	    ent < entropyToTriplet.rbegin()->first)
	{
	    entropyToTriplet.insert(make_pair(ent, make_pair(a, b)));
	}
    }
    getFirstNValues(entropyToTriplet, rTrips, numTrips);
}

void mexFunction(int nlhs, mxArray *plhs[], int nrhs, const mxArray* prhs[])
{ 
    /* Check for proper number of arguments */
    
    if (nrhs != 6) 
        mexErrMsgTxt("Six inputs required: S, IX, IA, IB, N, num_per_obj"); 
    else if (nlhs > 1)
        mexErrMsgTxt("Too many output arguments."); 
    

    size_t numObj = mxGetM(prhs[0]);
    if (mxGetN(prhs[0]) != numObj)
        mexErrMsgTxt("First argument must be square matrix."); 
    size_t numComps = mxGetM(prhs[1]);
    if (mxGetM(prhs[2]) != numComps || 
	mxGetM(prhs[3]) != numComps || 
	mxGetM(prhs[4]) != numComps)
    {
        mexErrMsgTxt("Input sizes don't match. "
		     "Arguments 2, 3, 4 and 5 must be of the same length"); 
    }
    


    
    Mat S(prhs[0]);    
    Mat numPerObjectMat(prhs[5]);    
    size_t numPerObj = (size_t)numPerObjectMat(0, 0);


    plhs[0] = mxCreateDoubleMatrix((int)numObj * numPerObj, (int)3, mxREAL); 
    Mat T(plhs[0]);

    mxArray* plhs1[1];

    mexCallMATLAB(1, plhs1, 5, const_cast<mxArray**>(prhs), 
		  "confusion_matrix");
    Mat P(plhs1[0]);
    for (size_t x = 0; x < numObj; ++x){
	P(x, x) = 0.0;
	double sum = 0.0;
	for (size_t y = 0; y < numObj; ++y)
	    sum += P(x, y);
	for (size_t y = 0; y < numObj; ++y)
	    P(x, y) = P(x, y) / sum;
    }

    
    for (size_t x = 0; x < numObj; ++x){
	Triplets trips;
	produce_triplets(S, P, numObj, x, trips, numPerObj);
	if (trips.size() < numPerObj)
	    mexPrintf("Warning: have only %d trips for %d\n", trips.size(), x);
	for (size_t i = 0; i < trips.size(); ++i){
	    size_t a = trips[i].first;
	    size_t b = trips[i].second;
	    mexPrintf("%d ~ %d / %d: p = %f,  P(x, a) = %f, P(x, b) = %f\n",
		      x, a, b, prob(S, x, a, b), P(x, a), P(x, b));
	    T(numPerObj * x + i, 0) = x;
	    T(numPerObj * x + i, 1) = a;
	    T(numPerObj * x + i, 2) = b;
	}
    }
    for (size_t x = 0; x < numObj * numPerObj; ++x){
	T(x, 0) += 1;
	T(x, 1) += 1;
	T(x, 2) += 1;
    }	


    mxDestroyArray(plhs1[0]);
	    
    return;
    
}


