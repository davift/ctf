# CTF

In this repository, I am making public my personal cheat sheet of key solutions and support scripts for Hacking CTFs.

After losing my hard drive with the history of previous events, I decided to make it public for my own use and for anyone else who stumbles upon it.

The scripts were hand-crafted while solving challenges from HTB, THM, ROG Emporium, PWNable.xyz, and more.

## Checks

The script `checks` is my shortcut (utilizing `pwntools`) for visualizing information from the `checksec` and `file` commands in a different layout, including comments and tips.

For ease of use, I created a symbolic link that is reachable from any directory with:

```
sudo ln -s /home/kali/Downloads/ctf/checks /usr/local/sbin/checks
```

## Finally

Feel free to use and propose modifications or improvements.
