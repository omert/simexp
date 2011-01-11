#include <stdlib.h>
#include <iostream>
#include <fstream>
#include <sstream>
#include <vector>
#include <set>
#include <boost/filesystem.hpp>   
#include <boost/regex.hpp>   
#include <lapackpp.h>

using namespace std;
using namespace boost::filesystem;
using boost::regex;

typedef LaGenMatDouble Mat;
typedef LaVectorDouble Vec;

class Triplets{
public:
    vector<size_t> _x;
    vector<size_t> _a;
    vector<size_t> _b;
    set<size_t> _ids;

    size_t size() const { return _x.size(); }
    size_t maxId() const { 
	if (_ids.size() > 0)
	    return *_ids.rbegin();
	else
	    return 0;
    }
    void 
    addTriplet(size_t x, size_t a, size_t b){
	_x.push_back(x);
	_a.push_back(a);
	_b.push_back(b);
	_ids.insert(x);
	_ids.insert(a);
	_ids.insert(b);
    }
};

Mat
tpose(const Mat& M)
{
    Mat ret(M.cols(), M.rows());
    for (size_t i = 0; i < (size_t) ret.rows(); ++i)
	for (size_t j = 0; j < (size_t) ret.cols(); ++j)
	    ret(i, j) = M(j, i);
    return ret;
}

double 
prob(size_t x, size_t a, size_t b, const Mat& S)
{
    double pa = fabs(1.0 + S(x, x) + S(b, b) - 2 * S(x, b)) + 1e-6;
    double pb = fabs(1.0 + S(x, x) + S(a, a) - 2 * S(x, a)) + 1e-6;
//    double pb = S(x, b);
//    double pa = S(x, a);
    return pa / (pa + pb);
}

double
modelFit(const Triplets& trips, const Mat& S, double& rExpectedFit)
{
    double ret = 0.0;
    rExpectedFit = 0.0;
    size_t correctGuesses = 0;
    for (size_t i = 0; i < trips.size(); ++i){
	size_t x = trips._x[i];
	size_t a = trips._a[i];
	size_t b = trips._b[i];
	double p = prob(x, a, b, S);
	ret -= log(p);
	rExpectedFit -= p * log(p) + (1 - p) * log(1 - p);
	if (p > 0.5)
	    ++correctGuesses;
    }
    cout << 100.0 * correctGuesses / trips._x.size() << " correct guess percentage" << endl;
    rExpectedFit = rExpectedFit / log(2) / trips._x.size();
    ret = ret / log(2) / trips._x.size();
    return ret;
}


Mat
meanWithTransposed(const Mat& U, const Mat& V)
{
    size_t n = U.rows();
    Mat ret(n, n);
    for (size_t i = 0; i < n; ++i)
	for (size_t j = 0; j < n; ++j)
	    ret(i, j) = (U(i, j) + V(j, i)) / 2;
    return ret;
}

Mat
quickProjectPSDM(const Mat& S, double M)
{
    Mat ret = S;
    size_t n = S.rows();
    for (size_t i = 0; i < n; ++i){
	double rowMax = M;
	for (size_t j = 0; j < n; ++j)
	    if (rowMax < ret(i, j))
		rowMax = ret(i, j);
	rowMax = rowMax / M;
	
	for (size_t j = 0; j < n; ++j){
	    ret(i, j) = ret(i, j) / rowMax;
	    if (ret(i, j) < 1)
		ret(i, j) = 1;
	    
	    ret(j, i) = ret(i, j);
	}
	ret(i, i) = M;
    }
    return ret; 
}

Mat
projectPSDd(const Mat& S, size_t d)
{
    size_t n = S.rows();

    
    Mat SS = (d < n) ? projectPSDd(S, S.rows()) : S;
    
    Mat U(n, n);
    Mat V(n, n);
    Vec sigVec(n);
    cout << "calculating SVD...";
    fflush(0);
    LaSVD_IP(SS, sigVec, U, V);
    cout << " done." << endl;
    fflush(0);
    
    Mat sig = Mat::zeros(n, n);
    for (size_t i = 0; i < d; ++i)
	sig(i, i) = sigVec(i);
    for (size_t i = d; i < n; ++i)
	sig(i, i) = 0;
    
    U = meanWithTransposed(U, V);
    
    Mat temp(n, n);
    Blas_Mat_Mat_Mult(U, sig, temp, false);
    Mat ret(n, n);
    Blas_Mat_Mat_Mult(temp, U, ret, false, true);
    return ret;
}

