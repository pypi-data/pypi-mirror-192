<div align="center">
  <img src="https://github.com/RainelDias88/packagePYPI/blob/6a9709f6baaa6ce0051cd0e37ac8a35737fb923d/file/logoraineldataia.png"><br>
</div>

-----------------

# rainel: powerful data science and artificial intelligence toolkit
[![PyPI Latest Release](https://img.shields.io/pypi/v/rainel?style=plastic)](https://pypi.org/project/rainel/)
[![Package Status](https://img.shields.io/pypi/status/rainel?style=plastic)](https://pypi.org/project/rainel/)
[![License](https://img.shields.io/pypi/l/rainel?style=plastic)](https://github.com/RainelDias88/packagePYPI/blob/main/rainel/license.t)
[![Downloads](https://static.pepy.tech/badge/rainel/month)](https://pepy.tech/project/rainel)

## What is it?

**rainel** is a Python package that provides useful tools for Data Science and Artificial Intelligence.

## Where to get it
The source code is currently hosted on GitHub at:
https://github.com/RainelDias88/packagePYPI

Binary installers for the latest released version are available at the [Python
Package Index (PyPI)](https://pypi.org/project/rainel/).

```sh
# PyPI
pip install rainel
```

-----------------

```sh
class rainel.Gaussian(mu=0, sigma=1)
```
Gaussian distribution class for calculating and visualizing a Gaussian distribution.

```sh
        Parameters: 
            mu:  The mean value of the distribution
            sigma: Standard deviation of the distribution
            
        Attributes:
            mean: mu
            stdev: sigma
            data: list of floats extracted from the data file

        Methods:
            read_data_file(file_name)	Read in data from a txt file. The txt file should have one number (float) per line. The numbers are stored in the data attribute.

            calculate_mean()    Return mean of the data set.

            calculate_stdev(sample=True)	Return standard deviation of the data set. sample (bool): whether the data represents a sample or population.

            plot_histogram()    Output a histogram of the instance variable data using matplotlib pyplot library.

            pdf(x)  Return probability density function output. x (float): point for calculating the probability density function.

            plot_histogram_pdf(n_spaces=50) Return x and y values for the pdf

```

-----------------

```sh
class rainel.Binomial(prob=.5, size=20)
```
Binomial distribution class for calculating and visualizing a Binomial distribution.

```sh
        Parameters: 
            prob:  representing the probability of an event occurring

            size: number of trials
            
        Attributes:
            p: prob
            n: size

        Methods:
            calculate_mean()	Return mean from p and n.

            calculate_stdev()	Return standard deviation of the data set.

            replace_stats_with_data()   Return p and n value from the data set.

            plot_bar()  Output a histogram of the instance variable data using matplotlib pyplot library.

            pdf(k)  Return probability density calculator for the gaussian distribution. x (float): point for calculating the probability density function.

            plot_bar_pdf()  Plot the pdf of the binomial distribution
```
