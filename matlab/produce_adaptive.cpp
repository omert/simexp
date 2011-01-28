#include <iostream>
#include <vector>
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

void
produce_triplet(const Mat& S, const Mat& P, const size_t numObj,
		size_t x, size_t& rA, size_t& rB, size_t coreSize)
{
    size_t maxObj = coreSize > 0 ? coreSize : numObj;
    double bestEntropy = numObj;
    for (size_t a = 0; a < maxObj; ++a){
	if (a == x)
	    continue;
	for (size_t b = a + 1; b < maxObj; ++b){
	    if (b == x)
		continue;
	    if (maxObj == numObj && frand() < 0.8)
		continue;
	    double ent = expectedEntropy(S, P, numObj, x, a, b);
	    if (ent < bestEntropy){
		bestEntropy = ent;
		rA = a;
		rB = b;
	    }
	}
    }
}

void mexFunction(int nlhs, mxArray *plhs[], int nrhs, const mxArray* prhs[])
{ 
    /* Check for proper number of arguments */
    
    if (nrhs != 6) 
        mexErrMsgTxt("Six inputs required: S, IX, IA, IB, N, core_size"); 
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
    

    plhs[0] = mxCreateDoubleMatrix((int)numObj, (int)3, mxREAL); 

    
    Mat S(prhs[0]);    
    Mat coreSizeMat(prhs[5]);    
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
	size_t a = 0;
	size_t b = 0;
	produce_triplet(S, P, numObj, x, a, b, (size_t)coreSizeMat(0, 0));
	mexPrintf("%d ~ %d / %d: p = %f,  P(x, a) = %f, P(x, b) = %f\n",
		  x, a, b, prob(S, x, a, b), P(x, a), P(x, b));
	T(x, 0) = x;
	T(x, 1) = a;
	T(x, 2) = b;
    }
    for (size_t x = 0; x < numObj; ++x){
	T(x, 0) += 1;
	T(x, 1) += 1;
	T(x, 2) += 1;
    }	


    mxDestroyArray(plhs1[0]);
	    
    return;
    
}


