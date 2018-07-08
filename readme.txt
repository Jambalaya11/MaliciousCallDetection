commiucateType: 分为cvoi,local,diatance
callingArea:通话地点
calledArea:对方地点
planName:产品名
custCode:客户标识
userType:用户类别
sellProduct:销售产品
以上为文字或字符,被编码为数字

callType:1.主叫 2.被叫
talkType:共10种 1.本地 2.漫游国内 3.漫游港澳台 4.漫游国际 5.漫游本地通话 6.国内长途 7.国际长途 8.港澳台长途 9.多方本地通话 10.多方通话国内长途
cost:费用
isRealName: 是否实名 0:否 1:是
useTime：本号码从开通至今使用时间
meanCallTime: 平均通话时间
stdCallTime: 通话时间均方差
isRestDay: 是否为休息日(周末和假期) 是：1 否：0
isWorkTime: 是否为工作时间(8:00-18:00) 是：1 否：0
label :0为普通号码 1为恶意号码



文件介绍：
benignCall.csv 普通号码
maliciousCall.csv 恶意号码
bill.csv 通话记录
ori_label.csv 处理前的特征文件
encoded_label.csv 特征提取及编码后的文件
deal_with_data.py 处理文件


