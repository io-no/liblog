# liblog: Unified Logging Across Python Packages
`liblog` is a Python library designed to make easier the management of logging across multiple Python packages. This library aims to provide a unified and consistent logging mechanism, ensuring that log outputs are coherent regardless of the package source.

`liblog` is built on top of Python's standard logging library to ensure maximum compatibility and rely on the features this library offer.

## Key Features
- **Coherent Logging**: Ensures all logging activities across different packages adhere to a consistent format and standard.
- **Automatic Debug Level Setting**: Facilitates the parsing of command-line arguments (argv) to automatically set the debug level, simplifying the configuration process for your logging needs.
- **Origin Traceability**: Each log message is clearly labeled with its package of origin, making it easier to trace logs back to their source.

## Installation
```bash
python3 -m pip install git+https://github.com/io-no/liblog
```

## Getting Started with liblog
To integrate `liblog` into your project, start by importing it into your package. Although liblog can perform lazy automatic registration in some cases, explicitly registering your package is recommended to ensure that no log messages are missed.
`liblog` seamlessly fetches and registers the name of your package, which is also displayed during logging. 

```python
from liblog import liblog

# Explicitly register your package
liblog.registerPackage()
```

Once registered, you can use `liblog` for logging with the following methods:
```python
liblog.exception("This is an exception message associated with my package")
liblog.critical("This is a critical message associated with my package")
liblog.error("This is an error message associated with my package")
liblog.warning("This is a warning message associated with my package")
liblog.info("This is an info message associated with my package")
liblog.debug("This is a debug message associated with my package")
```

`liblog` automatically recognizes the calling package and adapts accordingly. 

If you prefer, you can also access the standard Python `logging.Logger` object. Indeed, `liblog` exposes an attribute equal to the package name that contains the `logging.Logger` object. For example, if your package is named `mypackage`, you can access the `logging.Logger` object as follows:
```python
logger = liblog.mypackage
logger.error("This is an error message associated with my package")
```
Moreover, you can also access the `logging.Logger` object using the `getLogger` method:
```python
logger = liblog.getLogger("mypackage")
logger.error("This is an error message associated with my package")
```
When called without arguments, the `getLogger` method returns the logger object of the package that called it.
```python
logger = liblog.getLogger()
logger.error("This is an error message associated with my package")
```

You can set the logging level for your package using the `setLevel` method:
```python
liblog.setLevel("DEBUG")
```
The level will be only applied to the logger object of your package and any child logger objects.

### Child Loggers
For scenarios requiring multiple loggers within the same package, `liblog` supports child loggers, which function as named loggers under the primary package logger. To create and utilize a child logger:
```python
# Register and use a child logger
liblog.registerChild('child_logger_name')
liblog.child_logger_name.warning("Message from child logger")
```
You can also access the child logger using the `getChild` method:
```python
child_logger = liblog.getChild('child_logger_name')
child_logger.warning("Message from child logger")
```

### Advanced Level Configuration
By default, the logging level is set to `INFO`. However, if a logger's name (either package or child) is passed as a script argument, its level is set to `DEBUG`.

`ligblog` also supports the `SILENT` level, which completely disables logging.

To uniformly adjust the logging level across all loggers managed by liblog:
```python
liblog.setGlobalLevel("DEBUG")
```

### Example
```python
from liblog import liblog

# Register the main package
liblog.registerPackage()

# Issue a warning from the main package
liblog.warning("This is a warning message from the main package")

# Register and use a child logger
liblog.registerChild('exampleChild')
liblog.exampleChild.warning("This is a warning message from a child logger")

# Set global logging level to DEBUG
liblog.setGlobalLevel("DEBUG")
```

