# watermark

* Add watermark to file

* Plz install requirement package before use.

    ```bash
    git clone https://github.com/X3NNY/watermark.git
    cd ./watermark
    pip install -r requirements.txt
    ```
## Usage

* `python watermark.py -h`
    
    ```bash
    usage: watermark.py [-h] -p PATH [-d DEPTH] [-o OUTPUT] [-k] [-s SUFFIX] [watermark]

    Watermark for PDF

    positional arguments:
    watermark

    optional arguments:
    -h, --help            show this help message and exit
    -p PATH, --path PATH  Add all if path is a directory
    -d DEPTH, --depth DEPTH
                            The traversal depth（default 1）
    -o OUTPUT, --outpt OUTPUT
                            The ouput path of watermark file (default .)
    -k, --keep-structure  Keep the folder structure if exists
    -s SUFFIX, --suffix SUFFIX
    ```

* `python watermark.py Hello -p ./test.pdf`

    Add a watermark `Hello` to `./test.pdf`, Create a file named `./test-水印.pdf`, if u want to change the filename suffix, plz use option `-s` or `--suffix` to specify suffix(default `-水印`). 

* `python watermark.py Hello -p ./`

    Add a watermark `Hello` to every file in the directory `./`

    Attention, it will not add a watermark to the files in the sub-directory, if u want, plz use option `-d` or `--depth` to specify the traversal depth.

* `python watermark.py Hello -p ./a -o ./b`

    Add a watermark to every file in the directory `./a` and create the watermark-file in the directory `./b` 

* `python watermark.py Hello -p ./a -o ./b -k`

    Use the option `-k` or `--keep-structure` to maintain the directory structure of the output file.

    EG: 

    ```txt
    ./a
    -> ./a/a.pdf
    -> ./a/b/b.pdf
    ```

    result if not using this option

    ```txt
    ./b
    -> ./b/a-水印.pdf
    -> ./b/b-水印.pdf
    ``` 

    result if this option is used

    ```txt
    ./b
    -> ./b/a-水印.pdf
    -> ./b/b/b-水印.pdf
    ```

    As u see, it will automatically create a directory structure(unless u don't permission)

* `python watermark.py Hello -p ./a -o @ -d 5 -k`

    The output path can be `@`, we use it to represent the input file path. So this way we can generate the watermark file in the original location.

## EG



## Feature

* The sad thing is that now only supports ascii characters or Chinese on MAC, for other UNICODE characters maybe supported in the near future.XD.

* More convenient functions will come later...