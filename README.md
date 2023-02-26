# 创建QT Widget工程

## Windows

1. 使用

    把项目路径添加到环境变量

    直接在命令行运行

    ```shell
    CreateQtProject hello_world
    ```

2. 配置visual studio

    1. 在项目文件夹中`右键`->`使用Visual Studio打开`

    2. 在解决方案管理器中`右键CmakeLists.txt`->`CMake设置`

    3. 在CMake命令参数中配置`-DCMAKE_PREFIX_PATH=/path/to/qt/cmake`

        例如 `-DCMAKE_PREFIX_PATH=E:/Qt/6.4.2/msvc2019_64/lib/cmake`

    4. `右键CmakeLists.txt`->`配置缓存`

    5. `右键CmakeLists.txt`->`生成`

    6. 在上方的`本地调试器`中选择可执行文件

    此时运行调试会找不到qt的动态库文件，需要配置调试环境变量

    点击`调试`菜单,选择`调试和启动ProjectName的设置`

    在`configurations`中添加环境变量配置

    ```json
    "env": {
        "PATH": "/path/to/qt/bin"
    }
    ```

    完整示例：

    ```json
    {
        "version": "0.2.1",
        "defaults": {},
        "configurations": [
            {
                "type": "default",
                "project": "CMakeLists.txt",
                "projectTarget": "ProjectName.exe",
                "name": "ProjectName.exe",
                "env": {
                    "PATH": "E:\\Qt\\6.4.2\\msvc2019_64\\bin"
                }
            }
        ]
    }
    ```