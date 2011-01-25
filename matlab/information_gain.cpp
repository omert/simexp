#include <vector>
#include <math.h>
#include "mex.h"
#include "model.h"
#include "Mat.h"

using namespace std;

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
log2(double x)
{
    return log(x) / log(2.0);
}


void mexFunction(int nlhs, mxArray *plhs[], int nrhs, const mxArray*prhs[])
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
    

    Mat S(prhs[0]);    

    double *ix = mxGetPr(prhs[1]);
    double *ia = mxGetPr(prhs[2]);
    double *ib = mxGetPr(prhs[3]);
    double *n = mxGetPr(prhs[4]);

    mxArray* mxP = mxCreateDoubleMatrix((int)numObj, (int)numObj, mxREAL); 
    Mat P(mxP);


    for (size_t y = 0; y < numObj; ++y)
	for (size_t iComp = 0; iComp < numComps; ++iComp){
	    size_t x = (size_t)ix[iComp] - 1;
	    size_t a = (size_t)ia[iComp] - 1;
	    size_t b = (size_t)ib[iComp] - 1;
	    
	    P(x, y) += n[iComp] * log(prob(S, y, a, b));
	}
    for (size_t x = 0; x < numObj; ++x){
	for (size_t y = 0; y < numObj; ++y)
	    P(x, y) = exp(P(x, y));
	double sum = 0.0;
	for (size_t y = 0; y < numObj; ++y)
	    sum += P(x, y);
	for (size_t y = 0; y < numObj; ++y)
	    P(x, y) = P(x, y) / sum;
    }

    plhs[0] = mxCreateDoubleMatrix((int)1, (int)1, mxREAL); 
    double& igain = *mxGetPr(plhs[0]);
    for (size_t x = 0; x < numObj; ++x){
//	mexPrintf("%f\n", -log2(numObj) - log2(P(x, x)));
//	igain += log2(numObj) + log2(P(x, x));
	size_t position = 0;
	for (size_t y = 0; y < numObj; ++y)
	    if (P(x, y) >= P(x, x))
		++position;
	igain += position;
	
    }    
    igain = igain / numObj;


//    mexPrintf("%f\n", igain);

    mxDestroyArray(mxP);

	    
    return;
    
}


