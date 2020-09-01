#include <cstdio>
#include <python3.6m/Python.h>
#include <opencv2/opencv.hpp>

#include "facedetectcnn.h"

#define DETECT_BUFFER_SIZE 0x20000

using namespace cv;

extern "C"
{

void
py_init_parameters()
{
    printf("No need. I guess\n");
}

void
py_facedetect_cnn(void * const imgData, 
                  const int imgCols, 
                  const int imgRows, 
                  void * const output)
{

    facedetect_cnn((int *)output, (unsigned char *)imgData, imgCols, imgRows, imgCols * 3);
    
    // printf("Receiving image\n");
    // //printf("Step: %d\n", img.step);
    // //printf("PResult: %d\n", *pResult);

    // Mat img(Size(imgCols, imgRows), CV_8UC3, imgData);
    // imshow("window", img);
    // waitKey();
    // destroyAllWindows();
}

} /* extern "C" */
