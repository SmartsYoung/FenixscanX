@echo OFF
@rem  Copyright (c) 2015 nexB Inc. http://www.nexb.com/ - All rights reserved.
@rem  


@rem  A minimal shell wrapper to the CLI entry point

set SCANENGINE_ROOT_DIR=%~dp0

set SCANENGINE_CMD_LINE_ARGS=
set SCANENGINE_CONFIGURED_PYTHON=%SCANENGINE_ROOT_DIR%\Scripts\python.exe

@rem Collect all command line arguments in a variable
:collectarg
 if ""%1""=="""" goto continue
 call set SCANENGINE_CMD_LINE_ARGS=%SCANENGINE_CMD_LINE_ARGS% %1
 shift
 goto collectarg

:continue


if not exist "%SCANENGINE_CONFIGURED_PYTHON%" goto configure
goto scanengine

:configure
 echo * Configuring ScanEngine for first use...
 set CONFIGURE_QUIET=1
 call "%SCANENGINE_ROOT_DIR%\configure" etc/conf
 if %errorlevel% neq 0 (
    exit /b %errorlevel%
 )

:scanengine
"%SCANENGINE_ROOT_DIR%\Scripts\extractcode" %SCANENGINE_CMD_LINE_ARGS%

:EOS
