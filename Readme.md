## Getting started
### Install the environment
1. Connect to the agrinet remote server with your credentials
2. Clone the repository ```git clone https://github.com/simonlousky/model-leaf.git leafsegmentor```
3. Enter the directory with `cd leafsegmentor`
4. Run setup `bash setup.sh` and follow the miniconda install instructions with default values
    * This may take a while, go make yourself a coffee
  
The install will create a directory leafsegmentor. All relative paths should be from this directory.

#### Troubleshooting

* In case it didn't finish or you lost connection - do step 4 again
The setup should add an alias leafsegmentor for "python LeafSegmentor.py" so after setup you only need to 
enter the leafsegmentor directory to start working!
* If your session doesn't start with bash as the default shell (run ```echo $0``` to check that)
then you will need to run ```. ~/.bash_profile``` at the beginning of each session

### Using the command

1. Go to the leafsegmentor directory
2. Run `leafsegmentor --help`
You should see the command help doc.
For further info continue reading here or refer to the `--help` of every sub command

### Command examples

#### Training example with pre-cut banana leaves

```bash
leafsegmentor train dataset_config.json
```

Train a new model from scratch (From COCO) using the dataset configuration in `dataset_config.json`
The content of the configuration file is explained in the train manual (furthur down)

#### Inference and compare with ground truth

```bash
leafsegmentor infer -m ../models/banana_LS2_2019_11_18.h5 --gt AgrinetAdapter --task 129 ../GT_images_jsons
```

This example runs inference on the pictures of dataset task id 129 (pre-downloaded to directory GT_images_jsons) and also compares the result to the ground truth.

`-m ../models/banana_LS2_2019_11_18.h5` - Specifies a previously trained model

`--gt AgrinetAdapter` - Specifies that the json files in the inference directory are in the format parsed by the AgrinetAdapter class.

`--task 120` - a required argument by 

`AgrinetAdapter` to correctly parse the .json files.

### Cut leaves

```bash
cut -a CocoAdapter -o ../cut_leaves ../cut_jobs/cucumber/annotations.json
```

## A to Z work flow

Description of the training concept (BG and leaves etc...)

### Download training task
Downloading training tasks in the remote server is fairly simple.
They are located at `/mnt/gluster/catalog/experiment_<NO>/task_<NO>/plot_<NO>`
Preferably download to a simple relative path from `leafsegmentor` directory

### Cut leaves

Cut the leaves of the required dataset using the correct adapter, to a new directory you will use as your bank of leaves.

#### Customize leaf cutting

You may want to...

### Train model
1. bla
2. bla
#### Customize training and config
#### Work with difference datasets

### Infer with model

# leafsegmentor Manual page

## Name

leafsegmentor - the leaf model simple interface

## Synopsis

```leafsegmentor [--version]  [--help] <command> [<args>]```

## Description

leafsegmentor uses the Tensorflow implementation of Mask-RCNN by MatterPort and a handful of integration scripts and utilities to simplify training and inference of leaf datasets.

For information on the different subcommands read the according manual pages

## Options

###### -h

###### --help

Prints the synopsis and the list of possible options and commands.

###### -v

###### --version

Prints the leaf-model command line version

## Subcommands

###### [leafsegmentor-train](#bookmark=kix.d73ecqfzwil1)

Train a model from a dataset

###### [leafsegmentor-infer](#bookmark=id.omgzqarzcj72)

Run inference on a directory of pictures, using a pretrained model

###### [leafsegmentor-cut](#bookmark=id.t0gg9bnl4kan)

Cut leaves from annotated data

###### [leafsegmentor-info](#bookmark=kix.icual4pnf7xg)

Print model metadata

# leafsegmentor-train Manual Page

## Name

leafsegmentor-train - train a model for leaves

## Synopsis

```leafsegmentor train [-h] [-o <path> | --output=<path>] [-k <value> | --dataset-keep=<value>] [--preview-only] [-e <epochs> | --epochs <epochs>] [-s | --steps-per-epoch] [-l | --layers (all | heads | 3+ | 4+ | 5+)] [-p <pretrained> | --pretrain <pretrained>] <datasetconfigfile>```

## Description

Creates a dataset of synthetic pictures, and runs the training model on the dataset. The result models are saved as .h5 files.

## Positional argument

*\<datasetconfigfile\>*
This is the json file specifying the configuration of the training datatset. 

config example:

```json
{
    "dataset_module": "LeafDataset",
    "dataset_class": "LeafDataset",
    "config": {
        "train":{
            "folder_objects": "../datasets/examples/banana/train_leaves",
            "folder_bgs": "../datasets/examples/banana/train_backgrounds",
            "min_leaf": 4,
            "max_leaf": 10,
            "min_plants": 1,
            "max_plants": 1,
            "leaf_angle_offset": 70,
            "leaf_position_offset": 64,
            "min_scale": 0.5,
            "max_scale": 1.5,
            "image_size": 512,
            "number_of_images": 200,
            "centered_leaves": true
        },
        "valid":{
            "folder_objects": "../datasets/examples/banana/train_leaves",
            "folder_bgs": "../datasets/examples/banana/train_backgrounds",
            "min_leaf": 4,
            "max_leaf": 10,
            "min_plants": 1,
            "max_plants": 1,
            "leaf_angle_offset": 70,
            "leaf_position_offset": 64,
            "min_scale": 0.5,
            "max_scale": 1.5,
            "image_size": 512,
            "number_of_images": 200,
            "centered_leaves": true
        }
    }
}
```

