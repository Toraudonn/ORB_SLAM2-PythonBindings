
## ORB-SLAM2

```
./build.sh

cd build
sudo make install
```

## ORB-SLAM2-PythonBinding

```

mkdir build
cd build
cmake ..
make
sudo make install

```

## bind it to python

```

rm ~/.pyenv/versions/anaconda3-5.2.0/lib/python3.6/site-packages/orbslam2.so

sudo ln -s /usr/local/lib/python3.5/dist-packages/orbslam2.so ~/.pyenv/versions/anaconda3-5.2.0/lib/python3.6/site-packages/orbslam2.so

```