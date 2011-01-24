#include <iostream>
#include <vector>
#include <math.h>
#include "mex.h"
#include "model.h"
#include "Mat.h"

using namespace std;

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
 
}


double
informationGain(const Mat& S, const Mat& P, const size_t numObj,
		const size_t x, const size_t a, const size_t b)
{
    vector<double> p0(numObj);
    for (size_t i = 0; i < numObj; ++i)
	p0[i] = P(x, i);
    
    vector<double> pa = p0;
    vector<double> pb = p0;

    for (size_t y = 0; y < numObj; ++y){
	double pab = prob(S, y, a, b);
	pa[y] *= pab;
	pb[y] *= (1 - pab);
    }
    normalize(pa);
    normalize(pb);

    double p = prob(S, x, a, b);
    return p * entropy(pa) + (1 - p) * entropy(pb);
}

void
produce_triplet(const Mat& S, const Mat& P, const size_t numObj,
		size_t x, size_t& rA, size_t& rB)
{
    double bestInfoGain = 0.0;
    for (size_t a = 0; a < numObj; ++a){
	if (a == x)
	    continue;
	for (size_t b = a + 1; b < numObj; ++b){
	    if (b == x)
		continue;
	    double infoGain = informationGain(S, P, numObj, x, a, b);
	    if (infoGain > bestInfoGain){
		bestInfoGain = infoGain;
		rA = a;
		rB = b;
	    }
	}
    }
    
}

void mexFunction(int nlhs, mxArray *plhs[], int nrhs, const mxArray* prhs[])
{ 
    /* Check for proper number of arguments */
    
    if (nrhs != 5) { 
        mexErrMsgTxt("Five input arguments required."); 
    } else if (nlhs > 1) {
        mexErrMsgTxt("Too many output arguments."); 
    } 

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
    Mat T(plhs[0]);
    double *ix = mxGetPr(prhs[1]);
    double *ia = mxGetPr(prhs[2]);
    double *ib = mxGetPr(prhs[3]);
    double *n = mxGetPr(prhs[4]);

    mxArray* plhs1[1];

    mexCallMATLAB(1, plhs1, nrhs, const_cast<mxArray**>(prhs), 
		  "confusion_matrix");
    Mat P(plhs1[0]);
    
    for (size_t x = 0; x < 1; ++x){
	size_t a;
	size_t b;
	produce_triplet(S, P, numObj, x, a, b);
	T(x, 0) = x + 1;
	T(x, 1) = a + 1;
	T(x, 2) = b + 1;
    }
	


    mxDestroyArray(plhs[0]);
	    
    return;
    
}