`dataset_module` - The python module containing the dataset class.
`dataset_class` - The dataset Class. This class should inherit the `utils.Dataset` and implement the class method: `from_config(cls, config_dict, width, height)` - take a look at `LeafDataset.py`.

The idea is that the configuration is binded to the implementation of the `from_config` methdo. This way you can implement your own dataset and continue using the command line.

## Options

###### -o <path>

###### --output=<path>

specify path to .h5 model location [default: models]

###### -k <value>

######  --dataset-keep=<value>	

specify how many samples to keep (default 0)

###### --preview-only=<number>

generate samples of training set without training the model

###### -e <epochs>

###### --epochs <epochs>

number of training epochs

###### -s <steps> 

###### --steps-per-epoch <steps>

number of training steps to perform per epoch

###### -l <{all, heads, 3+, 4+, 5+}>

###### --layers <{all, heads, 3+, 4+, 5+}>

layers of model to train. Other layers will remain unchanged

######  -p \<pretrained>

###### --pretrain \<pretrained>

path to a .h5 file with a pretrained model, or just 'COCO' to retrieve the coco pretrain file. [default: COCO]

# leafsegmentor-infer Manual page

## Name

leafsegmentor-infer - leaf inference command

## Synopsis

```leafsegmentor infer [-h] [-m <model> | --model <model>] [-o <path> | --output <path>]  [--no-pictures] [--no-contours] [--no-masks] [--gt=<adapterClass>] [--task=<task_id>] <picturespath>```

## Description

Loads a model and runs inference on all the pictures located in a directory, or just on a picture. 

Output is:

1. A set of pictures with a translucent mask on every detected leaf
2. A set of mask pictures
3. A contour annotation file in json format and a list of numpy exportet txt files of the contours
4. If ground truth is specified (`--gt`) then also the mask of the ground truth is drawn in the output directory

## Positional argument

*\<picturespath\>*
The path to a directory containing pictures. The command will iterate over all the pictures and generate the mask files, and the contour txt files.

## Options

###### -m <model> 

###### --model <model>

path to .h5 trained model to infer with

###### -o <path>

###### --output=<path>

Set output directory [default: current]

###### --no-pictures

Doesn’t output the translucent pictures

###### --no-contours

Doesn’t output the contour file

###### --no-masks

Doesn’t output the mask pictures

###### --gt <adapter>

Specify the Name of the module and adapter class. 
The adapter class is supposed to parse some dataset format, and provide the polygons in a generic format.

See `BaseAnnotationAdapter` module for more details.

###### --task <taskid>

Special argument for the agrinet datasets which require to know the relevant task_id

# leafsegmentor-cut Manual page

## Name

leafsegmentor-cut - single leaf extractor


## Synopsis

```leafsegmentor cut [-h] [-o <path> | --output <path>] [-l <limit> | --limit <limit>] [-n <width>| --normalize=<width>] [-b | --background=(black | white | original, transparent)] [-a <adapter> | --adapter=<adapter>] [-r | --rotate] <jsonpath>```

## Description

Cut single leaf pictures from an annotated dataset. This step is intended to extract single leaves from annotated datasets, and then use these leaves to train a model. This can also be used to cut leaves from files that went through inference, in order to use the single leaves in other processes.

## Positional argument

*\<jsonpath\>*
A path to a directory or a json file that holds the dataset you want to cut to single leaves. The format of the json should be binded to the adapter class you specify.

## Options

###### -o <path>

###### --output=<path>

Set output directory [default: current]

###### -l <number>

###### --limit=<number>

Maximum number of object files to create. Not specifying this argument will result in cutting all the available objects

###### -n <width-size>

###### --normalize=<width-size>

Normalize the generated pictures to the specified width-size. By default pictures are not normalized, every leaf stays at its original size

###### -b ( black | white | original | transparent)

###### --background=( black | white | original | transparent )

Specify the background of the leaf, if a color or original is selected, the object won’t have an alpha layer [default: transparent]

###### -a <adapter>

###### --adapter <adapter>

Specify the Name of the module and adapter class. 
The adapter class is supposed to parse some dataset format, and provide the polygons in a generic format.

See `BaseAnnotationAdapter` module for more details.

###### -r

###### --rotate

Rotate output leaves to match 2 points from annotation
This works only if the adapter inherits from the `RotatableAdapter` class. See the docstring of the function `get_point` for mor details.

# leafsegmentor-info Manual page

## Name

leafsegmentor-info - model metadata extractor

## Synopsis

```leafsegmentor info <modelpath>```

## Description

Prints information about the model saved in the model-info variable

## Options

None