bool
moreEqualThanOpposite(const Mat& r1, const Mat& r2)
{
    double sumP = 0.0;
    double sumN = 0.0;
    for (size_t i = 0; i < (size_t)r1.rows(); ++i){
	sumP += fabs(r1(i, 0) - r2(0, i));
	sumN += fabs(r1(i, 0) + r2(0, i));
    }
    return sumP < sumN;

}

double 
sum(const Vec& v)
{
    double ret = 0.0;
    for (size_t i = 0; i < (size_t) v.size(); ++i)
	ret += v(i);
    return ret;
}

double 
nonZeroMin(const Vec& v)
{
    double ret = 1e300;
    for (size_t i = 0; i < (size_t) v.size(); ++i)
	if (v(i) > 1e-10 && v(i) < ret)
	    ret = v(i);
    return ret;
}

size_t 
numNonZero(const Vec& v)
{
    size_t ret = 0;
    for (size_t i = 0; i < (size_t) v.size(); ++i)
	if (v(i) > 1e-10)
	    ++ret;
    return ret;
}

void
printPositive(const Vec& v)
{
    for (size_t i = 0; i < (size_t) v.size(); ++i)
	if (v(i) > 1e-10)
	    cout << v(i) << " ";
    cout << endl;
}

Mat
projectPSDtr(const Mat& S, double maxTr)
{
    size_t n = S.rows();

    
    Mat SS = S;
    
    Mat U(n, n);
    Mat V(n, n);
    Vec s(n);
    cout << "calculating SVD...";
    fflush(0);
    LaSVD_IP(SS, s, U, V);
    cout << " done." << endl;
    fflush(0);
    

    for (size_t i = 0; i < n; ++i)
	if (!moreEqualThanOpposite(U.col(i), V.row(i)))
	    s(i) = 0.0;
    while (true){
	double tr = sum(s);
	if (tr < maxTr * 1.01)
	    break;
	double dtr = tr - maxTr;
	double smin = nonZeroMin(s);
	size_t m  = numNonZero(s);
	if (smin * m < dtr)
	    for (size_t i = 0; i < n; ++i)
		s(i) = max(0.0, s(i) - smin);
	else
	    for (size_t i = 0; i < n; ++i)
		s(i) = max(0.0, s(i) - dtr / m);
    }
//    printPositive(s);
    Mat sig = Mat::zeros(n, n);
    for (size_t i = 0; i < n; ++i)
	sig(i, i) = s(i);
    

    Mat temp(n, n);
    Blas_Mat_Mat_Mult(U, sig, temp, false);
    Mat ret(n, n);
    Blas_Mat_Mat_Mult(temp, V, ret, false);
    cout << "matrix rank: " << numNonZero(s) << endl;
//    for (size_t i = 0; i < (size_t)ret.rows(); ++i)
//	cout << ret(i, i) << " ";
    return ret;
}

Mat
projectPSDM(const Mat& S, double M)
{
    Mat ret = S;

    size_t n = S.rows();
    Mat SS = S;
    for (size_t i = 0; i < n; ++i)
	SS(i, i) = M;
    
    double stepSize = 100.0;
    double lastDiagNorm = 1e100;
    for (size_t iter = 0; iter < 1000; ++iter){
	Mat sTemp = S;
	Mat U(n, n);
	Mat V(n, n);
	Vec sigVec(n);
	Mat SStemp = SS;
	LaSVD_IP(SStemp, sigVec, U, V);

	Mat sig = Mat::zeros(n, n);
	for (size_t i = 0; i < n; ++i)
	    sig(i, i) = sigVec(i);

	U = meanWithTransposed(U, V);
	
	Mat temp(n, n);
	Blas_Mat_Mat_Mult(U, sig, temp, false);
	Blas_Mat_Mat_Mult(temp, U, ret, false, true);
	
	double diagNorm = 0.0;
	for (size_t i = 0; i < n; ++i)
	    diagNorm += (ret(i, i) - M) * (ret(i, i) - M);
	if (diagNorm < 1e-5 * n * M)
	    break;
	if (diagNorm > lastDiagNorm)
	    stepSize /= 2.0;
	if (stepSize < 0.1)
	    break;
	lastDiagNorm = diagNorm;
//	cout << iter << " " << stepSize << " " << diagNorm << endl;
	for (size_t i = 0; i < n; ++i)
	    SS(i, i) -= stepSize * (ret(i, i) - M);
    }
    return ret;
}

