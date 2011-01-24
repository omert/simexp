mexfiles = logistic_deriv.mexglx confusion_matrix.mexglx model_likelihood.mexglx distance_deriv.mexglx update_matrix.mexglx produce_adaptive.mexglx

all: $(mexfiles)

$(mexfiles): %.mexglx: %.cpp model.h Mat.h Makefile
	mex  CFLAGS="-Wall -O3 -pedantic" $< 
