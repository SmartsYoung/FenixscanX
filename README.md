# FenixscanX

Special Thanks : Aboutcode project -- what makes our tools **SPDX-Native**

### What is FenixscanX
A tool writtern by Python (vue+elementui+Django) for open source copyright compliance and in future it can support other compliance scan.

### Why FenixscanX?
“Open source compliance is the process by which users, integrators and developers of open source software observe copyright notices and satisfy license obligations for their open source software components” — The Linux Foundation

### What FenixscanX now looks like?
Now FenixscanX is in its prototype, it's only a cli-tool for scan software copyright and maybe other metadata. 

emmm ... Vue-UI and Django_rest_api is on the way.

Our purpose is to build a expert system to help people who uses opensource software to well obey their license and copyright obligations.

### How to build?
Build environment: Ubuntu Linux 20.04 (recommended) / M$ Windows 10 

Build tool: VC buildTool (if M$ Windows) | Python 3.8 | pip 20.3.3+

* **PAY ATTENTION** : If you are in M$ windows, you should install VC buildTool and Windows SDK firstly. You can get it from (https://visualstudio.microsoft.com/zh-hans/thank-you-downloading-visual-studio/?sku=BuildTools&rel=16)

1 - Now you can simply git clone the code 

2 - Go into "scanengine" folder

3 - just run "./configure" | in Windows 10 , just run ".\configure"

* **PAY ATTENTION** : If using venv, you should config pyvenv for your linux/windows

Have a cup of coffee and wait for everything to be done.

### How to use?

1. scan the copyright info  

You can type : 

scanengine -c -n 2 --json-pp copyright.json samples 

in Windows 10 :

.\scanengine -c -n 2 --json-pp copyright.json samples

**-c** means copyright scan

**-n 2** means 2 threads will be used in scan

**--json-pp** means json will be used for output format

**copyright.json** means the output report's name

**samples** means what folder you will scan

2. scan the license info  

You can type : 

scanengine -li -n 2 --json-pp license.json samples 

in Windows 10 :

.\scanengine -c -n 2 --json-pp license.json samples

**-li** means license scan

For more details command, use scanengine --help  

3. parse the json file

The scanned json file can be analyzed through the [visual UI](https://github.com/nexB/scancode-workbench/releases)


