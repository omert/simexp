#include <vector>
#include <math.h>
#include "mex.h"

void mexFunction(int nlhs, mxArray *plhs[], int nrhs, const mxArray*prhs[]);

class Mat{
public:
    Mat(const mxArray* m) 
	: _m(mxGetPr(m)), _numRows(mxGetM(m)) {}
    double& operator()(size_t i, size_t j){
	return _m[i + j * _numRows];
    }
    const double& operator()(size_t i, size_t j) const{
	return _m[i + j * _numRows];
    }
private:
    double*   _m;
    size_t    _numRows;
};


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
    

    plhs[0] = mxCreateDoubleMatrix((int)numObj, (int)numObj, mxREAL); 

    Mat S(prhs[0]);    
    Mat dS(plhs[0]);
    double *ix = mxGetPr(prhs[1]);
    double *ia = mxGetPr(prhs[2]);
    double *ib = mxGetPr(prhs[3]);
    double *n = mxGetPr(prhs[4]);


    for (size_t iComp = 0; iComp < numComps; ++iComp){
        size_t x = (size_t)ix[iComp] - 1;
        size_t a = (size_t)ia[iComp] - 1;
        size_t b = (size_t)ib[iComp] - 1;
	double da = 1.0 + S(x, x) - 2 * S(x, b) + S(b, b);
	double dab = 
	    1.0 + S(x, x) - 2 * S(x, a) + S(a, a)
	    + 1.0 + S(x, x) - 2 * S(x, b) + S(b, b);
	double dlogda = -n[iComp] / da;
	double dlogdab = n[iComp] / dab;

	dS(x, a) -= - 2.0 * dlogdab;
	dS(x, b) -= - 2.0 * dlogda - 2.0 * dlogdab;
	dS(x, x) -= 1.0 * dlogda + 2.0 * dlogdab;
	dS(b, b) -= 1.0 * dlogda + 1.0 * dlogdab;
	dS(a, a) -= 1.0 * dlogdab;

	dS(a, x) = dS(x, a);
	dS(b, x) = dS(x, b);
    }

	    
    return;
    
}


