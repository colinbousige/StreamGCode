# Simple G-Code creator for precise Direct-writing

### About this app

This App was initially developed during an academic research project, WEPRINT, funded by the French National Research Agency (N° ANR-16-CE09-0008-01). See the related paper reference in [How to cite](#how-to-cite).

The first aim was to design specific patterns for a device of direct writing. As the device used a combination of a 3D printer and an electric field, the printing precision was very high and the pattern had to be made of lines a few hundreds to a few thousands of nanometers wide. As such a scale was not easy to manage with conventional CAD softwares, at least at that time, the idea to develop this App came naturally.

This application is meant to help you write GCcode files for various shapes:

- Lines
- Circles with inner grid
- Spirals

Select the wanted shape in the sidebar menu to go to the corresponding app.

### Usage

Select the shape you want to produce in the "App Navigation" dropdown menu on the left, then enter all your parameters in the sidebar panel. The resulting shape is drawn in the right panel with a color ranging from green to red, *i.e.* from start to end of the printing. The printing area is represented by the thick black rectangle.

Once you are happy with your shape, click the "Download GCODE" button to download the resulting GCode file.

The "Remote voltage/current control" checkbox adds the lines "M42 S255 P5" and "M42 S24 P4" in the GCode initialization to allow for remote control of the voltage and current.

The image of the structure can be saved by right clicking on it and saving it.

### Support

This app was made by [Colin Bousige](mailto:colin.bousige@cnrs.fr). Contact me for support or to signal a bug, or leave a message on the [GitHub page of the app](https://github.com/colinbousige/StreamGCode).

### How to cite

This work is related to the article [*"Direct-Writing Electrospun Functionalized Scaffolds for Periodontal Regeneration: In Vitro Studies"*, Laura Bourdon, Nina Attik, Liza Benami, Charlène Chevalier, Colin Bousige, Arnaud Brioude and Vincent Salles, *J. Funct. Biomater.* **14**(5) (2023), 263](https://doi.org/10.3390/jfb14050263). Please cite this work if you publish using this code:

```bibtex
@article{bourdon_potential_2023,
    title = {Direct-Writing Electrospun Functionalized Scaffolds for Periodontal Regeneration: In Vitro Studies},
    author = {Bourdon, Laura and Attik, Nina and Benami, Liza and Chevalier, Charlène and Bousige, Colin and Brioude, Arnaud and Salles, Vincent},
    journal = {J. Funct. Biomater.},
    volume = {14},
    year = {2023},
    pages = {263}
    doi = {10.3390/jfb14050263}
}
```

The source can be found [on Github](https://github.com/colinbousige/StreamGCode), please consider citing it too:

```bibtex
@software{Bousige_Simple_G-Code_creator,
    author = {Bousige, Colin},
    title = {{Simple G-Code creator for precise Direct-writing}},
    url = {https://github.com/colinbousige/StreamGCode},
    doi = {10.5281/zenodo.7781855}
}
```

### License

This work is licensed under a <a rel="license" href="http://creativecommons.org/licenses/by-nc/4.0/">Creative Commons Attribution-NonCommercial 4.0 International License</a>.

<a rel="license" href="http://creativecommons.org/licenses/by-nc/4.0/"><img alt="Creative Commons License" style="border-width:0" src="https://i.creativecommons.org/l/by-nc/4.0/88x31.png" /></a>
