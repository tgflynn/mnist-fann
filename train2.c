
#include <stdio.h>
#include <stdlib.h>
#include <time.h>

#include "fann.h"


struct fann*
createNet()
{
  const float learning_rate = 1.e-3;
  const unsigned int num_input = 784;
  const unsigned int num_output = 10;
  const unsigned int num_layers = 3;
  const unsigned int num_neurons_hidden = 300;
  const float desired_error = 0.0001;
  const unsigned int max_iterations = 500000;
  const unsigned int iterations_between_reports = 1;

  struct fann *ann = fann_create_standard( num_layers,
					   num_input, 
					   num_neurons_hidden, 
					   num_output );

  fann_set_activation_function_hidden( ann, FANN_SIGMOID );
  fann_set_activation_function_output( ann, FANN_SIGMOID );
  fann_set_learning_rate( ann, learning_rate );


  return ann;
}

int argmax( fann_type* y,
	    int        nelements )
{
  int i;
  fann_type maxval = 0.0;
  int maxarg = -1;
  for( i  = 0; i < nelements; ++i )  {
    if( y[i] > maxval )  {
      maxval = y[i];
      maxarg = i;
    }
  }
  return maxarg;
}

double
calcClassificationError( struct fann*            ann,
			 struct fann_train_data* testData )
{
  double err = 0;
  int i;
  fann_type* out;
  int noutputs = testData->num_output;
  for( i = 0; i < testData->num_data; ++i )  {
    fann_type* x = testData->input[i]; 
    fann_type* y = testData->output[i];
    out = fann_run( ann ,x );
    int netClass = argmax( out, noutputs );
    int trueClass = argmax( y, noutputs );
    if( netClass != trueClass )  {
      err += 1.0;
    }
  }
  err /= (double)testData->num_data;
  return err;
}

void 
trainNet( struct fann*            ann, 
	  struct fann_train_data* trainData, 
	  struct fann_train_data* testData,
	  int                     numIterations )
{
  int i;
  int j;
  char timestr[500];
  time_t t;
  struct tm *tmp;

  printf( "trainNet: Beginning training\n" );
  for( i = 0; i < numIterations; ++i )  {
    for( j = 0; j < trainData->num_data; ++j )  {
      fann_type* x = trainData->input[j]; 
      fann_type* y = trainData->output[j];
      fann_train( ann, x, y );
    }
    double err = calcClassificationError( ann, testData );
    t = time( NULL );
    tmp = localtime( &t );

    if ( strftime( timestr, sizeof(timestr), "%Y-%m-%d %H:%M:%S", tmp ) == 0 ) {
      fprintf( stderr, "strftime returned 0" );
      exit( EXIT_FAILURE );
    }

    printf( "%s epoch = %6d, classification error = %8.4f%%\n", timestr, i, 100.0 * err ); 
  }
}

int main( int argc, char* argv[] )
{
  
  char* trainFile = "train.fann";
  char* testFile = "test.fann";

  srand( 1 );

  printf( "Loading training data\n" );
  struct fann_train_data* trainData = fann_read_train_from_file( trainFile );

  printf( "Loading test data\n" );
  struct fann_train_data* testData = fann_read_train_from_file( testFile );

  printf( "Creating net\n" );
  struct fann* ann = createNet();

  printf( "Training net\n" );
  trainNet( ann, trainData, testData, 500 );
    
  printf( "Saving net\n" );
  fann_save( ann, "fann.net" );
  
  fann_destroy( ann );
  
  return 0;
}
