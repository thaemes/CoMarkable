![](2021-02-02-20-53-15.png)

# CoMarkable
POC / WIP for ReMarkable tablets to work with multiple tablets on one document/illustration in real time. It reproduces penstrokes from device A on device B and vice versa. 

**Largely based on [LinusCDE - rmWacomToMouse](https://github.com/LinusCDE/rmWacomToMouse)**

## State 

Hacky and shaky. Currently it works uni-directionally; it copies the strokes from one tablet to another. The two tablets talk to each other directly, but a server in should be made, especially if we want to support more than two devices in the future. 

Requires installing python3 on the tablet for example via entware.

## To do

- [ ] Do not send pen hover events
- [ ] Include sender information in stroke events to prevent infinite-loop stroke copying
OR
- [ ] Create second Wacom device to prevent infinite-loop and glitches
- [ ] RM2 support
- [ ] Write server program to support >2 devices and ease set up

