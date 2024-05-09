# Simple Python Selenium UI Automation Framework

This is a simple UI automation framework built with:
- Python: 3.6.8, pytest 7.1.0, Selenium: 4.0.0.a7 and GitHub Actions CI
<br>



## Features

- Easy-to-use UI automation framework.
- Based on popular Python libraries: Pytest and Selenium.
- Supports Chrome,Firefox and Remote browsers for UI testing.
- Provides setup and teardown for setting up and managing WebDriver instances. Preparing a clean session ready for testcase execution, with zero manual intervention required.
- Clean execution and side effect free testcase execution.
- Free order execution of testcases.
- Supports different drivers : Firefox, Chrome.
- Supports pytest reports and custom debug logs

## Getting Started

### Prerequisites

- Python 3.6.8
- Windows 10/11 32/64 bit
- Git CLI
- Anaconda Distribution

### Usage locally

1. Clone this repository 
```
git clone https://github.com/Sathvik-Malgikar/HPE_CTY_Project1_ClusterStor
```
2. change directory to this repository
```
cd HPE_CTY_Project1_ClusterStor
```

3. Install required dependencies using these commands to read the hpe_env.yml file and setup dependencies accordingly, this will take some time
```
conda env create -f hpe_env.yml
conda activate hpe_env
```
4. 
- Modify config.ini file in infrastructure folder and set the placeholders below to your google account to be used for tests. <br/> ```WARNING : All data present in this account's google drive is wiped out permanently !!```<br/> 
- [Optional] The delay params can be tweaked as needed, use only in case of unusually slow network. Increasing delay helps to avoid false negatives in case of high network latency.<br/> 

5. Lastly,
 - Download the below provided prerequisites.zip containing dummy testfiles for all 3 test suites
 - Extract the zip into your user folder  ```C:\Users\<your-username>```
<br/> -- OR --<br/>
Make use of bat script provided to do the extraction<br/>
( prerequisites.zip must be in same folder as bat file before running )

- #### [Click here to download Prerequisites](https://dl.dropbox.com/scl/fi/nlvt2cu52axbyx6tdb5en/prerequisites.zip?rlkey=z2k6n4vj064gk1z65tqzs3o5a&st=h5xuv9nl&dl=0)
- #### [Click here to download extraction script](https://dl.dropbox.com/scl/fi/xi9bmfxtay8svzk6lgfy0/extract_to_userfolder.bat?rlkey=o38j9zrpvj4w771eos5nv8tff&st=kotblukf&dl=0)


### Dependencies / modules used:
1. Pytest
2. Selenium
3. PyAutoGUI
4. Pyperclip
5. win10toast
6. pytest-html-reporter

Checkout hpe_env.yml for more info !
