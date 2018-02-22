INCLUDE(FindPkgConfig)
PKG_CHECK_MODULES(PC_COMINA comina)

FIND_PATH(
    COMINA_INCLUDE_DIRS
    NAMES comina/api.h
    HINTS $ENV{COMINA_DIR}/include
        ${PC_COMINA_INCLUDEDIR}
    PATHS ${CMAKE_INSTALL_PREFIX}/include
          /usr/local/include
          /usr/include
)

FIND_LIBRARY(
    COMINA_LIBRARIES
    NAMES gnuradio-comina
    HINTS $ENV{COMINA_DIR}/lib
        ${PC_COMINA_LIBDIR}
    PATHS ${CMAKE_INSTALL_PREFIX}/lib
          ${CMAKE_INSTALL_PREFIX}/lib64
          /usr/local/lib
          /usr/local/lib64
          /usr/lib
          /usr/lib64
)

INCLUDE(FindPackageHandleStandardArgs)
FIND_PACKAGE_HANDLE_STANDARD_ARGS(COMINA DEFAULT_MSG COMINA_LIBRARIES COMINA_INCLUDE_DIRS)
MARK_AS_ADVANCED(COMINA_LIBRARIES COMINA_INCLUDE_DIRS)

