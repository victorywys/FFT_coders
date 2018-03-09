# wav2mid

## 一. 环境配置
版本支持python2，大部分库可使用pip安装
### 1.支持使用pip安装的库
**numpy，scipy，matplotlib**
例子如：`pip install numpy`
### 2.其他库
**midi**
从[midi库的github地址](https://github.com/vishnubob/python-midi)下载该库源码，在对应文件夹下运行 `python setup.py install`

#### 至此，wav2mid所有环境配置完成

### 二. 使用说明
1. **配置文件**     
wav2mid.config,可在其中配置希望输出的mid的路径，例子：`./home/midFiles/`
2. **命令格式说明**    
运行的命令格式为`python wav2mid.py [wavFilePath] [tempo]`     
其中[wavFilePath] 是待处理的wav文件的路径名    
[tempo]是乐曲的节奏，可以没有，默认120     
例子：`python wav2mid.py ./home/wavFiles/sample.wav 120`
3. **输出文件说明**     
wav2mid会为输出的mid文件赋予一个唯一的uuid作为名称，并在生成结束后在终端print出一行mid文件的完整文件路径






