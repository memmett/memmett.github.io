divert(-1)dnl
#
# $Id: unix.m4,v 1.1 2009/05/05 22:55:02 memmett Exp $
#

include(`uofa.m4')

define(`_title', `UN*X notes')

divert(0)dnl
include(`head.m4')dnl
          
<p>
  These notes are intented for users of the Math & Stats network at
  the University of Alberta.  Unless otherwise stated, I usually work
  from <code>sirius3</code>, and will assume that you can login to
  this machine.  I will denote the shell prompt with a dollar sign, so

  <pre>
$ ls
  </pre>

  means that I want you to enter the 'ls' command at the shell
  prompt.
</p>

<h3>Running <code>MATLAB</code> and <code>Mathematica</code></h3>

<p>
  To run <code>MATLAB</code>:

  <pre>
$ ssh -X numbers
[enter login information]
$ matlab
  </pre>
</p>

<p>
  To run <code>Mathematica</code>:

  <pre>
$ xset +fp tcp/font.srv.ualberta.ca:7100
$ ssh -X numbers
[enter login information]
$ mathematica
  </pre>
</p>

<h3>JPEG (etc) to EPS</h3>

<p>
  To convert a JPEG to EPS there is a nice program out there called
  'jpeg2ps'.  It is efficient because it doesn't decompress the JPEG
  into a bitmap format and subsequently convert the the bitmap to an EPS
  raster, but rather wraps the JPEG in valid PostScript since
  PostScript engines can decompress JPEG themselves.  Anyway...
</p>

<p>
  Copy the jpeg2ps program to your home directory:

  <pre>
$ cp /tmp/jpeg2ps ~
$ chmod 755 ~/jpeg2ps
  </pre>
</p>

<p>
  Then, when you need to convert a JPEG to EPS:

  <pre>
$ ~/jpeg2ps in.jpg > out.eps
  </pre>
</p>

<p>
  If you want to convert other graphic formats to EPS, one efficient
  way is to convert the graphic to a JPEG and then to EPS:

  <pre>
$ convert in.bmp tmp.jpg
$ ~/jpeg2ps tmp.jpg > out.eps
  </pre>
</p>

dnl <h3>Fast and loose SSH</h3>

include(`foot.m4')
