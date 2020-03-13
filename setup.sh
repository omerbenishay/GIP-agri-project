if [[ $(echo `conda env list | grep model-cmd | awk '{print $1}'`) != "model-cmd" ]] ; then
  conda env create -f environment.yml;
  conda init
fi

echo "alias leaf-segmentor='conda activate model-cmd && python LeafSegmentor.py'" >> ~/.bash_profile
echo "alias leaf-segmentor='conda activate model-cmd && python LeafSegmentor.py'" >> ~/.bashrc

. ~/.bash_profile
. ~/.bashrc