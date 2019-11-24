
如果你正在使用Python3，虚拟环境已经成为内置模块，可以直接通过如下命令来创建它：

$ python3 -m venv venv
译者注：这个命令不一定能够执行成功，比如译者在Ubuntu16.04环境下执行，提示需要先安装对应的依赖。sudo apt-get install python3-venv

使用这个命令来让Python运行venv包，它会创建一个名为venv的虚拟环境。 命令中的第一个“venv”是Python虚拟环境包的名称，第二个是要用于这个特定环境的虚拟环境名称。 如果你觉得这样很混乱，可以用你自定义的虚拟环境名字替换第二个venv。我习惯在项目目录中创建了名为venv的虚拟环境，所以无论何时cd到一个项目中，都会找到相应的虚拟环境。



Flask-Migrate通过flask命令暴露来它的子命令。 你已经看过flask run，这是一个Flask本身的子命令。 Flask-Migrate添加了flask db子命令来管理与数据库迁移相关的所有事情。 那么让我们通过运行flask db init来创建microblog的迁移存储库：

flask db migrate -m "users table"

flask db migrate命令不会对数据库进行任何更改，只会生成迁移脚本。 要将更改应用到数据库，必须使用flask db upgrade命令。


pip3 freeze > requirements.txt


从requirements.txt安装依赖库
pip3 install -r requirements.txt