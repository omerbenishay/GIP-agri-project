## Getting started
### Install the environment
1. Connect to the agrinet remote server with your credentials
2. Clone the repository ```git clone https://github.com/simonlousky/model-leaf.git leafsegmentor```
3. Enter the directory with `cd leafsegmentor`
4. Run setup `bash setup.sh` and follow the miniconda install instructions with default values
* In case it didn't finish or you lost connection - do step 4 again
The setup should add an alias leafsegmentor for "python LeafSegmentor.py" so after setup you only need to 
enter the leafsegmentor directory to start working!

### Using the command

1. Go to the leafsegmentor directory
2. Run `leafsegmentor --help` 
You should see the command help doc.
For further info continue reading here or refer to the `--help` of every sub command 
 
### Command examples
#### Example 1

```
bla bla
```
#### Example 2
```
bla bla
```
## A to Z work flow
Description of the training concept (BG and leaves etc...)
### Download training task
1. bla
2. bla
### Cut leaves
1. bla
2. bla
#### Customize leaf cutting
1. bla
2. bla
### Train model
1. bla
2. bla
#### Customize training and config
#### Work with difference datasets

### Infer with model


<!----- Conversion time: 0.945 seconds.


Using this Markdown file:

1. Cut and paste this output into your source file.
2. See the notes and action items below regarding this conversion run.
3. Check the rendered output (headings, lists, code blocks, tables) for proper
   formatting and use a linkchecker before you publish this page.

Conversion notes:

* Docs to Markdown version 1.0β18
* Sat Mar 07 2020 14:10:08 GMT-0800 (PST)
* Source doc: https://docs.google.com/open?id=1uvhRShosFWqySOQqXwItVI6SNPeA_l2XltMpL98kqxY
----->



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


# 


# leafsegmentor-train Manual Page


## Name

leafsegmentor-train - train a model for leaves


## Synopsis

```leafsegmentor train [-h] [-o <path> | --output=<path>] [-k <value> | --dataset-keep=<value>]  [-t <path> | --test-set=<path>] [-d <datasetclass> | --dataset-class <datasetclass>] [--preview-only] [-e <epochs> | --epochs <epochs>] [-s | --steps-per-epoch] [-l | --layers (all | heads | 3+ | 4+ | 5+)] [-p <pretrained> | --pretrain <pretrained>] <datasetconfigfile>```


## Notes

<datasetpath> Should be the path to a json annotation file with valid relative paths to the images.

<bg-path> Path to a directory containing the synthetic backgrounds.


## Description

Creates a dataset of synthetic pictures, and runs the training model on the dataset. The best result model is saved as a .h5 file. 


## Positional argument


###### <datasetconfigfile>


## Options


###### -o <path>


###### --output=<path>			

specify path to .h5 model location [default: current]


###### -t <path>


###### --test-set=<path>	

specify path to test set 


###### -k <value>


######  --dataset-keep=<value>	

specify how many samples to keep (default 0)


###### -d <datasetclass> 


###### --dataset-class <datasetclass>

dataset module and class name to use [eg:  'BananaDataset']


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


######  -p <pretrained>


###### --pretrain <pretrained> 

path to a .h5 file with a pretrained model, or just 'COCO' to retrieve the coco pretrain file. 

[default: COCO]


# leafsegmentor-infer Manual page


## Name

leafsegmentor-infer - leaf inference command


## Synopsis

```leafsegmentor infer [-h] [-m <model> | --model <model>] [-o <path> | --output=<path>]  [--no-pictures] [--no-contours] [--no-masks] <picturespath>```


## Description

Loads a model and runs inference on all the pictures located in a directory, or just on a picture. 

Output is:



1. A set of pictures with a translucent mask on every detected leaf
2. A set of mask pictures
3. A contour annotation file


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


# leafsegmentor-cut Manual page


## Name

leafsegmentor-cut - single leaf extractor


## Synopsis

```leafsegmentor cut [-h] [-o <path> | --output <path>] [-l <limit> | --limit <limit>] [-n <width>| --normalize=<width>] [-b | --background=(black | white | original, transparent)] [-a (banana | cucumber | maize) | --adapter] [-r | --rotate] <jsonpath>```


## Description

Cut single leaf pictures from an annotated dataset


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


###### -a (banana | cucumber | maize)


###### --adapter (banana | cucumber | maize)

Type of annotation file used - specify in order to correctly parse the contour file


###### -r 


###### --rotate

Rotate output files to match 2 points from annotation


# leafsegmentor-info Manual page


## Name

leafsegmentor-info - model metadata extractor


## Synopsis

```leafsegmentor info <modelpath>```


## Description

Prints information about the model saved in the model-info variable


## Options

None


<!-- Docs to Markdown version 1.0β18 -->
