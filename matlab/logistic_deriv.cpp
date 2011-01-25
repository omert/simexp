#include <vector>
#include <math.h>
#include "mex.h"
#include "model.h"
#include "Mat.h"

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
	
#ifdef EXP_DIST
	double h = 1.0 / 
	    (1.0 + exp(-S(b, b) + 2 * S(x, b) - 2 * S(x, a) + S(a, a)));
	double dlogh = n[iComp] * (1.0 - h);
	dS(x, a) += 2 * dlogh;
	dS(x, b) -= 2 * dlogh;
	dS(b, b) += dlogh;
	dS(a, a) -= dlogh;
#endif	

#ifdef EXP_INNER_PRODUCT        
	double h = 1.0 / (1.0 + exp(S(x, b) - S(x, a)));
	double dlogh = n[iComp] * (1.0 - h);
	dS(x, a) += dlogh;
	dS(x, b) -= dlogh;
#endif
#ifdef REL_DIST
	double dxa = 1.0 + S(x, x) + S(a, a) - 2 * S(x, a);
	double dxb = 1.0 + S(x, x) + S(b, b) - 2 * S(x, b);
//	dS(x, a) += n[iComp] * S(x, x) * dxa * dxb / pow(dxa + dxb, 3.0);
//	dS(x, b) -= n[iComp] * S(x, x) * dxa * dxa / pow(dxa + dxb, 3.0);
	dS(x, a) += n[iComp] * 2.0 / (dxa + dxb);
	dS(x, b) += n[iComp] * (2.0 / (dxa + dxb) - 2.0 / dxb);
#endif
	dS(a, x) = dS(x, a);
	dS(b, x) = dS(x, b);

    }

	    
    return;
    
}
