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

double 
prob(size_t x, size_t a, size_t b, const Mat& S)
{
    double pa = fabs(1.0 + S(x, x) + S(b, b) - 2 * S(x, b)) + 1e-6;
    double pb = fabs(1.0 + S(x, x) + S(a, a) - 2 * S(x, a)) + 1e-6;
//    double pa = exp(S(x, a));
//    double pb = exp(S(x, b));
    return pa / (pa + pb);
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
	double p = prob(x, b, a, S);
	double q = 1 - p;
	p *= n[iComp];
	q *= n[iComp];
	dS(x, a) += p;
	dS(a, x) = dS(x, a);
	dS(x, b) -= q;
	dS(b, x) = dS(x, b);
    }

	    
    return;
    
}


