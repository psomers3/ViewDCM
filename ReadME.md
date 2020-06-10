## ViewDCM

This is a quick DCM file viewer made to be compiled with pyinstaller:

```
pyinstaller ViewDCM.spec
```

Once compiled, pass the folder directory containing the .dcm files as an argument to the executable from the commandline. The files are assumed to be labeled sequentially in some sort of way (just a general sort is used). Using the left and right arrow keys will cycle through the images.
