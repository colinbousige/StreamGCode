# Simple G-Code creator for precise Direct-writing  <a href="https://zenodo.org/badge/latestdoi/417509535"><img src="https://zenodo.org/badge/417509535.svg" alt="DOI" align="right"></a>


- [About this app](#about-this-app)
- [Usage](#usage)
- [Support](#support)
- [How to cite](#how-to-cite)
- [License](#license)

## About this app

This App was initially developed during an academic research project, WEPRINT, funded by the French National Research Agency (N° ANR-16-CE09-0008-01). See the related paper reference in [How to cite](#how-to-cite).

The first aim was to design specific patterns for a device of direct writing. As the device used a combination of a 3D printer and an electric field, the printing precision was very high and the pattern had to be made of lines a few hundreds to a few thousands of nanometers wide. As such a scale was not easy to manage with conventional CAD softwares, at least at that time, the idea to develop this App came naturally.

This application is meant to help you write GCcode files for various shapes:

- Lines
- Circles with inner grid
- Spirals

**See the running app [here](https://share.streamlit.io/colinbousige/streamgcode/GCode.py).**

## Usage

Select the shape you want to produce at the top of the sidebar, then enter all your parameters in the sidebar panel. The resulting shape is drawn in the right panel with a color ranging from green to red, *i.e.* from start to end of the printing. The printing area is represented by the thick black rectangle.

Once you are happy with your shape, click the "Download GCODE" button to download the resulting GCode file.

The "Remote voltage/current control" checkbox adds the lines "M42 S255 P5" and "M42 S24 P4" in the GCode initialization to allow for remote control of the voltage and current.

The image of the structure can be saved by right clicking on it and saving it.

## Support

This app was made by [Colin Bousige](mailto:colin.bousige@cnrs.fr). Contact me for support or to signal a bug.

## How to cite

This work is related to the article [*"Potential of a bi-functional scaffold fabricated by direct-writing electrospinning for the periodontal regeneration"*, Laura Bourdon, Nina Attik, Liza Benami, Charlène Chevalier, Colin Bousige, Arnaud Brioude and Vincent Salles, *Acta Biomaterialia* (2022), pages](http://doi.org/the_doi). Please cite this work if you publish using this code:

```bibtex
@article{Bourdon_2022,
    title = {Potential of a bi-functional scaffold fabricated by direct-writing electrospinning for the periodontal regeneration},
    author = {Bourdon, Laura and Attik, Nina and Benami, Liza and Chevalier, Charlène and Bousige, Colin and Brioude, Arnaud and Salles, Vincent},
    journal = {Acta Biomaterialia},
    volume = {},
    year = {2022},
    pages = {}
    doi = {}
    }
```

The source can be found [on Github](https://github.com/colinbousige/StreamGCode), please consider citing it too:

```bibtex
@software{Bousige_Simple_G-Code_creator,
    author = {Bousige, Colin},
    title = {{Simple G-Code creator for precise Direct-writing}},
    url = {https://github.com/colinbousige/StreamGCode}
}
```

## License

This work is licensed under a <a rel="license" href="http://creativecommons.org/licenses/by-nc/4.0/">Creative Commons Attribution-NonCommercial 4.0 International License</a>.

<a rel="license" href="http://creativecommons.org/licenses/by-nc/4.0/"><img alt="Creative Commons License" style="border-width:0" src="https://i.creativecommons.org/l/by-nc/4.0/88x31.png" /></a>
