
include_directories(
    ${Boost_INCLUDE_DIRS}
    ${OCC_INCLUDE_DIR}
    ${PYTHON_INCLUDE_PATH}
    ${ZLIB_INCLUDE_DIR}
    ${XERCESC_INCLUDE_DIR}
)

set(Phuru_LIBS
    FreeCADApp
)

SET(Phuru_SRCS
    AppPhuru.cpp
    AppPhuruPy.cpp
    PreCompiled.cpp
    PreCompiled.h
)

add_library(Phuru SHARED ${Phuru_SRCS})
target_link_libraries(Phuru ${Phuru_LIBS})


fc_target_copy_resource(Phuru 
    ${CMAKE_SOURCE_DIR}/src/Mod/Phuru
    ${CMAKE_BINARY_DIR}/Mod/Phuru
    Init.py)

SET_BIN_DIR(Phuru Phuru /Mod/Phuru)
SET_PYTHON_PREFIX_SUFFIX(Phuru)

install(TARGETS Phuru DESTINATION ${CMAKE_INSTALL_LIBDIR})
