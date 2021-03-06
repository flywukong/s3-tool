# S3工具


## 1. 删除工具


### 1.1 基本参数

-H  后面加主机名  如果是IP需要在前面加上http   例如 http://172.21.212.250 
-a  后面加access_key  例如YTU004W0Z1A585KIRSO6 
-s  后面加secret_key  例如JlNVoLfLuJJRbKBiFoyb2joRyuRXqNpIV1tRDHZP

### 1.2 工具分类

(1) 删除单个bucket
该功能对应的脚本为thread-delete-bucket.py , 使用时指定 -b参数 后面加bucket名称
```
[wuchen@manager delete]$ python thread-delete-bucket.py -H http://172.21.212.250 -a YTU004W0Z1A585KIRSO6  -s JlNVoLfLuJJRbKBiFoyb2joRyuRXqNpIV1tRDHZP   -b test7
['test1', 'test2', 'test7']
[{'Key': u'osd.84.log'}] 1

```


(2)删除bucket列表
该功能对应的脚本为thread-delete-buckets.py ,
 使用前需要将bucket 列表每行一个bucket 名称写入一个配置文件中，该功能对应的脚本为thread-delete-buckets.py , 使用时指定 -f参数 后面加配置文件的路径（包括配置文件名）

```
[wuchen@manager delete]$ cat bucket.txt 
test10
test3
test4
test5
test6
test7
test8
test9
[wuchen@manager delete]$ python thread-delete-buckets.py -H http://172.21.212.250 -a YTU004W0Z1A585KIRSO6  -s JlNVoLfLuJJRbKBiFoyb2joRyuRXqNpIV1tRDHZP   -f /home/wuchen/wuchen/delete/bucket.txt 
deleting test10
[{'Key': u'osd.84.log'}] 1
deleting test3
[{'Key': u'osd.84.log'}] 1
deleting test4
[{'Key': u'osd.84.log'}] 1
deleting test5
[{'Key': u'osd.84.log'}] 1
deleting test6
[{'Key': u'osd.84.log'}] 1
deleting test7
[{'Key': u'osd.84.log'}] 1
deleting test8
[{'Key': u'osd.84.log'}] 1
deleting test9
[{'Key': u'osd.84.log'}] 1

```


(3) 删除某个用户所有bucket
该功能对应的脚本为thread-delete-user.py ,只需要基本的3个参数，删除该用户所有的bucket
```
[wuchen@manager delete]$ python thread-delete-user.py -H http://172.21.212.250 -a YTU004W0Z1A585KIRSO6  -s JlNVoLfLuJJRbKBiFoyb2joRyuRXqNpIV1tRDHZP 
```

## 2. 下载工具

### 2.1 基本参数

#### 2.1.1  下载文件
使用脚本thread-download.py 分片多线程下载大文件(大于8M),  如果是小于8M 小文件下载 只需要指定-t 参数为0

(1) 必写参数
-H  主机地址  如果写IP的话 前面不需要加http 例如172.21.212.250 
-a  用户的access_key  例如YTU004W0Z1A585KIRSO6  
-s  用户的secret_key  例如JlNVoLfLuJJRbKBiFoyb2joRyuRXqNpIV1tRDHZP  
-b  要下载对象所在桶名称   例如test12
-o  要下载对象的对象名  例如python.tar.gz 如果是包含多层文件夹目录，需要写上完整的路径 
-f   下载对象写入本地的文件路径  例如/home/wuchen/wuchen/download/download-file 

(2) 可选参数
 -t  指定线程数 默认是10个线程   
 -c 指定分片大小为多少M , 默认是8M

#### 2.1.2  下载目录
使用脚本download-folder.py 下载bucket中的某个文件夹到 中，该功能会递归下载目录中的所有子目录

参数解析如下：
-H  主机地址  如果写IP的话 前面不需要加http 例如172.21.212.250 
-a  用户的access_key  例如YTU004W0Z1A585KIRSO6  
-s  用户的secret_key  例如JlNVoLfLuJJRbKBiFoyb2joRyuRXqNpIV1tRDHZP  
-b  要下载目录所在桶名称  
-f  下载目录数据存放在本地的路径位置
-p  要下载的s3目录，如果是多层级的目录需要给出完整的路径，例如bucket下面有目录 test1 , test1有目录test2， 要下载test1, 则 -p后加test1 ,要下载test2, -p 后加test1/test2 

### 2.2 使用示例

#### 2.2.1 下载文件使用
使用默认参数下载
```
[wuchen@manager download]$ python thread-download.py  -H  172.21.212.250 -a YTU004W0Z1A585KIRSO6  -s JlNVoLfLuJJRbKBiFoyb2joRyuRXqNpIV1tRDHZP  -b test12 -o  python.tar.gz -f /home/wuchen/wuchen/download/download-file  
```

使用15个线程下载，分片默认
```
[wuchen@manager download]$ python thread-download.py  -H  172.21.212.250 -a YTU004W0Z1A585KIRSO6  -s JlNVoLfLuJJRbKBiFoyb2joRyuRXqNpIV1tRDHZP  -b test12 -o  python.tar.gz -f /home/wuchen/wuchen/download/download-file   -t 20
```

使用20个线程下载，分片为20M
```
[wuchen@manager download]$ python thread-download.py  -H  172.21.212.250 -a YTU004W0Z1A585KIRSO6  -s JlNVoLfLuJJRbKBiFoyb2joRyuRXqNpIV1tRDHZP  -b test12 -o  python.tar.gz -f /home/wuchen/wuchen/download/download-file   -t 20 -c 20

```

