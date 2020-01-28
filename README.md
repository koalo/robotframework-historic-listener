# robotframework-historic-listener

Listener to push robotframework execution results to MySQL (for Robotframework Historic report)

![PyPI version](https://badge.fury.io/py/robotframework-historic-listener.svg)
[![Downloads](https://pepy.tech/badge/robotframework-historic)](https://pepy.tech/project/robotframework-historic-listener)
![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square)
![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)
![Open Source Love png1](https://badges.frapsoft.com/os/v1/open-source.png?v=103)
[![HitCount](http://hits.dwyl.io/adiralashiva8/robotframework-historic-listener.svg)](http://hits.dwyl.io/adiralashiva8/robotframework-historic-listener)

---

## Installation

 - Install `robotframework-historic-listener` 

    ```
    pip install robotframework-historic-listener
    ```

--- 

## Usage

   Robotframework Historic report required following information, users must pass respective info while using listener
    
    - SQL_HOST --> mysql hosted machine ip address (default: localhost)
    - SQL_USER_NAME --> mysql user name (default: superuser)
    - SQL_PASSWORD --> mysql password (default: passw0rd)
    - RFH_PROJECT_NAME --> project name in robotframework historic
    - RFH_EXECUTION_NAME --> execution info
    

 - Use `robotframework-historic-listener` while executing tests

   ```
   > robot --listener robotframework_historic_listener.listener
    -v SQL_HOST:"<SQL_HOSTED_IP:3306>"
    -v SQL_USER_NAME:"<NAME>"
    -v SQL_PASSWORD:"<PWD>"
    -v RFH_PROJECT_NAME:"<PROJECT-NAME>"
    -v RFH_EXECUTION_NAME:"<EXECUTION-INFO>"
   ```

   __Example:__
   ```
   > robot --listener robotframework_historic_listener.listener
    -v SQL_HOST:"10.30.2.150:3306"
    -v SQL_USER_NAME:"admin"
    -v SQL_PASSWORD:"Welcome1!"
    -v RFH_PROJECT_NAME:"projec1"
    -v RFH_EXECUTION_NAME:"Smoke test on v1.0" <suite>
   ```

## Using variable file

 - Create variable file like `config.py`

 - Place all variables info
    ```
    # MYSQL location ie., localhost or 127.0.0.1:18007 etc.,
    SQL_HOST = "localhost"

    # Database and its credentials
    SQL_USER_NAME = "superuser"
    SQL_PASSWORD = "passw0rd"
    RFH_PROJECT_NAME = "projectname"

    # Execution details
    RFH_EXECUTION_NAME = "Smoke Test on v1.0"
    ```

 - Use variable file while using listener

   ```
   > robot --listener robotframework_historic_listener.listener -V config.py <suite>
   ```

---

> For more info refer to [robotframework-historic](https://github.com/adiralashiva8/robotframework-historic)