Mat
addWithFactor(const Mat& A, const Mat& B, double x)
{
    Mat ret = A;
    for (size_t i = 0; i < (size_t) A.rows(); ++i)
	for (size_t j = 0; j < (size_t) A.cols(); ++j)
	    ret(i, j) += B(i, j) * x;
    return ret;
}

double 
factorFitness(const Mat& S, const Mat& dS, const Triplets& trips, double M,
	      double mu)
{
    Mat S1 = addWithFactor(S, dS, mu);
//    S1 = quickProjectPSDM(S1, M);
    S1 = projectPSDtr(S1, M);
    double temp;
    return modelFit(trips, S1, temp);
 }

double
findOptimalFactor(const Mat& S, const Mat& dS, const Triplets& trips, double M)
{
    double temp;
    double baseFitness = modelFit(trips, S, temp);
    double bracket = 10.0;
    double x0 = 1.0;
    double x1 = 0.38 * bracket;
    double x2 = (0.38 + 0.38 * 0.62) * bracket;
    double x3 = bracket;

    double f1 = factorFitness(S, dS, trips, M, x1);
    double f2 = factorFitness(S, dS, trips, M, x2);
    cout << "starting in bracket: " 
	 << "(" << x0 << ", )" 
	 << "(" << x1 << ", " << f1 << ")" 
	 << "(" << x2 << ", " << f2 << ")" 
	 << "(" << x3 << ", )" << endl;
    for (size_t iter = 0; iter < 4; ++iter){
	
	
	if (f2 <= f1){
	    x0 = x1;
	    x1 = x2;
	    x2 = 0.62 * x1 + 0.38 * x3;
	    f1 = f2;
	    f2 = factorFitness(S, dS, trips, M, x2);
	}
	else{
	    x3 = x2;
	    x2 = x1;
	    x1 = 0.62 * x2 + 0.38 * x0;
	    f2 = f1;
	    f1 = factorFitness(S, dS, trips, M, x1);
	}
	cout << iter << ": " 
	     << "(" << x0 << ", )" 
	     << "(" << x1 << ", " << f1 << ")" 
	     << "(" << x2 << ", " << f2 << ")" 
	     << "(" << x3 << ", )" << endl;

    }    
    if (baseFitness < f1 && baseFitness < f2)
	return 0.0;
    if (f2 < f1)
	return x2;
    else
	return x1;
}

void
calculateSimilarity(const Triplets& trips, Mat& S, double M, 
		    const Triplets& heldouts)
{
    size_t n = trips.maxId()+1;
    S = Mat::eye(n, n);

    size_t m = trips.size();
    double lastFitness = 1e100;
    for (size_t iter = 1; iter < 100; ++iter){
	double expectedFitness;
	cout << "------------------------------------" << endl;
	cout << "iteration " << iter << endl;

	cout << "sample" << endl;
	double fitness = modelFit(trips, S, expectedFitness);
	cout << "    fitness: " << fitness << endl;
	cout << "    expected fitness: " << expectedFitness << endl;

	cout << "heldouts" << endl;
	double heldoutFit = modelFit(heldouts, S, expectedFitness);
	cout << "    fit to heldouts: " <<  heldoutFit << endl;
	cout << "    expected fit to heldouts: " <<  expectedFitness << endl;

	Mat dS = Mat::zeros(n, n);
	for (size_t i = 0; i < m; ++i){
	    size_t x = trips._x[i];
	    size_t a = trips._a[i];
	    size_t b = trips._b[i];
	    double p = prob(x, b, a, S);
	    double q = 1 - p;
	    dS(x, a) += p;
	    dS(a, x) += p;
	    dS(x, b) -= q;
	    dS(b, x) -= q;
	}
//	double mu = findOptimalFactor(S, dS, trips, M);
	double mu = 0.01 / sqrt(iter);
	S = addWithFactor(S, dS, mu);
	S = projectPSDtr(S, M);
	
	double temp;
	fitness = modelFit(trips, S, temp);
//	if (lastFitness < fitness + 0.0001 && iter > 20)
//	    break; 
	lastFitness = fitness;

    }
    double temp;
    double fitness = modelFit(trips, S, temp);
    cout << "------------------------------------" << endl;
    cout << "done" << endl;
    cout << "fitness: " << fitness << endl;
}



