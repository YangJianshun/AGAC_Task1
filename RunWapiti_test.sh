Wapiti=/public/home/yangjs/test/CRF_test/Wapiti/bin/wapiti
Pattern_File=test.pat
Training_Options=' -a sgd-l1 -t 4 -i 15 '

mkdir -p output
echo "================ Training (this may take some time) ================" 1>&2
# training: create a MODEL based on PATTERNS and TRAINING-CORPUS
# wapiti train -p PATTERNS TRAINING-CORPUS MODEL
echo "wapiti train $training_options -p $pattern_file <(cat AGAC_training_tab/*.tab) output/train.mod" 1>&2
$Wapiti train $Training_Options -p $Pattern_File <(cat AGAC_training_tab/*.tab) output/train.mod
# wapiti train -a bcd -t 2 -i 5 -p t.pat train-bio.tab t-train-bio.mod
#
# Note: The default algorithm, l-bfgs, stops early and does not succeed in annotating any token (all O)
# sgd-l1 works; bcd works

# To examine the contents of the model, first dump it into a text file then use 'less FILE' to view its contents
$Wapiti dump output/train.mod output/train.txt

echo "================ Inference  ================" 1>&2
# inference (labeling): apply the MODEL to label the TEST-CORPUS, put results in TEST-RESULTS
# wapiti label -m MODEL TEST-CORPUS TEST-RESULTS
# -c : check (= evaluate)
# <(COMMAND ARGUMENTS ...) : runs COMMAND on ARGUMENTS ... and provides the results as if in a file
echo "wapiti label -c -m output/train.mod <(cat AGAC_sample_tab/*.tab) output/train-test.tab" 1>&2
$Wapiti label -c -m output/train.mod <(cat AGAC_sample_tab/*.tab) output/train-test.tab
# wapiti label -c -m t-train-bio.mod test-bio.tab t-train-test-bio.tab
