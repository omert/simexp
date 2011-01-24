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
