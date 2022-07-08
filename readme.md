
X报生成器
====

`Blind Holmes`
`v1.0.0`

> Written with [StackEdit](https://stackedit.hewenhan.me/).

## 简介

程序员在日常工作中，往往公司有要求编写日报周报或者月报。然而众所周知，程序员都讨厌编写文档。
所以我想要做一个 `X报生成器` 来减轻程序员的日常工作。主要功能的构思是，通过拉取程序员开发的 GIT 仓库，将周期内的特定用户的提交记录提取出来，塞到周报模板里。这是我这个 `X报生成器` 想要做到的功能。

## 使用说明

### 安装依赖
```
pip3 install gitpython
```

### 创建配置文件

在 `config` 文件夹下创建 `config.json` 文件
在 `template` 文件夹下创建模板文件，并配置文件名写进 `config.json` 文件中
配置文件格式

```
{
	"cache": "cache", // 缓存文件路径
	"output": "output", // 周报文件输出文件路径
	"committerName": ["limaoquan"], // 提交者名称
	"afterDate": "2022-07-01", // 拉取该日期之后的提交记录
	"gitUrls": [{
		"url": "ssh://git@git.sf-pharma.com:51122/static/sf-integrated-platform-admin.git", // git仓库地址
		"name": "运营端" // 仓库别名
	}],
	"template": "weekReport.txt" // 周报模板文件名
}
```

### 运行
```
python3 run.py
```

运行完成，会在 output 的文件夹下生成周报文件