# 生物文本挖掘课程作业
通过Wapiti实现的AGAC Task1，命名实体识别
## 环境配置
1.需要python3环境
2.需要安装Wapiti软件，并在RunWapiti_dev.sh和RunWapiti_test.sh中修改软件路径
## 数据描述
AGAC_sample/目录中包含50个测试数据，格式为json
AGAC_training/目录中包含250个训练数据，格式为json
## 数据处理
在训练模型和测试前均需要对数据进行预处理，运行脚本json2tab.py将训练数据和测试数据转换为“.tab”格式
python json2tab.py AGAC_training AGAC_training_tab
python json2tab.py -NoTriggerWords AGAC_sample AGAC_sample_tab
## 模型训练
将训练数据按7:3划分，在训练模型过程中7份用作实际训练模型，3份用作开发集，调整参数。当模型最优化后用该参数训练所有10份数据，并对测试数据进行预测。
1.调整参数模型优化
mkdir AGAC_training_tab_part1 && ls -l  AGAC_training_tab/ | awk '{if($9!="")print "cp AGAC_training_tab/"$9 " AGAC_training_tab_part1"}' | head -n 175 | sh
mkdir AGAC_training_tab_part2 && ls -l  AGAC_training_tab/ | awk '{if($9!="")print "cp AGAC_training_tab/"$9 " AGAC_training_tab_part2"}' | tail -n 75 | sh
bash RunWapiti_dev.sh
2.预测测试数据
bash RunWapiti_test.sh
## 结果数据格式转化
运行脚本将预测得到的“.tab”格式文件转化为json格式，保存在AGAC_sample_result/目录中
python tab2json.py output/train-test.tab AGAC_sample_result
