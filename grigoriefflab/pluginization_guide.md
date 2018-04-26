Scipion's next release will use plugins instead of the current packages. 
These plugins will be delivered as pip modules, and will have their own repository independent from Scipion. 
This guide uses the package 
[grigoriefflab](https://github.com/I2PC/scipion/tree/v1.2/pyworkflow/em/packages/grigoriefflab)
to describe the steps to migrate a package to a pip-based plugin. 
It is assumed that you have a working version of Scipion installed.

Table of Contents
=================

* [0. Before you start](#0-before-you-start)
* [1. Adding plugin.py file](#1-adding-pluginpy-file)
    * [1.1 Environment Variables](#11-environment-variables)
    * [1.2 Installation of plugin binaries](#12-installation-of-plugin-binaries)
     
* [2. Installing as pip module](#2-installing-as-pip-module)
    * [2.1 Create pip distribution](#21-create-pip-distribution)
    * [2.2 Packaging and installing via pip locally (development mode)](#22-packaging-and-installing-via-pip-locally-development-mode)
        * [2.2.1 Remove previous installation of the package from Scipion](#221-remove-previous-installation-of-the-package-from-scipion)
        * [2.2.2 Download json with list of plugins](#222-download-json-with-list-of-plugins)
        * [2.2.3 Install plugin](#223-install-plugin)
    * [2.3 Create and upload distribution](#23-create-and-upload-distribution)
    * [2.4 Install from pip](#24-install-from-pip)
* [3. Wrapping up](#3-wrapping-up)



# 0. Before you start

* #### Communicate! :-)
    Make sure nobody is working on that package before you pluginize it (or coordinate with whoever is working on it so
    nobody has to do the work twice).
    Ask in our slack channel (scipion.slack.com) and/or open a github issue. 
    If you aren't part of our slack channel please
    ask for an invite by sending an email to (?).

* #### Move the package folder outside of Scipion

    * To make following this guide easier, open a terminal and export 
    the path to the directory of Scipion as scipion_home:
        ```bash
        export scipion_home="your/path/to/scipion/dir"
        ```
    * Copy the package folder as it is to a different directory (an empty folder outside of scipion):
        ```bash
        mkdir scipion_grigoriefflab && cp $scipion_home/pyworkflow/em/packages/grigoriefflab grigoriefflab_plugin
        ```
    * Export the new directory of the package as plugin_home:
        ```bash
        export plugin_home="some/path/to/scipion_grigoriefflab"
        ```
    * Remove the package from its original location inside scipion:
        ```bash
        rm -r $scipion_home/pyworkflow/em/packages/grigoriefflab 
        ```
    * Make a link to the new location of the package (we will remove this later):
        ```bash
        ln -s $plugin_home/grigoriefflab $scipion_home/pyworkflow/em/packages/grigoriefflab
        ```
    * If you don't have them, install the package's binaries. In the case of grigoriefflab there are many binaries,
        but for the purpose of this guide we'll work with ctffind:
        ```bash
        $scipion_home/scipion install ctffind4 --no-xmipp
        ```
    * We need the `requests` pip module, and it is only installed by default from the pluginization branch of Scipion,
    so it is possible that you don't have it.
        ```bash
        $scipion_home/scipion install requests --no-xmipp
        ```   
    


# 1. Adding plugin.py file

The goal of this file is to isolate in the plugin three main aspects that are 
currently handled by Scipion: environment variables, installation and the logo 
(if there is one). `plugin.py` needs to be in the top level of our package, and in 
this case we will move the logo here too (and remove it from its 
[original location](https://github.com/I2PC/scipion/blob/v1.2/pyworkflow/resources/brandeis_logo.png)).
```bash
$ mv $scipion_home/pyworkflow/resources/brandeis_logo.png $plugin_home && touch $plugin_home/plugin.py
```

<pre>
grigoriefflab/
├── bibtex.py
<b>├── brandeis_logo.png</b> 
├── constants.py
├── convert.py
├── dataimport.py
├── grigoriefflab.py
├── __init__.py
<b>├── plugin.py</b>
├── protocol_ctffind.py
├── protocol_frealign_base.py
....
..
├── tests
│   ├── __init__.py
│   ├── test_protocols_grigoriefflab_magdist.py
│   ├── test_protocols_grigoriefflab_movies.py
│   └── test_protocols_grigoriefflab.py
├── viewer.py
├── wizard.py
</pre>

###  1.1 Environment Variables
These are now located in [`scipion.template` packages section](https://github.com/I2PC/scipion/blob/v1.2/config/templates/scipion.template#L19). We need to locate the ones that belong to our plugin, comment or remove them, and store them in a dictionary in `plugin.py`. 

Comment our package's variables in  
**[`scipion.template`](https://github.com/I2PC/scipion/blob/v1.2/config/templates/scipion.template)**:

```python
[PACKAGES]
EM_ROOT = software/em

BSOFT_HOME = %(EM_ROOT)s/bsoft-1.9.0
CRYOEF_HOME = %(EM_ROOT)s/cryoEF-1.1.0
CRYOEF_HOME = %(EM_ROOT)s/cryoEF-1.1.0
# CTFFIND_HOME = %(EM_ROOT)s/ctffind-3.6 ############## COMMENT THIS: now in plugin.py ########################
# CTFFIND4_HOME = %(EM_ROOT)s/ctffind4-4.1.8 ############## COMMENT THIS: now in plugin.py ########################
CCP4_HOME =  %(EM_ROOT)s/ccp4-6.5
[ . . . ]
ETHAN_HOME = %(EM_ROOT)s/ethan-1.2
# FREALIGN_HOME = %(EM_ROOT)s/frealign-9.07 ############## COMMENT THIS: now in plugin.py ########################
GAUTOMATCH_HOME = %(EM_ROOT)s/Gautomatch-0.53
[ . . . ]
LOCALREC_RELION_HOME = %(EM_ROOT)s/relion-1.4
# MAGDIST_HOME = %(EM_ROOT)s/mag_distortion-1.0.1  ############## COMMENT THIS: now in plugin.py #####################
MATLAB_BINDIR = None
MATLAB_LIBDIR = None
MOTIONCORR_HOME = %(EM_ROOT)s/motioncorr-2.1
[ . . . ]
SPIDER_HOME = %(EM_ROOT)s/spider-21.13/spider
# SUMMOVIE_HOME = %(EM_ROOT)s/summovie-1.0.2 ############## COMMENT THIS: now in plugin.py ########################
# UNBLUR_HOME = %(EM_ROOT)s/unblur-1.0.2 ############## COMMENT THIS: now in plugin.py ########################
XMIPP_HOME = %(EM_ROOT)s/xmipp
```

If you don't know which are the ones that belong to your package, you'll need to poke around to find them
(usually in `__init__.py` or in the .py file named after the package). In the case of grigoriefflab we have 
more variables than usual, but it is common to have just one `SOMEPACKAGE_HOME`. The name of these variables is stored in 
**[`grigoriefflab.py`](https://github.com/I2PC/scipion/blob/v1.2/pyworkflow/em/packages/grigoriefflab/grigoriefflab.py)**,
so it is recommended to move these to our plugin and import them here. In general, we consider it a good practice to
have the name of the environment variables in their own python variables, so we recommend to follow this approach
if your package's code is using directly the string to get env vars.

**`grigoriefflab.py`** :
```python
from plugin import * # Import everything from plugin.py - we'll need things that move there!

[. . .]
# MAGDIST_HOME_VAR = 'MAGDIST_HOME' # 'MAGDIST_HOME' is in scipion.template. Move this to plugin.py

#SUMMOVIE_HOME = 'SUMMOVIE_HOME' # 'SUMMOVIE_HOME' is in scipion.template. Move this to plugin.py

#UNBLUR_HOME = 'UNBLUR_HOME' # 'UNBLUR_HOME' is in scipion.template. Move this to plugin.py

#FREALIGN_HOME_VAR = 'FREALIGN_HOME' # 'FREALIGN_HOME' is in scipion.template. Move this to plugin.py

#CTFFIND4_HOME = 'CTFFIND4_HOME' # 'CTFFIND4_HOME' is in scipion.template. Move this to plugin.py
#CTFFIND_HOME = 'CTFFIND_HOME' # 'CTFFIND_HOME' is in scipion.template. Move this to plugin.py

CTFFIND3 = 'ctffind3.exe' # NOT a var in scipion.template. We do not need to move it.
[. . .]
```

Now we store them in a dict in **`plugin.py`**. Note how paths are now built using `os.path.join` and how we substitute
 `%(EM_ROOT)s` (used in `scipion.template`) with `os.environ['EM_ROOT']`:

**`plugin.py`**:
``` python
import os

MAGDIST_HOME_VAR = 'MAGDIST_HOME'
SUMMOVIE_HOME = 'SUMMOVIE_HOME'
UNBLUR_HOME = 'UNBLUR_HOME'
FREALIGN_HOME_VAR = 'FREALIGN_HOME'
CTFFIND4_HOME = 'CTFFIND4_HOME'
CTFFIND_HOME = 'CTFFIND_HOME'

VARS = {
    MAGDIST_HOME_VAR: os.path.join(os.environ['EM_ROOT'], 'mag_distortion-1.0.1'),
    SUMMOVIE_HOME: os.path.join(os.environ['EM_ROOT'], 'summovie-1.0.2'),
    UNBLUR_HOME:   os.path.join(os.environ['EM_ROOT'], 'unblur-1.0.2'),
    FREALIGN_HOME_VAR: os.path.join(os.environ['EM_ROOT'], 'frealign-9.07'),
    CTFFIND4_HOME: os.path.join(os.environ['EM_ROOT'], 'ctffind4-4.1.8'),
    CTFFIND_HOME:  os.path.join(os.environ['EM_ROOT'], 'ctffind-3.6'),

}
```

### 1.2 Installation of plugin binaries
The next step is to isolate the code responsible of the installation of the binaries. 
The case of `grigoriefflab` is a particularly complex one, since there are many different 
binaries grouped in one plugin (it is common to find one binary per plugin).

We comment the code that is currently responsible of the installation in Scipion's script [**`install.py`**](https://github.com/I2PC/scipion/blob/v1.2/install/script.py#L368) :

```python
#  ************************************************************************
#  *                                                                      *
#  *                       External (EM) Packages                         *
#  *                                                                      *
#  ************************************************************************

# 'commands' is a list of (command, [targets]) to run after installation.


[ . . . ]

#env.addPackage('ctffind', version='3.6',
#                tar='ctffind_V3.5.tgz')
# 
# env.addPackage('ctffind4', version='4.0.15',
#                tar='ctffind_V4.0.15.tgz')
# 
# env.addPackage('ctffind4', version='4.1.5',
#                tar='ctffind_V4.1.5.tgz')
# 
# env.addPackage('ctffind4', version='4.1.8',
#                tar='ctffind_V4.1.8.tgz')
# 
# env.addPackage('summovie', version='1.0.2',
#                tar='summovie_1.0.2.tgz')
# 
# env.addPackage('unblur', version='1.0.15',
#                tar='unblur_1.0_150529.tgz')
# 
# env.addPackage('unblur', version='1.0.2',
#                tar='unblur_1.0.2.tgz')

[ . . . ]

#env.addPackage('frealign', version='9.07',
#               tar='frealign_v9.07.tgz')
#
[ . . . ]

#env.addPackage('mag_distortion', version='1.0.1',
#               tar='mag_distortion-1.0.1.tgz')


```

And we put it in the function registerPluginBinaries in **`plugin.py`**. Please note how we have added `default=True` to
one of the ctffind4 options - as we will see later, this means that this binary will be installed automatically when we
get this plugin unless told otherwise.

**`plugin.py`**:
```python
def registerPluginBinaries(env):
    env.addPackage('ctffind', version='3.6',
                   tar='ctffind_V3.5.tgz')

    env.addPackage('ctffind4', version='4.0.15',
                   tar='ctffind_V4.0.15.tgz')

    env.addPackage('ctffind4', version='4.1.5',
                   tar='ctffind_V4.1.5.tgz')

    env.addPackage('ctffind4', version='4.1.8',
                   tar='ctffind_V4.1.8.tgz',
                   default=True  # Optional: install this binary by default
                    )

    env.addPackage('summovie', version='1.0.2',
                   tar='summovie_1.0.2.tgz')

    env.addPackage('unblur', version='1.0.15',
                   tar='unblur_1.0_150529.tgz')

    env.addPackage('unblur', version='1.0.2',
                   tar='unblur_1.0.2.tgz')

    env.addPackage('frealign', version='9.07',
                   tar='frealign_v9.07.tgz')

    env.addPackage('mag_distortion', version='1.0.1',
                   tar='mag_distortion-1.0.1.tgz')
```

The next step is to add a Plugin object and import it in the plugin's `__init__.py`. 
It is important to assign it to a variable called **`_plugin`** so that Scipion can find it.

**`plugin.py`**:
```python
from pyworkflow.plugin import Plugin

_plugin = Plugin('grigoriefflab',
                 version="1.0.0",
                 configVars=VARS,
                 logo="brandeis_logo.png",
                 registerFunction=registerPluginBinaries)
```

Finally, we'll have to take into account how the package uses the things that we've defined in _plugin.
In grigoriefflab, we'll have to import `_plugin` in `__init__.py` and change the value of the logo. By doing this import,
we already initialize the default values of the environment variables (see the `__init__` function from `Plugin`).
Please note that this step likely be slightly different in each individual case - you'll probably have to import
 _plugin in __init__.py in every case, but the use of its environment variables needs to be carefully reviewed.

**`__init__.py`**:
```python
"""
This sub-package contains data and protocol classes
wrapping Grigorieff Lab programs at Brandeis
"""
from plugin import _plugin  # import at the very top
from bibtex import _bibtex # Load bibtex dict with references
from grigoriefflab import *

_logo = _plugin.logo  # Load logo from plugin
```
Here's the finished [plugin.py]() file. 
You can see the possible parameters of the Plugin class [here](https://github.com/yaizar/scipion/blob/pluginization_install_config/pyworkflow/plugin.py).

At this point we can test if we didn't break anything (we probably did ;D) and our package is working in plugin mode.
For this, temporariliy remove the default variables of the plugin (those we defined in `VARS`)
from our `~/.config/scipion/scipion.conf`. Since we are testing with ctffind4, we remove CTFFIND4_HOME.


**`~/.config/scipion/scipion.conf`**:
```python
[PACKAGES]
BSOFT_HOME = %(EM_ROOT)s/bsoft-1.9.0
CCP4_HOME = software/em/ccp4-6.5
CHIMERA_HEADLESS_HOME = %(EM_ROOT)s/chimera_headless
CHIMERA_HOME = %(EM_ROOT)s/chimera-1.10.1
CRYOEF_HOME = software/em/cryoEF-1.1.0 
# CTFFIND4_HOME = %(EM_ROOT)s/ctffind4-4.1.8 # REMOVE THE VARS WE WANT TO TEST
CTFFIND_HOME = %(EM_ROOT)s/ctffind-3.6
DOGPICKER_HOME = %(EM_ROOT)s/dogpicker-0.2.1
```


Next, launch scipion and try to run one of the plugin's tests. 
Please note that for this step you need to have the protocol's binaries installed! 

* Open terminal and find tests
    ```bash
    $scipion_home/scipion test --show | grep grigorieff
    ```
* Locate your test in the ouptut:
    ```bash
     scipion test em.packages.grigoriefflab.tests.test_protocols_grigoriefflab_magdist
        scipion test em.packages.grigoriefflab.tests.test_protocols_grigoriefflab_magdist.TestMagDist
     scipion test em.packages.grigoriefflab.tests.test_protocols_grigoriefflab_movies
        scipion test em.packages.grigoriefflab.tests.test_protocols_grigoriefflab_movies.TestUnblur
        scipion test em.packages.grigoriefflab.tests.test_protocols_grigoriefflab_movies.TestSummovie
     scipion test em.packages.grigoriefflab.tests.test_protocols_grigoriefflab
        scipion test em.packages.grigoriefflab.tests.test_protocols_grigoriefflab.TestImportParticles
        scipion test em.packages.grigoriefflab.tests.test_protocols_grigoriefflab.TestFrealignRefine
        scipion test em.packages.grigoriefflab.tests.test_protocols_grigoriefflab.TestFrealignClassify
        scipion test em.packages.grigoriefflab.tests.test_protocols_grigoriefflab.TestBrandeisCtffind4
        scipion test em.packages.grigoriefflab.tests.test_protocols_grigoriefflab.TestBrandeisCtffind
    ```
* Paste in terminal:
    ```bash
    scipion test em.packages.grigoriefflab.tests.test_protocols_grigoriefflab.TestBrandeisCtffind4
    ```
* The ouptut of the test tells us if test executed OK:
    ```bash
    [ RUN   OK ] TestBrandeisCtffind4.testCtffind4V22 (46.883 secs)
    
    [==========] run 2 tests (97.652 secs)
    [  PASSED  ] 2 tests
    
    ```
* Open the test project:
    ```bash
    scipion last
    ```
    First, inspect the protocol output to make sure there's nothing weird; then, open the
    protocol box to see if our logo is there. It's important to do this step because
    if we don't open the GUI we won't be able to detect logo related issues.
    
    
# 2. Installing as pip module

### 2.1 Create pip distribution

We'll explain below the steps followed to convert the package into a pip module that we can
 upload to pypi. Many of these steps are not scipion-specific, so it is recommended to check an external source (like 
[this one](https://python-packaging.readthedocs.io/en/latest/index.html) or 
[this one](https://packaging.python.org/tutorials/distributing-packages/)) if you have doubts about pip packaging.

We add four files to the folder that contains grigoriefflab: 
`CHANGES.txt`, `setup.py`, `MANIFEST.in`, `README.rst`. (This is
why we copied grigoriefflab in an empty folder).
<pre>
scipion_grigoriefflab
<b>├── CHANGES.txt</b>
<b>├── .gitignore</b>
├── grigoriefflab
│   ├── bibtex.py
│   ├── brandeis_logo.png
...
..
<b>├── MANIFEST.in</b>
<b>├── README.rst</b>
<b>└── setup.py</b>
</pre>

* **`setup.py`**
    This is the most important one. It needs to call the setup function with, at least,
    the required arguments. Here we present a synthesized version, see [this one]() for more
    detailed comments.
    **`setup.py`**:
    ```python
    # Always prefer setuptools over distutils
    from setuptools import setup, find_packages
    # To use a consistent encoding
    from codecs import open
    from os import path
    
    here = path.abspath(path.dirname(__file__))
    
    # Get the long description from the README file
    with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
        long_description = f.read()
    
    setup(
        name='scipion_grigoriefflab',  # Required
        version='1.0a',  # Required
        description='A python wrapper to use Ctffind, Unblur & others in Scipion',  # Required
        long_description=long_description,  # Optional
        url='https://github.com/yaizar/scipion_grigoriefflab',  # Optional
        author='Probably Gregory',  # Optional
        author_email='some@human.com',  # Optional
        keywords='scipion cryoem imageprocessing scipion-1.2',  # Optional
        packages=find_packages(),
        package_data={  #!!!!!! Required if we have a logo!!!!!
           'grigoriefflab': ['brandeis_logo.png'],
        }
    
    )
    ```
    
* **`CHANGES.txt`**,  **`MANIFEST.in`** and `.gitignore` (All optional):

    We have added a `changes.txt` where we will add a summary of changes each time we 
    modify the plugin. The `MANIFEST.in` is needed so that our .txt file is included
    when we do the distribution. We also put our .gitignore here.
    
    **`changes.txt`**:
    ```text
    v1.0.0, 23/04/2018 -- First commit
    ```
    **`MANIFEST.in`**:
    ```text
    include *.txt
    ```
    **`.gitignore`**:
    ```text
    ### Python binaries
    *.pyc
    *.pyo
    
    # Other
    dist/
    /*.egg-info
    venv
    
    [. . . ]
    
    ```

### 2.2 Packaging and installing via pip locally (development mode)
#### 2.2.1 Remove previous installation of the package from Scipion
* Remove binaries
    ```bash
    rm -rf $scipion_home/software/em/ctffind*
    ```
* Remove symlink
    ```bash
    rm $scipion_home/pyworkflow/em/packages/grigoriefflab
        
    ```
#### 2.2.2 Download json with list of plugins
Scipion requests a json list of available plugins from `http://scipion.i2pc.es/getplugins` and uses metadata from pypi
 to filter which packages are available for the current Scipion version. Since we want to test our pip plugin before
 we upload it to pypi, we will read locally a file like the one provided in the website, with our plugin added.
 
* In a directory of your choice, add a `plugins.json` file with the appropriate info for your plugin:

     **`plugins.json`**:
     ```json
     {
        "scipion_grigoriefflab": {
            "name":"grigoriefflab",
            "pipName": "scipion_grigoriefflab",
            "pluginSourceUrl":"/path/to/your/scipion_grigoriefflab"
        }
    }
    ```
    Note that when you add the key `pluginSourceUrl`, Scipion will use pip to install the plugin from 
    that directory. Once this is done, you can make changes in your plugin and test them immediately,
    without needing to install it again. If this key is missing, Scipion will install from pypi.
 
* In the **`VARIABLES`** section of your **`~/.config/scipion/scipion.conf`**, add variable `SCIPION_PLUGIN_JSON`
  (remember to replace the example with the right path):
    <pre>
    [. . .]
    [VARIABLES]
    SCIPION_NOTES_PROGRAM =
    SCIPION_NOTES_ARGS =
    SCIPION_NOTES_FILE = notes.txt
    SCIPION_NOTIFY = False
    <b>SCIPION_PLUGIN_JSON=/home/desktop/yaiza/plugins.json</b>
    </pre>
    
#### 2.2.3 Install plugin

* In your terminal:
    ```bash
    $scipion_home/scipion install_plugin -p scipion_grigoriefflab
    ```
  If no errors happen, we get an output similar to this one:
  ```
    /home/yaiza/git/scipion/software/bin/python /home/yaiza/git/scipion/scipion install_plugin -p scipion_grigoriefflab
    
    Scipion  pluginization_install_config (2018-04-11) 0ee533a
    
    python  /home/yaiza/git/scipion/install/install-plugin.py /home/yaiza/git/scipion/scipion install_plugin -p scipion_grigoriefflab
    Building scipion_grigoriefflab ...
    python /home/yaiza/git/scipion/software/lib/python2.7/site-packages/pip install /home/yaiza/git/scipion_grigoriefflab
    Processing /home/yaiza/git/scipion_grigoriefflab
    Installing collected packages: scipion-grigoriefflab
      Running setup.py install for scipion-grigoriefflab: started
        Running setup.py install for scipion-grigoriefflab: finished with status 'done'
    Successfully installed scipion-grigoriefflab-1.0a0
    You are using pip version 9.0.3, however version 10.0.1 is available.
    You should consider upgrading via the 'pip install --upgrade pip' command.
    Done (1.01 seconds)
    [. . .]
    Building ctffind4-4.1.8 ...
      Skipping command: wget -nv -c -O /home/yaiza/git/scipion/software/em/ctffind_V4.1.8.tgz.part http://scipion.cnb.csic.es/downloads/scipion/software/em/ctffind_V4.1.8.tgz
    mv -v /home/yaiza/git/scipion/software/em/ctffind_V4.1.8.tgz.part /home/yaiza/git/scipion/software/em/ctffind_V4.1.8.tgz
      All targets exist.
    cd /home/yaiza/git/scipion/software/em
    tar -xzf ctffind_V4.1.8.tgz
    cd /home/yaiza/git/scipion/software/em/
    Link 'ctffind4-4.1.8 -> ctffind_V4.1.8'
    Created link: 'ctffind4-4.1.8 -> ctffind_V4.1.8'
    Done (0.20 seconds)
    
    Process finished with exit code 0
  ```
  
  Now you can run the test again and check your plugin is ready to upload it to pypi.

#### 2.3 Create and upload distribution
To upload your distribution to pypi, you'll need to 
[create an account](https://packaging.python.org/tutorials/distributing-packages/#create-an-account).

* Install twine if you don't have it
    ```bash
    pip install twine
    
    ```
    
* Create the source distribution (at least! You can also create a Built distribution. Read more in the official
[packaging guide](https://packaging.python.org/tutorials/distributing-packages/#setup-cfg))
    ```bash
    cd $plugin_home
    python setup.py sdist
    ```
    It is convenient to check your `*egg-info/SOURCES.TXT` and see if you miss any file (pay special attention to
    non-python files that you might have forgot to include in `MANIFEST.in` or in your `setup.py`, like the logo).

* Upload the distribution **WITH EARLIEST COMPATIBLE SCIPION VERSION IN THE COMMENTS**. 
    ```bash
    cd $plugin_home && twine upload dist/* -c "scipion-1.2"
    
    ```
    This means that this release we're uploading will be available for Scipion version 1.2 or higher. 
    The scipion version must follow the pattern used above (scipion-X.Y(.Z))
    Now our plugin is on [pypi](https://pypi.org/project/scipion-grigoriefflab/).
    
#### 2.4 Install from pip
* Uninstall plugin:
    ```bash
    $scipion_home/scipion uninstall_plugin -p grigoriefflab
    ```
* Remove `SCIPION_PLUGIN_JSON` from **`~/.config/scipion/scipion.conf`** (we exit development mode)
* Install
    ```bash
    $scipion_home/scipion install_plugin -p grigoriefflab
    ```    
* Test again
    ```bash
    scipion test em.packages.grigoriefflab.tests.test_protocols_grigoriefflab.TestBrandeisCtffind4
    ```
    
    If the test passed, the plugin is ready to go :)

# 3. Wrapping up
To finish, we need to create a pull request to Scipion repo with the old package removed.
    