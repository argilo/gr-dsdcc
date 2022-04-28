find_package(PkgConfig)

PKG_CHECK_MODULES(PC_GR_DSDCC gnuradio-dsdcc)

FIND_PATH(
    GR_DSDCC_INCLUDE_DIRS
    NAMES gnuradio/dsdcc/api.h
    HINTS $ENV{DSDCC_DIR}/include
        ${PC_DSDCC_INCLUDEDIR}
    PATHS ${CMAKE_INSTALL_PREFIX}/include
          /usr/local/include
          /usr/include
)

FIND_LIBRARY(
    GR_DSDCC_LIBRARIES
    NAMES gnuradio-dsdcc
    HINTS $ENV{DSDCC_DIR}/lib
        ${PC_DSDCC_LIBDIR}
    PATHS ${CMAKE_INSTALL_PREFIX}/lib
          ${CMAKE_INSTALL_PREFIX}/lib64
          /usr/local/lib
          /usr/local/lib64
          /usr/lib
          /usr/lib64
          )

include("${CMAKE_CURRENT_LIST_DIR}/gnuradio-dsdccTarget.cmake")

INCLUDE(FindPackageHandleStandardArgs)
FIND_PACKAGE_HANDLE_STANDARD_ARGS(GR_DSDCC DEFAULT_MSG GR_DSDCC_LIBRARIES GR_DSDCC_INCLUDE_DIRS)
MARK_AS_ADVANCED(GR_DSDCC_LIBRARIES GR_DSDCC_INCLUDE_DIRS)