下载单个小文件
```
wuchen@manager download]$ python thread-download.py  -H  172.21.212.250 -a YTU004W0Z1A585KIRSO6  -s JlNVoLfLuJJRbKBiFoyb2joRyuRXqNpIV1tRDHZP  -b test12 -o  python.tar.gz -f /home/wuchen/wuchen/download/download-file   -t  0
```

#### 2.2.1 下载目录使用
```
[wuchen@manager download]$ python download-folder.py -H  http://172.21.212.250 -a YTU004W0Z1A585KIRSO6  -s JlNVoLfLuJJRbKBiFoyb2joRyuRXqNpIV1tRDHZP -f /home/wuchen/wuchen/s3-tool/download/result22  -p werfefdsa/dffds -b test12
```
该命令执行后，本地result22目录会下载bucket 名称为test12中的 werfefdsa/dffds
```
[wuchen@manager download]$ python download-folder.py -H  http://172.21.212.250 -a YTU004W0Z1A585KIRSO6  -s JlNVoLfLuJJRbKBiFoyb2joRyuRXqNpIV1tRDHZP -f /home/wuchen/wuchen/s3-tool/download/result22  -p werfefdsa -b test12
```
该命令执行后，本地result22目录会下载bucket 名称为test12中的 werfefdsa/

## 3. 上传工具

### 3.1 参数

#### 3.1.1 上传文件参数
使用脚本thread-upload.py 分片多线程上传大文件(大于8M), 默认会按照8M 切片 10线程上传， 如果是小于8M 小文件上传只需要指定-t 参数为0

(1) 必写参数
-H  主机地址  如果写IP的话 前面不需要加http 例如172.21.212.250 
-a  用户的access_key  例如YTU004W0Z1A585KIRSO6  
-s  用户的secret_key  例如JlNVoLfLuJJRbKBiFoyb2joRyuRXqNpIV1tRDHZP  
-b  要上传对象所在桶名称   例如test12
-o  要上传对象的对象名 
-f   上传对象在本地的文件路径  例如/home/wuchen/wuchen/download/download-file 

(2) 可选参数
 -t  指定线程数 默认是10个线程   
 -c 指定分片大小为多少M , 默认是8M

#### 3.1.2 上传目录参数
使用脚本upload-folder.py  , 递归上传本地指定路径的文件夹 到bucket下，可以直接上传到bucket下，也可以上传到bucket下面的某个目录路径下
参数解析如下：
-H  主机地址  如果写IP的话 前面不需要加http 例如172.21.212.250 
-a  用户的access_key  例如YTU004W0Z1A585KIRSO6  
-s  用户的secret_key  例如JlNVoLfLuJJRbKBiFoyb2joRyuRXqNpIV1tRDHZP  
-b  要上传的目录所在桶名称  
-l  上传目录存放在本地的路径位置
-d  递归上传本地指定路径的文件夹到bucket下面的路径位置，如果直接上传到bucket下，则指定 -d root， 如果上传到bucket 下面的某个目录路径，则给出完整路径，例如上传到bucket下面的test1目录下的子目录test2 下，则指定-d   test1/test2



### 3.2 使用示例

#### 3.2.1 上传文件使用示例

使用默认参数上传
```
python thread-upload.py  -H  172.21.212.250 -a YTU004W0Z1A585KIRSO6  -s JlNVoLfLuJJRbKBiFoyb2joRyuRXqNpIV1tRDHZP  -b test12 -o jar -f /home/wuchen/wuchen/upload/iflyek_url_tesy-1.0.1.100247.jar
```

使用15个线程下载，分片默认
```
python thread-upload.py  -H  172.21.212.250 -a YTU004W0Z1A585KIRSO6  -s JlNVoLfLuJJRbKBiFoyb2joRyuRXqNpIV1tRDHZP  -b test12 -o jar -f /home/wuchen/wuchen/upload/iflyek_url_tesy-1.0.1.100247.jar -t 15
```

使用20个线程上传，分片为20M
```
python thread-upload.py  -H  172.21.212.250 -a YTU004W0Z1A585KIRSO6  -s JlNVoLfLuJJRbKBiFoyb2joRyuRXqNpIV1tRDHZP  -b test12 -o jar -f /home/wuchen/wuchen/upload/iflyek_url_tesy-1.0.1.100247.jar -t 20 -c 20
```

上传单个小文件
```
python thread-upload.py  -H  172.21.212.250 -a YTU004W0Z1A585KIRSO6  -s JlNVoLfLuJJRbKBiFoyb2joRyuRXqNpIV1tRDHZP  -b test12 -o jar -f /home/wuchen/wuchen/upload/iflyek_url_tesy-1.0.1.100247.jar -t 0
```
#### 3.2.2 上传目录使用示例
将本地目录 直接上传到bucket test12下面
```
[wuchen@manager upload]$   python upload-folder.py  -H http://172.21.212.250 -a YTU004W0Z1A585KIRSO6  -s JlNVoLfLuJJRbKBiFoyb2joRyuRXqNpIV1tRDHZP   -b test12 -l /home/wuchen/wuchen/s3-tool/upload/download  -d  root

```
将本地目录 上传到bucket test12下面的werfefdsa目录下

```
[wuchen@manager upload]$   python upload-folder.py  -H http://172.21.212.250 -a YTU004W0Z1A585KIRSO6  -s JlNVoLfLuJJRbKBiFoyb2joRyuRXqNpIV1tRDHZP   -b test12 -l /home/wuchen/wuchen/s3-tool/upload/download  -d  werfefdsa
```