template<class B>
void
splitString(const std::basic_string<B>& s, 
            const B& seperator,
            std::vector<std::basic_string<B> >& rBits)
{
    rBits.clear();
    
    for (size_t i = 0; i < s.length();)
    {
        size_t j = s.find(seperator, i);
        if (j > i)
            rBits.push_back(s.substr(i, j - i));
        if (j == std::string::npos)
            break;
        i = j + 1;
    }
}

void
readFile(const string& fileName, Triplets& rTrips)
{
    cout << "parsing file " << fileName << endl;
    size_t oldSize = rTrips.size();
    ifstream tripsFile(fileName.c_str());
    
    if (!tripsFile.is_open()){
        cout << "Could not open file " << fileName << endl;
        exit(1);
    }
    size_t lineNum = 0;
    while (!tripsFile.eof()){
	++lineNum;
        string line;
        getline(tripsFile, line);
	vector<string> lineParts;
	splitString(line, ' ', lineParts);
	if (lineParts.size() < 3){
	    if (lineParts.size() > 0)
		cout << "faulty line " << lineNum << ":" << endl
		     << line << endl;
	}
	else{
	    size_t x = atoi(lineParts[0].c_str());
	    size_t a = atoi(lineParts[1].c_str());
	    size_t b = atoi(lineParts[2].c_str());
	    rTrips.addTriplet(x, a, b);
	}
    }
    tripsFile.close();
    cout << "found " << rTrips.size() - oldSize << " comparisons" << endl;
}



void
readDirectory(const path& dirPath, const regex& filesDesc, Triplets& rTrips)
{
    if (!exists(dirPath)) 
	return;
    directory_iterator end_itr;
    for (directory_iterator it(dirPath); it != end_itr; ++it)
	if (!is_directory(it->status()) && regex_match(it->leaf(), filesDesc))
	    readFile(it->path().string(), rTrips);
}

map<size_t, string> 
getImageFiles(const string& dataset)
{
    string fileName = string("../images/") + dataset + string("/ids.txt");
    ifstream f(fileName.c_str());
    
    if (!f.is_open()){
        cout << "Could not open file " << fileName << endl;
        exit(1);
    }

    map<size_t, string> ret;
    size_t lineNum = 0;
    while (!f.eof()){
        string line;
        getline(f, line);
	ret[lineNum] = line;
	++lineNum;
    }
    return ret;
    
}


