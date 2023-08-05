##############################
robotframework-localization
##############################
|license|

*************************************************************
Robot Framework Localization Helper 
*************************************************************

A python library and CLI to help testers to internationalize and localize robot test cases. 

============
Installation
============
robotLocalization can be installed with pip/pipenv:

.. code:: bash

    pip install robotframework-localization
    pipenv install robotframework-localization

=====
Usage
=====

robotLocalization can be used in two modes as a get_variables function or a CLI.  
The get_variables function can be used in the robot test case to load strings from
properpties files by providing a language fallback mechanism. 
robotLocalization CLI provides functionalities to help testers to internationalize 
test cases. 

.. code:: java

    # resources/sample.properties
    msg = Hello, World!

.. code:: java

    # resources/sample_ja.properties
    msg = みなさん、こんにちは!

.. code:: robotframework

    #   sample.robot
    # 
    #   $ robot --variable language:en sample.robot
    #   $ robot --variable language:ja sample.robot
    #   
    *** Settings ***
    Library     SeleniumLibrary
    Variables   robotLocalization     ${LANGUAGE}    resources/sample.properties    verbose=True

    *** Variables ***
    ${LANGUAGE}              en     # default LANGUAGE.  This can be replaced by --variable option.

    *** Test Cases ***
    Test Case 1
        [Documentation]    robotLocalization Sample
        Log To Console     ${msg}
        Log Variables

Getting variables from get_variables function
***********************************************

robotLocalization provides get_variabes function which can be specified 
in the robot Variables statement. 

Syntax in robot test
--------------------

Variables   **robotLocalization**   *localeId*   *path or file list* *pathOptions*

*localeId* specifies the locale or language of the properties being used.  It is used 
to load strings from properties files in the properties files in the specified path list 
or files.  If specified locale is not available, English propereties will be used. 

*pathOptions*
^^^^^^^^^^^^^

verbose=            True or False
filetype=           file type

Examples
--------
Variables   **robotLocalization**   en   ${PROJECT_REPO_PATH}

Accessing variables from robot code. 

Internationalization Helper CLI 
********************************

The xpt command helps testers to internationalize robot test cases.  

**robotLocalization** *operand* *file_patterns* *language-list* 

Analyze Mode
------------

In the analyze mode, robotLocalization CLI reports the localizable strings in robot test and 
cadicases of available strings in existing properties files from properties files in the
specified path list. 

.. code:: bash 

    robotLocalization [*path list()] --analyze [*robot_file*]

--analyze
^^^^^^^^^^^
Specifies a robot test case.  Typically, this robot file contains Xpath specifications
with UI elements or robot variable specifications used in other keywords. 

Extract Mode
------------

The extract mode is used to extract strings from a specified robot file.  
It also generates internationalized robot files by replacing localizable strings
with variables references. 

--extract
^^^^^^^^^^
Specifies a robot test case to extract strings. 

--output_bundle
^^^^^^^^^^^^^^^^

Specifies a bundle file which can be used to store product properties into a single file. 
This options is only valid if *--use_bundle* option is enaled. 

--output_properties
^^^^^^^^^^^^^^^^^^^^

Specifies a properties file to store localizable strings. If *--use_bundle* is specified,
only strings not available in product properties files are stored.  

--output_robot|--outr
^^^^^^^^^^^^^^^^^^^^^^

Specifies a robot file by internationalizing the robot file specifeid wit --extract option.
All localizable strings will be replaced by variable references.  A string with "# i18n:OK "
comments are ignored. 

--use_bundle|--use_keys
^^^^^^^^^^^^^^^^^^^^^^^^
--use_bundle options checks the availablity of strings in the specified product properties files.
If found, it uses strings there. 

--multi_trans
^^^^^^^^^^^^^
--multi_trans options checks the translated value for locales specified with --bundle_locale option
and checks the multiple translations.   If variant translation found, it extends the Xpath expression 
to use "OR" condition to use all of the variant translations. 

--playwright
^^^^^^^^^^^^
--playwright options checks the css/xpath specification for Playwright when externalizing the robot
variables.  This option is useful when robot Framework is used with the Playwright for Python. 

Dump Mode
---------

--dump
^^^^^^^

--dump option generates list all the variables loaded from properties files.  


.. |license| image:: https://img.shields.io/badge/license-MIT-blue.svg
.. |robotLocalization_icon| image:: robotLocalization.png
