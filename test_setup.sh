

# dependencies for TransSynW
python -m pip install --upgrade pip
pip install pytest
pip install -r requirements.txt
R -e 'install.packages(c("purrr","Rcpp","reshape2","RcisTarget"), repos = "http://cran.us.r-project.org")'
R -e 'install.packages("~/R/RcisTarget_1.0.2.tar.gz", repos=NULL)'

sudo apt install libboost-all-dev

export CPATH=$CPATH:'/opt/homebrew/include'
export LIBRARY_PATH=$LIBRARY_PATH:'/opt/homebrew/lib/'

cd ./data
curl -O https://resources.aertslab.org/cistarget/databases/old/homo_sapiens/hg19/refseq_r45/mc9nr/gene_based/ 
cd ..

mkdir ./craft/dependencies
cd ./craft/dependencies
touch __init__.py
git clone --depth=1 https://gitlab.lcsb.uni.lu/CBG/transsynw.git transsynw

# dependencies for Signet
wget https://github.com/Lan-lab/SIGNET/raw/main/SIGNET_Tutorial/SIGNET.py -O SIGNET.py

cd -

# if the user wants to download the latest data from TRRUST database
# # curl -s 'https://www.grnpedia.org/trrust/data/trrust_rawdata.human.tsv' >> trrust_rawdata_human.tsv
# echo "Setup completed"