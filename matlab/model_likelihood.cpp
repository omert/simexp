#include <vector>
#include <math.h>
#include "mex.h"

void mexFunction(int nlhs, mxArray *plhs[], int nrhs, const mxArray*prhs[] )
{ 
    
    /* Check for proper number of arguments */
    
    if (nrhs != 5) { 
        mexErrMsgTxt("Five input arguments required."); 
    } else if (nlhs > 2) {
        mexErrMsgTxt("Too many output arguments."); 
    } 

    size_t numObj = mxGetM(prhs[0]);
    size_t numDim = mxGetN(prhs[0]);
    size_t numComps = mxGetM(prhs[1]);
//   	mexPrintf("num_obj: %d, dim: %d, num_comps: %d\n", numObj, numDim, numComps);
    if (mxGetM(prhs[2]) != numComps || mxGetM(prhs[3]) != numComps || mxGetM(prhs[4]) != numComps)
        mexErrMsgTxt("Input sizes don't match"); 
    

    plhs[0] = mxCreateDoubleMatrix(1, 1, mxREAL); 
    double &f = *mxGetPr(plhs[0]);
    double *V = mxGetPr(prhs[0]);
    double *ix = mxGetPr(prhs[1]);
    double *ia = mxGetPr(prhs[2]);
    double *ib = mxGetPr(prhs[3]);
    double *n = mxGetPr(prhs[4]);

    double *g;
    if (nlhs > 1){
        plhs[1] = mxCreateDoubleMatrix((int)numObj, (int)numDim, mxREAL); 
        g = mxGetPr(plhs[1]);
    }

    f = 0.0;
    for (size_t iComp = 0; iComp < numComps; ++iComp){
        size_t x = (size_t)ix[iComp] - 1;
        size_t a = (size_t)ia[iComp] - 1;
        size_t b = (size_t)ib[iComp] - 1;
        double da = 0.0;
        double db = 0.0;
//        da = V[x] * V[x] + V[a] * V[a];
//        db = V[x] * V[x] + V[b] * V[b];
        for (size_t iDim = 0; iDim < numDim; ++iDim){
            double dai = V[x + numObj * iDim] - V[a + numObj * iDim];
            da += dai * dai;
            double dbi = V[x + numObj * iDim] - V[b + numObj * iDim];
            db += dbi * dbi;
        }
        double llhr = log(1 + da) - log(1 + db);
        double p = 1 / (1  + exp(llhr));
        f -= n[iComp] * log(p);
        if (nlhs > 1){
//            g[x] += 2 * n[iComp] * (1 - p) * V[x] / (1 + da);
//            g[x] -= 2 * n[iComp] * (1 - p) * V[x] / (1 + db);
//            g[a] += 2 * n[iComp] * (1 - p) * V[a] / (1 + da);
//            g[b] -= 2 * n[iComp] * (1 - p) * V[b] / (1 + db);
            for (size_t iDim = 0; iDim < numDim; ++iDim){
                double ga = 2 * n[iComp] * (1 - p) * (V[x + numObj * iDim] - V[a + numObj * iDim]) / (1 + da);
                double gb = 2 * n[iComp] * (1 - p) * (V[x + numObj * iDim] - V[b + numObj * iDim]) / (1 + db);
                g[x + numObj * iDim] += ga - gb;
                g[a + numObj * iDim] -= ga;
                g[b + numObj * iDim] += gb;
            }
        }
    }

    return;
    
}


