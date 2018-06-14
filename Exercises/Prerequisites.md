# Software Prerequisites

[Git](https://git-scm.com)

* clone the repo in a local folder

```
git clone https://github.com/LSIR/DIS2018.git
```

[Python 3.X](https://www.python.org/)

[Anaconda](https://www.anaconda.com/download/) or [Miniconda](https://conda.io/miniconda.html)

* install conda libraries
```
conda install -y scipy pandas numpy networkx nltk matplotlib jupyter
```

* download nltk packages
```
python -m nltk.downloader stopwords punkt #-d /path/to/nltk_data
```

* create a new environment 

```
conda create -n dis2018 python=3.5 scipy pandas numpy networkx nltk matplotlib jupyter
```

* activate it
	
```
source activate dis2018
```


Run a notebook server (be sure to be at the repo's folder; a browser window should open up for you)

```
jupyter notebook
```

