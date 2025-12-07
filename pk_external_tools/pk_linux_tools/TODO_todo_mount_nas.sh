#!/bin/bash
sudo umount /mnt/NAS1/30_VISION_DEV

cd / && mkdir mnt -p
cd mnt && sudo mkdir NAS1 -p
cd NAS1 && sudo mkdir 30_VISION_DEV -p

sudo mount 192.168.1.41:/volume1/30_VISION_DEV /mnt/NAS1/30_VISION_DEV

sudo umount /mnt/NAS2/30_VISION_DEV

cd / && mkdir mnt -p
cd mnt && sudo mkdir NAS2 -p
cd NAS2 && sudo mkdir 30_VISION_DEV -p

sudo mount xxx.xxx.x.xx:/volume1/30_VISION_DEV /mnt/NAS2/30_VISION_DEV
