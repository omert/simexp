mexfiles = logistic_deriv.mexglx confusion_matrix.mexglx model_likelihood.mexglx distance_deriv.mexglx update_matrix.mexglx produce_adaptive.mexglx information_gain.mexglx predict_using_bank.mexglx

all: $(mexfiles)

$(mexfiles): %.mexglx: %.cpp model.h Mat.h Makefile
	mex  CXXFLAGS#"-Wall -O3 -pedantic" $< 
