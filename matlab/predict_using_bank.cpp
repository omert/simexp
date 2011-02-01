#include "assert.h"
#include <iostream>
#include <vector>
#include <map>
#include <set>
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

class Distribution : vector<double>{
public:
    Distribution(size_t n) : vector<double>(n) {}
    Distribution() {}

    const double& operator() (const size_t i) const { return (*this)[i]; }
    double& operator() (const size_t i) { return (*this)[i]; }
    
    void resize(size_t n) { vector<double>::resize(n); }
    
    size_t size() const { return vector<double>::size(); }
    void makeUniform(){
	for (size_t i = 0; i < this->size(); ++i)
	    (*this)[i] = 1.0 / this->size();
	    
    }
    void makeUniform(size_t n){
	resize(n);
	for (size_t i = 0; i < this->size(); ++i)
	    (*this)[i] = 1.0 / this->size();
	    
    }
    void normalize(){
	double sum = 0.0;
	for (size_t i = 0; i < this->size(); ++i)
	    sum += (*this)[i];
	if (sum > 0.0)
	    for (size_t i = 0; i < this->size(); ++i)
		(*this)[i] = (*this)[i] / sum;
    }
    
    double entropy() const{
	double ent = 0.0;
	for (size_t i = 0; i < this->size(); ++i)
	    if ((*this)[i] > 0.0)
		ent -= (*this)[i] * log((*this)[i]);
	return ent;
    }
};

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

    double p = pa / (pa + pb);
    double llh = atanh(2 * p - 1) * 0.7;
    return 0.5 + 0.5 * tanh(llh);
#endif
 
}


double
expectedEntropy(const Mat& S, const Distribution& p0, 
		const size_t a, const size_t b)
{
    size_t numObj = p0.size();
    
    Distribution pa = p0;
    Distribution pb = p0;
    
    double p = 0.0;
    for (size_t y = 0; y < numObj; ++y){
	double pab = prob(S, y, a, b);
	pa(y) *= pab;
	pb(y) *= 1 - pab;
	p += pab * p0(y);
    }
    pa.normalize();
    pb.normalize();

    return p * pa.entropy() + (1 - p) * pb.entropy();
}

typedef pair<size_t, size_t> Triplet;
typedef multiset<Triplet> Triplets;
typedef map<size_t, Triplets> Bank;


Triplets::iterator
mostInformativeQuery(const Mat& S, const Distribution& prior,
		     Triplets& triplets)
{
//    return *triplets.begin();
    assert(triplets.size() > 0);
    Triplets::iterator res = triplets.begin();

    double bestEntropy = 1e100;
    for (Triplets::const_iterator it = triplets.begin(); 
	 it != triplets.end(); ++it)
    {
	size_t a = it->first;
	size_t b = it->second;
	double ent = expectedEntropy(S, prior, a, b);
	if (ent < bestEntropy){
	    bestEntropy = ent;
	    res = it;
	}
	
    }
    return res;
}

void
guessObject(const Mat& S, const size_t numObj, 
	    const Triplets& triplets, const size_t maxQueries,
	    vector<Distribution>& p)
{
    mexPrintf("   questions:");
    p.resize(maxQueries);
    p[0].makeUniform(numObj);
    Triplets tripsLeft = triplets;
    for (size_t queries = 0; queries < maxQueries && tripsLeft.size() > 0; 
	 ++queries)
    {
	if (queries > 0)
	    p[queries] = p[queries - 1];

	Triplets::iterator t = mostInformativeQuery(S, p[queries], tripsLeft);
	size_t a = t->first;
	size_t b = t->second;
	tripsLeft.erase(t);
	
	for (size_t y = 0; y < numObj; ++y){
	    double pab = prob(S, y, a, b);
	    p[queries](y) *= pab;
	}
//	mexPrintf("_%d_%d", a, b);
	p[queries].normalize();
    }
    mexPrintf(" \n");

}



void
buildBank(const double* ix, const double* ia, 
	  const double* ib, const double* in, 
	  const size_t numComps, Bank& rBank)
{
    for (size_t iComp = 0; iComp < numComps; ++iComp){
	size_t x = (size_t)ix[iComp] - 1;
	size_t a = (size_t)ia[iComp] - 1;
	size_t b = (size_t)ib[iComp] - 1;
	size_t n = (size_t)in[iComp];

	for (size_t i = 0; i < n; ++i)
	    rBank[x].insert(make_pair(a, b));
    }
}

void mexFunction(int nlhs, mxArray *plhs[], int nrhs, const mxArray* prhs[])
{ 
    /* Check for proper number of arguments */
    
    if (nrhs != 6) 
        mexErrMsgTxt("Six inputs required: S, IX, IA, IB, N, num_queries"); 
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
    const double *ix = mxGetPr(prhs[1]);
    const double *ia = mxGetPr(prhs[2]);
    const double *ib = mxGetPr(prhs[3]);
    const double *n = mxGetPr(prhs[4]);
    Mat numQueriesMat(prhs[5]);    
    size_t numQueries = (size_t)numQueriesMat(0, 0);

    Bank bank;
    buildBank(ix, ia, ib, n, numComps, bank);
    mexPrintf("have bank for %d objects with %d trips\n", 
	      bank.size(), numComps);

    size_t numGains = 3;
    plhs[0] = mxCreateDoubleMatrix((int)numGains, (int)numQueries, mxREAL); 
    Mat igain(plhs[0]);
    for (Bank::const_iterator it = bank.begin(); it != bank.end(); ++it){
	size_t x = it->first;
	mexPrintf("trying to guess object %d from %d trips ", x, 
		  it->second.size());

	if (it->second.size() < numQueries){
	    mexPrintf("ERROR: not enough trips (%d) to make %d queries.\n",
		      it->second.size(), numQueries);
	    continue;
	}

	vector<Distribution> p;
	mexPrintf("Learning %d\n", x);
	guessObject(S, numObj, it->second, numQueries, p);

	for (size_t i = 0; i < numQueries; ++i){
	    igain(0, i) += log2(1.0 * numObj) + log2(p[i](x));
	    
	    size_t position = 0;
	    for (size_t y = 0; y < numObj; ++y)
		if (p[i](y) >= p[i](x))
		    ++position;

	    if (i == numQueries - 1)
		mexPrintf("    %d queries: position %d\n", i, position);
	    igain(1, i) += position;
	    igain(2, i) += log2(1.0 * position);
	}

    }
    for (size_t i = 0; i < numGains; ++i)
	for (size_t j = 0; j < numQueries; ++j)
	    igain(i, j) = igain(i, j) / bank.size();
    
    
	    
    return;
    
}


