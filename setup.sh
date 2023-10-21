ENV_NAME=leafsegmentor
CONDA_INSTALL_NAME=miniconda_install.sh

# Install conda if not installed
if [[ ! $(command -v conda) ]]; then

  if [[ ! -f ~/$CONDA_INSTALL_NAME ]]; then
    curl -o ~/$CONDA_INSTALL_NAME https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
  fi

  # Add conda to bash profile
  cd ~
  bash $CONDA_INSTALL_NAME
  echo ". ~/.bashrc" >> ~/.bash_profile
  . ~/.bash_profile
fi

# Create leafsegmentor conda environment
if [[ "$(conda env list | grep $ENV_NAME | awk '{print $1}')" != $ENV_NAME ]] ; then
  conda env create --name $ENV_NAME -v -f environment.yml;
  echo "alias leafsegmentor='conda deactivate && conda activate $ENV_NAME && srun python LeafSegmentor.py'" >> ~/.bash_profile
  . ~/.bash_profile
fi
