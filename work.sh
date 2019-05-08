python json2tab.py AGAC_training AGAC_training_tab
python json2tab.py -NoTriggerWords AGAC_sample AGAC_sample_tab
mkdir AGAC_training_tab_part1 && ls -l  AGAC_training_tab/ | awk '{if($9!="")print "cp AGAC_training_tab/"$9 " AGAC_training_tab_part1"}' | head -n 175 | sh
mkdir AGAC_training_tab_part2 && ls -l  AGAC_training_tab/ | awk '{if($9!="")print "cp AGAC_training_tab/"$9 " AGAC_training_tab_part2"}' | tail -n 75 | sh
bash RunWapiti_dev.sh
bash RunWapiti_test.sh
python tab2json.py output/train-test.tab AGAC_sample_result
