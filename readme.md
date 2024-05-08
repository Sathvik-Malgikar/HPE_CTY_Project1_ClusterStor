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
4. Create config.ini file in infrastructure folder and set the placeholders below to your google account to be used for tests. 
```
; Testing requires a Google account to be used.
; WARNING : All data present in this account's google drive is wiped out permanently !!
[Account Credentials]
email = <your-email-here>
password = <your-password-here>

; These can be tweaked as needed, use only in case of unusually slow network. Increasing delay helps to avoid false negatives in case of high network latency.
[Delay Parameters]
very_small_delay = 0.7
small_delay = 2
medium_delay = 3
large_delay = 5
```

5. Create pytest.ini file in root folder(HPE_CTY_Project1_ClusterStor) with following configurations :
```
[pytest]
addopts = --html-report=results/report.html --self-contained-html

```

6. Lastly extract the below provided prerequisites.zip containing dummy testfiles for all 3 test suites into your user folder ```C:\Users\<your-username>```

- #### [Click here to download Prerequisites](https://dl.dropbox.com/scl/fi/nlvt2cu52axbyx6tdb5en/prerequisites.zip?rlkey=z2k6n4vj064gk1z65tqzs3o5a&st=h5xuv9nl&dl=0)

### Dependencies / modules used:
1. Pytest
2. Selenium
3. PyAutoGUI
4. Pyperclip
5. win10toast
6. pytest-html-reporter

Checkout hpe_env.yml for more info !
