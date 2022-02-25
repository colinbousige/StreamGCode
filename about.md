## Simple G-Code creator for precise Direct-writing

- [About this app](#about-this-app)
- [Usage](#usage)
- [Support](#support)
- [How to cite](#how-to-cite)
- [License](#license)

### About this app

This application is meant to help you write GCcode files for various shapes:

- Lines
- Circles with inner grid
- Spirals

### Usage

Click on the shape you want to produce in the navigation bar at the top, then enter all your parameters in the sidebar panel. The resulting shape is drawn in the right panel with a color ranging from green to red, *i.e.* from start to end of the printing. The printing area is represented by the thick black rectangle.

Once you are happy with your shape, click the "Download GCODE" button to download the resulting GCode file.

The "Remote voltage/current control" checkbox adds the lines "M42 S255 P5" and "M42 S24 P4" in the GCode initialization to allow for remote control of the voltage and current.

The image of the structure can be saved by right clicking on it and saving it.

### Support

This app was made by [Colin Bousige](mailto:colin.bousige@cnrs.fr). Contact me for support or to signal a bug.

### How to cite

This work is related to the article [*"Name of the article"*, L. Bourdon, C. Bousige, A. Brioude, V. Salles, *Journal* **volume** (2022), pages](http://doi.org/the_doi). Please cite this work if you publish using this code:

```bibtex
@article{Bourdon_2022,
    author = {},
    journal = {},
    volume = {},
    year = {2022},
    pages = {}
    doi = {}
    }
```

The source can be found [on Github](https://github.com/colinbousige/StreamGCode), please consider citing it to:

```bibtex
@software{Bousige_Simple_G-Code_creator,
    author = {Bousige, Colin},
    title = {{Simple G-Code creator for precise Direct-writing}},
    url = {https://github.com/colinbousige/StreamGCode}
}
```

### License

This work is licensed under a <a rel="license" href="http://creativecommons.org/licenses/by-nc/4.0/">Creative Commons Attribution-NonCommercial 4.0 International License</a>.

<a rel="license" href="http://creativecommons.org/licenses/by-nc/4.0/"><img alt="Creative Commons License" style="border-width:0" src="https://i.creativecommons.org/l/by-nc/4.0/88x31.png" /></a>
