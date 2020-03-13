
ENV_NAME=leafsegmentor

if [[ $(echo `conda env list | grep $ENV_NAME | awk '{print $1}'`) != $ENV_NAME ]] ; then
  conda env create --name $ENV_NAME -f environment.yml;
  conda init
fi

echo "alias leaf-segmentor='conda activate $ENV_NAME && python LeafSegmentor.py'" >> ~/.bash_profile

. ~/.bash_profile

if [[ ! -d ../models ]] then
  cp -r /mnt/gluster/shares/WP2_Analysis/WP2_models/Kimmel/LeafSegmentor_data/models ..
fi

if [[ ! -d ../cut_jobs ]] then
  cp -r /mnt/gluster/shares/WP2_Analysis/WP2_models/Kimmel/LeafSegmentor_data/cut_jobs ..
fi