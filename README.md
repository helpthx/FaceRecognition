
# FaceRecognition

<<<<<<< HEAD

![](https://img.shields.io/eclipse-marketplace/last-update/notepad4e.svg)

![](https://img.shields.io/dub/l/vibe-d.svg)

![](https://img.shields.io/badge/Version-v1-green.svg)


![](https://img.shields.io/pypi/pyversions/Django.svg)

![](https://img.shields.io/powershellgallery/p/:packageName.svg)



<p align="justify">
Simple project about face recognition. Based on college project [DS_2_2018](https://github.com/helpthx/DS_2_2018) . Aiming to use face recognition to control access at college's restaurant. The system was embedded in a Raspberry pi 3(SoC) and tested in different environments. There are a local database base on sqlite3, A server in Apache to editing the database while face recognition system are running and relay to send signal to open the door - control by Raspberry Pi GPIO.</p>
=======
<p align="center">
 
<a href="#backers" alt="">
        <img src="https://img.shields.io/eclipse-marketplace/last-update/notepad4e.svg" /></a>
        
<a href="#backers" alt="">
        <img src="https://img.shields.io/dub/l/vibe-d.svg" /></a>
        
<a href="#backers" alt="">
        <img src="https://img.shields.io/badge/Version-v1-green.svg" /></a>
        
<a href="#backers" alt="">
       <img src="https://img.shields.io/pypi/pyversions/Django.svg" /></a>
 
<a href="#backers" alt="">
       <img src="https://img.shields.io/powershellgallery/p/:packageName.svg" /></a>
  
<a href="#backers" alt="">
       <img src="https://img.shields.io/github/repo-size/badges/shields.svg" /></a>

</p>


Simple project about face recognition. Based on college project [DS_2_2018](https://github.com/helpthx/DS_2_2018) . Aiming to use face recognition to control access at college's restaurant. The system was embedded in a Raspberry pi 3(SoC) and tested in different environments. There are a local database base on sqlite3, a server in Apache to editing the database while face recognition system are running and relay to send signal to open the door - control by Raspberry Pi GPIO.
>>>>>>> c460e3593c6e1db950ec73ae4f05b89ad6cf101d

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

```
OpenCv 3.4.4
Qt version: 4.8.7
SIP version: 4.19.7
PyQt version: 4.12.1
sqlite3 2, 6, 0
Numpy 
```

### Installing

* Create an empty Folder named **"dataset"** in the same directory where the python scripts are 
* Create an empty folder called **"trainer"** In same directory 


## Running the tests


* Create an empty Folder named **"dataset"** in the same directory where the python scripts are.
* Create an empty folder called **"trainer"** in the same directory.
* Run on terminal **"python3 exe.py"**.
* Type **"3"** and press enter **"3 -> Edit database"**.
* Type **"1 -> Table create"** and a sqlite3 table will be create.
* Make a new register typing **"1"**.
* Write your name.
* Write your id number (max 8 numbers)
* Look to your camera and wait(Photos will be save in **"dataset"**).
* OpenCV API will training the photos in the file **"trainer"**
* Than you can start **"2 -> Face Recognition"**.



* In **"3 -> Edit database"**.
* Adding Credits. Just type your id number and how much money to add.


## Built With

* [OpenCV](https://opencv.org/) - API used
* [Python3](https://www.python.org/download/releases/3.0/) - Main language
* [NumPy](http://www.numpy.org/) - Key API 


## Authors

* **João Vitor Rodrigues Baptista** - *Initial work* - [helpthx](https://github.com/helpthx)

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* Based on original code by Anirban Kar: [Face-Recognition](https://github.com/thecodacus/Face-Recognition)
 
