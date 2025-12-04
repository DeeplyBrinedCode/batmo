Exception in Tkinter callback
Traceback (most recent call last):
  File "/usr/lib/python3/dist-packages/RPi/GPIO/__init__.py", line 393, in _gpio_list
    return tuple(_to_gpio(int(channel)) for channel in chanlist)
                ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
TypeError: 'int' object is not iterable

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/usr/lib/python3.11/tkinter/__init__.py", line 1948, in __call__
    return self.func(*args)
           ^^^^^^^^^^^^^^^^
  File "/usr/lib/python3.11/tkinter/__init__.py", line 861, in callit
    func(*args)
  File "/usr/lib/python3/dist-packages/matplotlib/backends/_backend_tk.py", line 251, in idle_draw
    self.draw()
  File "/usr/lib/python3/dist-packages/matplotlib/backends/backend_tkagg.py", line 10, in draw
    super().draw()
  File "/usr/lib/python3/dist-packages/matplotlib/backends/backend_agg.py", line 405, in draw
    self.figure.draw(self.renderer)
  File "/usr/lib/python3/dist-packages/matplotlib/artist.py", line 74, in draw_wrapper
    result = draw(artist, renderer, *args, **kwargs)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/lib/python3/dist-packages/matplotlib/artist.py", line 51, in draw_wrapper
    return draw(artist, renderer)
           ^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/lib/python3/dist-packages/matplotlib/figure.py", line 3092, in draw
    DrawEvent("draw_event", self.canvas, renderer)._process()
  File "/usr/lib/python3/dist-packages/matplotlib/backend_bases.py", line 1230, in _process
    self.canvas.callbacks.process(self.name, self)
  File "/usr/lib/python3/dist-packages/matplotlib/cbook/__init__.py", line 312, in process
    self.exception_handler(exc)
  File "/usr/lib/python3/dist-packages/matplotlib/cbook/__init__.py", line 96, in _exception_printer
    raise exc
  File "/usr/lib/python3/dist-packages/matplotlib/cbook/__init__.py", line 307, in process
    func(*args, **kwargs)
  File "/usr/lib/python3/dist-packages/matplotlib/animation.py", line 900, in _start
    self._init_draw()
  File "/usr/lib/python3/dist-packages/matplotlib/animation.py", line 1722, in _init_draw
    self._draw_frame(frame_data)
  File "/usr/lib/python3/dist-packages/matplotlib/animation.py", line 1744, in _draw_frame
    self._drawn_artists = self._func(framedata, *self._args)
                          ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/jcrisp1/testing.py", line 73, in update_plot
    dist = get_distance()
           ^^^^^^^^^^^^^^
  File "/home/jcrisp1/testing.py", line 35, in get_distance
    GPIO.output(TRIG, False)
  File "/usr/lib/python3/dist-packages/RPi/GPIO/__init__.py", line 744, in output
    gpios = _gpio_list(channel)
            ^^^^^^^^^^^^^^^^^^^
  File "/usr/lib/python3/dist-packages/RPi/GPIO/__init__.py", line 396, in _gpio_list
    return (_to_gpio(int(chanlist)),)
            ^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/lib/python3/dist-packages/RPi/GPIO/__init__.py", line 356, in _to_gpio
    raise RuntimeError(
RuntimeError: Please set pin numbering mode using GPIO.setmode(GPIO.BOARD) or GPIO.setmode(GPIO.BCM)

(GPIO.BOARD) or GPIO.setmode(GPIO.BCM)