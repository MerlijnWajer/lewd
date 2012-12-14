/*
 * This file is part of the LEd Wall Daemon (lewd) project
 * Copyright (c) 2009-2012 by ``brainsmoke'' and Merlijn Wajer (``Wizzup'')
 *
 *   lewd is free software: you can redistribute it and/or modify
 *   it under the terms of the GNU General Public License as published by
 *   the Free Software Foundation, either version 3 of the License, or
 *   (at your option) any later version.
 *
 *   lewd is distributed in the hope that it will be useful,
 *   but WITHOUT ANY WARRANTY; without even the implied warranty of
 *   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
 *   GNU General Public License for more details.
 *
 *   You should have received a copy of the GNU General Public License
 *   along with lewd.  If not, see <http://www.gnu.org/licenses/>.
 *
 * See the file COPYING, included in this distribution,
 * for details about the copyright.
 */

#define _BSD_SOURCE
#include <sys/ioctl.h>

#include <linux/spi/spidev.h>

#include <unistd.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <stdio.h>
#include <fcntl.h>
#include <math.h>
#include <sys/time.h>
#include <time.h>

int spi_transfer(int fd, char *in, const char *out, size_t len)
{
	struct spi_ioc_transfer transfer =
	{
		.tx_buf        = (unsigned long)out,
		.rx_buf        = (unsigned long)in,
		.len           = len,
		.delay_usecs   = 0,
	};

	return ioctl(fd, SPI_IOC_MESSAGE(1), &transfer);
}

int spi_open(const char *devname, int mode, int speed, int bits_per_word)
{
	int fd = open(devname, O_RDWR);

	if (fd < 0)
		return fd;
	
	if ( (ioctl(fd, SPI_IOC_WR_MODE, &mode) == 0) &&
	     (ioctl(fd, SPI_IOC_WR_BITS_PER_WORD, &bits_per_word) == 0) &&
	     (ioctl(fd, SPI_IOC_WR_MAX_SPEED_HZ, &speed) == 0) )
		return fd;

	close(fd);
	return -1;
}

void init_colortab(unsigned char colortab[6144])
{
	int i, r, g, b;

	for (i=0; i<2048; i++)
	{
		if (i<256)
		{
			r = i*3;
			g = (int)(pow((float)i/256., 1.5)*1024.);
			b = (i*i)/256;
			if (r > 255) r = 255;
			if (g > 255) g = 255;
			if (b > 255) b = 255;
		}
		else
			r=g=b=0;
		colortab[i*3+1] = r;
		colortab[i*3  ] = g;
		colortab[i*3+2] = b;
	}
}

void apply_gamma(unsigned char colortab[6144], float gamma)
{
	int i;
	for (i=0; i<6144; i++)
		colortab[i] = (int)(pow((float)colortab[i]/256., gamma)*256);
}


void init_ca_map(int ca_map[2048])
{
	int i, val;

	for(i=0; i<2048; i++)
	{
		val = (int)(pow(i/256.,1.25)/3.7*256.);
		ca_map[i] = val < 2047 ? val : 2047;
	}
}

void fire(int fd, int width, int height, int transform_map[])
{
	char send_buf[height*width*3]; memset(send_buf, 0, sizeof(send_buf));
	int w = width*2, h = height*2; int s=w*(h+1);
	int cells[s]; memset(cells, 0, sizeof(cells));
	int ca_map[2048]; init_ca_map(ca_map);
	unsigned char color_tab[2048*3]; init_colortab(color_tab); apply_gamma(color_tab, 2.2);

	int j, y, i, sum;
	struct timeval tv; gettimeofday(&tv, NULL);

	int wait, usec=tv.tv_usec, fps = 0;

	for(;;)
	{
		for (i=w; i<s; i++)
		{
			sum = cells[i] + cells[i+1];
			cells[i-w] = ca_map[sum<2047?sum:2047];
			for (j=w-2, i++; j; j--, i++)
			{
				sum = cells[i-1] + cells[i] + cells[i+1];
				cells[i-w] = ca_map[sum<2047?sum:2047];
			}
			sum = cells[i] + cells[i-1];
			cells[i-1] = ca_map[sum<2047?sum:2047];
		}

		unsigned long noise = rand();
		for (i=s-w; i<s; i++)
		{
			cells[i] = (noise&1) ? 221 : 0;
			noise >>= 1;
		}

		for (i=y=0; y<height; y++)
			for (j=0; j<w; j+=2,i++)
			{
				int ix = ( cells[i*4-j] + cells[i*4-j+1] +
				           cells[i*4+w-j] + cells[i*4+w-j+1] ) >> 2;
				ix += ix << 1;
				int map = transform_map[i];
				map += map << 1;

				send_buf[map++] = color_tab[ix++];
				send_buf[map++] = color_tab[ix++];
				send_buf[map  ] = color_tab[ix  ];
			}

		spi_transfer(fd, NULL, send_buf, width*height*3);

		usec += 20000; usec %= 1000000;
		gettimeofday(&tv, NULL);
		wait = 1000000 + usec - tv.tv_usec; wait %= 1000000;
		if (wait < 20000)
			usleep(wait);
	}
}

void init_transform_map(int width, int height, int map[])
{
	int x, y;
	for (y=0; y<height; y++)
		for (x=0; x<width; x++)
			map[y*width+x] = (x&1) ? height*x + y : height*(x+1)-1 - y;
}

int main(int argc, char *argv[])
{
	if (argc < 2)
	{
		fprintf(stderr, "Usage: %s <spi-device>\n", argv[0]);
		exit(EXIT_FAILURE);
	}

	int fd = spi_open(argv[1], 0, 2000000, 8);

	int transform_map[12*10]; init_transform_map(12, 10, transform_map);

	fire(fd, 12, 10, transform_map);
}
