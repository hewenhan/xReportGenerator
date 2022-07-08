#!/usr/bin/python3

# pip3 install gitpython
from distutils.command.config import config
from libs.log import printLog
from git import Repo
import shutil, os, datetime, json

config = json.load(open('config/config.json', 'r'))

# 转换日期字符串为时间戳
def timestamp(date):
	return datetime.datetime.strptime(date, '%Y-%m-%d').timestamp()

# 输入一个git地址，输出仓库的名称
def getGitRepoName(gitUrl):
	return gitUrl.split('/')[-1].split('.')[0]

# 清空cache文件夹，如果cache文件夹不存在，则创建cache文件夹，如果cache文件夹存在，则清空cache文件夹
def clearCacheDir():
	printLog('clearing cache dir')
	if os.path.exists(config['output']) == False:
		os.mkdir(config['output'])
	if os.path.exists(config['cache']):
		shutil.rmtree(config['cache'])
	os.mkdir(config['cache'])
	printLog('clearing cache dir done')

# 允许用户输入一个git仓库地址和用户名称和日期范围，将仓库自动clone到本地，并切换遍历所有分支，读取提交记录，将提交记录中日期范围内的特定用户的提交记录打印出来。
def getGitCommitTextByUserDateRange(gitConfig):
	localCachePath = f'./{config["cache"]}/{getGitRepoName(gitConfig["url"])}'
	printLog('cloning git url: ' + gitConfig['url'])
	repo = Repo.clone_from(gitConfig['url'], localCachePath)
	printLog('clone done git url: ' + gitConfig['url'])
	return repo

# 根据时间范围读取全部远程分支地址
def getGitBranches(repo, repoName):
	result = []
	printLog(f'reading {repoName} branches')
	branches = repo.remotes.origin.refs
	for branch in branches:
		if branch.commit.committed_date < timestamp(config['afterDate']):
			continue
		result.append(branch.name)
	printLog(f'reading {repoName} branches done')
	return result

def getRemoteBranchNameByCommitFirstTime(commit):
	currentBranchList = commit.repo.git.branch('--sort=committerdate', '-a','--contains', commit.hexsha).split('\n')
	currentBranchList = list(map(lambda x: x.strip(), currentBranchList))
	currentBranchList = list(filter(lambda x: x.split('/')[0] == 'remotes', currentBranchList))
	currentBranchList = list(filter(lambda x: 'origin/HEAD' not in x, currentBranchList))
	return currentBranchList[0].replace('remotes/', '')

# 根据时间范围读取提交记录
def getGitCommitTextByDateRange(repo, branches, repoName = ''):
	printLog(f'reading {repoName} commits')
	result = ''

	commits = list(repo.iter_commits(branches, since=config['afterDate'], committer=config['committerName']))
	for commit in commits:
		result += f'{repoName} {getRemoteBranchNameByCommitFirstTime(commit)} {commit.message}'

	printLog(f'reading {repoName} commits done')

	return result

# 将 gitsCommitsText 插入文本模板中
def insertGitsCommitsTextIntoTemplate(gitsCommitsText):
	printLog('inserting gits commits text into template')
	template = open(f'template/{config["template"]}', 'r')
	templateText = template.read()
	template.close()
	templateText = templateText.replace('{{gitsCommitsText}}', gitsCommitsText)
	template = open(f'{config["output"]}/{config["template"]}', 'w')
	template.write(templateText)
	template.close()
	printLog('inserting gits commits text into template done')

def main():
	printLog('start')

	# 清缓存
	clearCacheDir()

	gitsCommitsText = ''
	# 遍历 config['gitUrls'] 下所有分支
	for gitConfig in config['gitUrls']:
		repo = getGitCommitTextByUserDateRange(gitConfig)
		branches = getGitBranches(repo, gitConfig['name'])
		commitsText = getGitCommitTextByDateRange(repo, branches, gitConfig['name'])
		gitsCommitsText += commitsText
		repo.close()
		shutil.rmtree(repo.working_tree_dir)

	# 将 gitsCommitsText 插入文本模板中
	insertGitsCommitsTextIntoTemplate(gitsCommitsText)

	printLog('end')
	printLog('')

main()
