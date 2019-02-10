
mkdir build
cd build
cmake .. -DCMAKE_INSTALL_PREFIX=~/.local -DORB_SLAM2_DIR=~/.local -DPYTHON_NUMPY_INCLUDE_DIR=~/.local/lib/python3.5/site-packages/numpy/core/include
make  #&& sudo porg -lp orbslam2-python make install
make install