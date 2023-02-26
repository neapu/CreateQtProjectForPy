#!/usr/bin/env python

import os
import sys

project_name = ''

# 项目名称
if len(sys.argv) == 2:
    project_name = sys.argv[1]

if project_name == '':
    project_name = input('项目名称[new_project]:')

if project_name == '':
    project_name = 'new_project'

# 生成目录
if os.path.exists(project_name):
    print(f'文件夹[{project_name}]已存在')
    exit(-1)
os.makedirs(project_name)

cmakelist_content = f"""cmake_minimum_required(VERSION 3.5)

project({project_name} VERSION 0.1 LANGUAGES CXX)

set(CMAKE_AUTOUIC ON)
set(CMAKE_AUTOMOC ON)
set(CMAKE_AUTORCC ON)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

find_package(QT NAMES Qt6 Qt5 REQUIRED COMPONENTS Widgets)
find_package(Qt${{QT_VERSION_MAJOR}} REQUIRED COMPONENTS Widgets)

file(GLOB SRC_FILES CONFIGURE_DEPENDS src/*.cpp)
file(GLOB UI_FILES CONFIGURE_DEPENDS src/*.ui)

set(PROJECT_SOURCES
        ${{SRC_FILES}}
        ${{UI_FILES}}
)

if(${{QT_VERSION_MAJOR}} GREATER_EQUAL 6)
    qt_add_executable(${{PROJECT_NAME}}
        MANUAL_FINALIZATION
        ${{PROJECT_SOURCES}}
    )
# Define target properties for Android with Qt 6 as:
#    set_property(TARGET {project_name} APPEND PROPERTY QT_ANDROID_PACKAGE_SOURCE_DIR
#                 ${{CMAKE_CURRENT_SOURCE_DIR}}/android)
# For more information, see https://doc.qt.io/qt-6/qt-add-executable.html#target-creation
else()
    if(ANDROID)
        add_library(${{PROJECT_NAME}} SHARED
            ${{PROJECT_SOURCES}}
        )
# Define properties for Android with Qt 5 after find_package() calls as:
#    set(ANDROID_PACKAGE_SOURCE_DIR "${{CMAKE_CURRENT_SOURCE_DIR}}/android")
    else()
        add_executable(${{PROJECT_NAME}}
            ${{PROJECT_SOURCES}}
        )
    endif()
endif()

target_link_libraries(${{PROJECT_NAME}} PRIVATE Qt${{QT_VERSION_MAJOR}}::Widgets)

set_target_properties(${{PROJECT_NAME}} PROPERTIES
    MACOSX_BUNDLE_GUI_IDENTIFIER my.example.com
    MACOSX_BUNDLE_BUNDLE_VERSION ${{PROJECT_VERSION}}
    MACOSX_BUNDLE_SHORT_VERSION_STRING ${{PROJECT_VERSION_MAJOR}}.${{PROJECT_VERSION_MINOR}}
    MACOSX_BUNDLE TRUE
    WIN32_EXECUTABLE TRUE
)

install(TARGETS ${{PROJECT_NAME}}
    BUNDLE DESTINATION .
    LIBRARY DESTINATION ${{CMAKE_INSTALL_LIBDIR}})

if(QT_VERSION_MAJOR EQUAL 6)
    qt_finalize_executable(${{PROJECT_NAME}})
endif()

"""

with open(os.path.join(project_name, "CMakeLists.txt"), "w") as f:
    f.write(cmakelist_content)

if not os.path.exists(project_name+"/src"):
    os.makedirs(project_name+"/src")

main_content = """#include "widget.h"
#include <QApplication>

int main(int argc, char *argv[])
{
    QApplication a(argc, argv);
    Widget w;
    w.show();
    return a.exec();
}

"""

with open(project_name+"/src/main.cpp", "w") as f:
    f.write(main_content)

widget_cpp_content = """#include "widget.h"
#include "./ui_widget.h"

Widget::Widget(QWidget *parent)
    : QWidget(parent)
    , ui(new Ui::Widget)
{
    ui->setupUi(this);
}

Widget::~Widget()
{
    delete ui;
}

"""

with open(project_name+"/src/widget.cpp", "w") as f:
    f.write(widget_cpp_content)

widget_h_content = """#ifndef WIDGET_H
#define WIDGET_H

#include <QWidget>

QT_BEGIN_NAMESPACE
namespace Ui { class Widget; }
QT_END_NAMESPACE

class Widget : public QWidget
{
    Q_OBJECT

public:
    Widget(QWidget *parent = nullptr);
    ~Widget();

private:
    Ui::Widget *ui;
};
#endif // WIDGET_H

"""

with open(project_name+"/src/widget.h", "w") as f:
    f.write(widget_h_content)

widget_ui_content = """<?xml version="1.0" encoding="UTF-8"?>
<ui version="4.0">
 <class>Widget</class>
 <widget class="QWidget" name="Widget">
  <property name="geometry">
   <rect>
    <x>0</x>
    <y>0</y>
    <width>800</width>
    <height>600</height>
   </rect>
  </property>
  <property name="windowTitle">
   <string>Widget</string>
  </property>
 </widget>
 <resources/>
 <connections/>
</ui>

"""

with open(project_name+"/src/widget.ui", "w") as f:
    f.write(widget_ui_content)

print(f"""Create Success.Run:
    cd {project_name}
    cmake -S. -Bbuild_gcc -DCMAKE_PREFIX_PATH=/path/to/qt -DCMAKE_CXX_COMPILER=g++ -G "Ninja"
    cmake --build ./build_gcc
generate project
""")