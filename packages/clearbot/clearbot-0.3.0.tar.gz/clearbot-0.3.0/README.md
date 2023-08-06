# clearbot

Clearbit Logo API client.

`clearbot` fetches the logo of company (png file) based on their domain name.

## Install

The script in available through a python package.

```shell
pip install clearbot
```

## Get started

You can run directly the script on a domain.

```shell
clearbot github.com
```

![github](examples/github.com.png)

You can pass several domains as well.

```shell
clearbot github.com gitlab.com
```

A file can also be used as input (one domain by line).

```shell
clearbot -f ./domains.txt
```

By default it will output `/tmp/<DOMAIN>.png`. You can change the destination directory with the `-d` option.

```shell
clearbot -d . github.com
```

By default it outputs 512px png file (i.e. the greatest side has 512px). You can change it with the `-s` option.

```shell
clearbot -s 64 github.com
```

![64](examples/github.com.64.png)

Sometimes we may want to remove the white background (by using transparency: alpha = 0). For this purpose, you can use the `-t` options that thresholds the whites (it must be between 0 and 255 as it is applied on a grayscale version of the image).

```shell
clearbot -t 240 github.com
```

![alpha](examples/github.com.alpha.png)

Since `v0.3.0`, clearbot can colorize image (but it is still **experimental**). You can color the whites (resp. the blacks) by providing the `-w` flag (resp. the `-b` flag).

```shell
clearbot -t 235 -b "#FC6D26" github.com
```

![color](examples/github.com.color.png)

## What's next?

- Add tests
- Print result to the terminal
