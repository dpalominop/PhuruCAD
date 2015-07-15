
include_directories(
    ${CMAKE_SOURCE_DIR}/src
    ${CMAKE_CURRENT_BINARY_DIR}
    ${Boost_INCLUDE_DIRS}
    ${COIN3D_INCLUDE_DIR}
    ${QT_INCLUDE_DIR}
    ${ZLIB_INCLUDE_DIR}
    ${PYTHON_INCLUDE_PATH}
    ${XERCESC_INCLUDE_DIR}
)

set(PhuruGui_LIBS
    Phuru
    FreeCADGui
)

qt4_add_resources(Phuru_QRC_SRCS Resources/Phuru.qrc)

SET(PhuruGui_SRCS
    ${Phuru_QRC_SRCS}
    AppPhuruGui.cpp
    AppPhuruGuiPy.cpp
    Command.cpp
    PreCompiled.cpp
    PreCompiled.h
    Workbench.cpp
    Workbench.h
)

add_library(PhuruGui SHARED ${PhuruGui_SRCS})
target_link_libraries(PhuruGui ${PhuruGui_LIBS})

fc_target_copy_resource(PhuruGui 
    ${CMAKE_SOURCE_DIR}/src/Mod/Phuru
    ${CMAKE_BINARY_DIR}/Mod/Phuru
    InitGui.py)

SET_BIN_DIR(PhuruGui PhuruGui /Mod/Phuru)
SET_PYTHON_PREFIX_SUFFIX(PhuruGui)
    
install(TARGETS PhuruGui DESTINATION ${CMAKE_INSTALL_LIBDIR})
