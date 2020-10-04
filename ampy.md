---
title: How to use ampy with M5Stick-C
author: Miguel Maltez Jose
date: 20201003
---

```
export AMPY_PORT=/dev/tty.usbserial-7952A013B4
```

Connect to the Stick-C serial terminal

```
screen /dev/tty.usbserial-7952A013B4 115200
```

And kill the screen by pressing Ctrl+A followed by Ctrl+\\ press yes and enter.

```
ampy ls
```
