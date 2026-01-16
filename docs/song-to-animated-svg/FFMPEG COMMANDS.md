
# Get wave

```
ffmpeg -i input -filter_complex "aformat=channel_layouts=mono,showwavespic=s=640x320:colors=black" \
  -frames:v 1 output.png
```


## make wave mono

`ffmpeg -i input -filter_complex "aformat=channel_layouts=mono,showwavespic=s=640x120" -frames:v 1 output.png`


## waveform video

```
ffmpeg -i input -filter_complex "[0:a]showwaves=s=1280x720:mode=line,format=yuv420p[v]" -map "[v]" -map 0:a -c:v libx264 -c:a copy output.mkv

```



###  all showwavespic options


- size, s
- split_channels
	Set if channels should be drawn separately or overlap. Default value is 0.
- colors
	Set colors separated by ’|’ which are going to be used for drawing of each channel.
- scale
	Set amplitude scale
		‘lin’ = Linear.
		‘log’ = Logarithmic.
		‘sqrt’ = Square root.
		‘cbrt’ = Cubic root.
	Default is linear.
-  draw

	Set the draw mode.
	‘scale’
		Scale pixel values for each drawn sample.
	‘full’
		Draw every sample directly.
	Default value is `scale`.

- filter
	Set the filter mode.
	‘average
		Use average samples values for each drawn sample.
	‘peak’
		Use peak samples values for each drawn sample.
	Default value is `average`.

