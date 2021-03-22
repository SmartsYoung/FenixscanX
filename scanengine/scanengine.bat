@echo OFF
@rem Copyright (c) nexB Inc. http://www.nexb.com/ - All rights reserved.

@rem  A wrapper to ScanEngine command line entry point

set SCANENGINE_ROOT_DIR=%~dp0
set SCANENGINE_CONFIGURED_PYTHON=%SCANENGINE_ROOT_DIR%Scripts\python.exe

@rem Collect all command line arguments in a variable
@rem Use a trailing space in the next line sets the variable to an empty string (rather than unseting it)
set "SCANENGINE_CMD_LINE_ARGS= "

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
@rem FIXME: we did not set a given Python PATH
set CONFIGURE_QUIET=1
call "%SCANENGINE_ROOT_DIR%configure" etc/conf

@rem Return a proper return code on failure
if %errorlevel% neq 0 (
    exit /b %errorlevel%
)

:scanengine
@rem without this things may not always work on Windows 10, but this makes things slower
set PYTHONDONTWRITEBYTECODE=1

"%SCANENGINE_ROOT_DIR%Scripts\scanengine" %SCANENGINE_CMD_LINE_ARGS%
