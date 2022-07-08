import time

fileObj = open('./run.log', 'a+', encoding='utf-8')
def printLog(msg):
	try:
		if type(msg) != str:
			msg = str(msg)
		msg = time.strftime('%Y-%m-%d %H:%M:%S') + ': ' + msg
		print(msg)
		fileObj.write(msg + '\n')
		fileObj.flush()
	except Exception as e:
		print(e)