void 
svdPlot(const Mat& S, const path& dirName, const string& dataset, 
	const string& fileName)
{

    string img_base_url = string("file:///home/tamuz/dev/simexp/images/") 
	+  dataset + string("/");

    size_t small_image_size = 70;
    size_t page_size[] = {1500, 1000, small_image_size};
    size_t large_image_size = 200;

    ofstream f1(fileName.c_str());
    
    if (!f1.is_open()){
        cout << "Could not open file " << fileName << endl;
        exit(1);
    }
    
    f1 << "<html>\n"
       << "<body>\n";

    size_t n = S.rows();
    Mat S0 = Mat::zeros(n, n);
    for (size_t j = 0; j < n; ++j){
	double colMean = 0.0;
	for (size_t i = 0; i < n; ++i)
	    colMean += S(i, j);
	colMean = colMean / n;
	for (size_t i = 0; i < n; ++i)
	    S0(i, j) = S(i, j) - colMean;
    }
	
    Mat U(n, n);
    Mat V(n, n);
    Vec sigVec(n);
    LaSVD_IP(S0, sigVec, U, V);
//    cout << sigVec;

    for (size_t j = 0; j < 2; ++j){
	double rowMin = 1e100;
	for (size_t i = 0; i < n; ++i)
	    if (rowMin > U(i, j))
		rowMin = U(i, j);
	for (size_t i = 0; i < n; ++i)
	    U(i, j) = U(i, j) - rowMin;

	double rowMax = -1e100;
	for (size_t i = 0; i < n; ++i)
	    if (rowMax < U(i, j))
		rowMax = U(i, j);
	for (size_t i = 0; i < n; ++i)
	    U(i, j) = U(i, j) / rowMax;
    }
    map<size_t, string> img_files = getImageFiles(dataset);
    cout << "found " << img_files.size() << " images in list" << endl;
    for (size_t i = 0; i < n; ++i){
	size_t xpos = page_size[0] * U(i, 0);
	size_t ypos = page_size[1] * U(i, 1);
	size_t z_image_size = small_image_size;
	{
	    ostringstream s;
	    s <<  "<span onmouseover = \"document.img" << i 
	      << ".width = " << large_image_size 
	      << "; document.img" << i
	      << ".height = " << large_image_size
	      << ";\" onmouseout = \"document.img" << i
	      << ".width = " << z_image_size
	      << "; document.img" << i
	      << ".height = " << z_image_size
	      << "\">\n";
	    f1 << s.str();
	}
	{
	    ostringstream s;
	    s << "<img name = \"img" << i << "\""
	      << " src = \"" << img_base_url << img_files[i] << "\""
	      << " style = \"position:absolute;"
	      << " left: " << xpos << "; top: " << ypos << ";\""
	      << " height = " << z_image_size 
	      << " width = " << z_image_size 
	      << " title=\"" << img_files[i] << "\"/>\n";
	    f1 << s.str();
	}
	f1 << "</span>\n";
    }
    
    for (size_t j = 0; j < n; ++j){
	size_t ypos = j * (small_image_size + 10) + page_size[1];
	set<size_t> usedIds;
	for (size_t i = 0; i < 10; ++i){
	    size_t xpos = i * (small_image_size + 10);

	    double rowMax = 0;
	    size_t id = 0;
	    for (size_t k = 0; k < n; ++k){
		double p = prob(j, k, j, S);
		if (p > rowMax && usedIds.count(k) == 0){
		    rowMax = p;
		    id = k;
		}
	    }
	    usedIds.insert(id);
	    {
		ostringstream s;
		s << "<img"
		  << " src = \"" << img_base_url << img_files[id] << "\""
		  << " style = \"position:absolute; left: " << xpos
		  << "; top:" << ypos << ";\"" 
		  << " height = " << small_image_size 
		  << " width = " << small_image_size 
		  <<  " title=\"" << img_files[id]<< "\"/>\n";
		f1 << s.str();
	    }
	    
	    
	}
    }
}

void
testSVD()
{
    size_t n = 50;
    Mat M(n, n);
    for (size_t i = 0 ; i < n; ++i)
	for (size_t j = i ; j < n; ++j)
	    M(i, j) = M(j, i) = (1.0 * rand()) / RAND_MAX - 0.5;
    projectPSDtr(M, 1);
}

int 
main(int argc, char* argv[])
{
//    testSVD();    return 0;
    if (argc < 3){
	cout << "usage: " << argv[0] 
	     << " <triplets directory> <dataset>" << endl;
	exit(-1);
    }
    Triplets trips;
    regex fileDesc(".*\\.out");
    readDirectory(argv[1], fileDesc, trips);

    Triplets heldouts;
    readFile(string(argv[1]) + string("heldout"), heldouts);
    
    
    cout << "read " << trips._x.size() << " triplets" << endl;
    cout << "maximum id: " << trips.maxId() << endl;
    cout << "distinct ids: " << trips._ids.size() << endl;
    cout << "read " << heldouts._x.size() << " heldout triplets" << endl;
//    for (size_t i = 0; i < trips._x.size(); ++i)
//	cout << trips._x[i] << " " << trips._a[i] << " " << trips._b[i] << endl;

    Mat S;
    calculateSimilarity(trips, S, 100.0, heldouts);
    
    svdPlot(S, argv[1], argv[2], "../images/svd.html");
    
    return 0;
}
