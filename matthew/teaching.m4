include(`defaults.m4')dnl
define(`_title', `Matthew Emmett - Teaching')dnl
define(`_head', `<link rel="stylesheet" type="text/css" href="riemann.css"/>')dnl
include(`head.m4')dnl

<h2>Philosophy</h2>

<p>My goal as a teacher is to affect change in students.  I endeavour
to be an enthusiastic guide and resource for their learning
experience.  Practically, this means: treating students with respect;
encouraging interaction between myself and students; being prepared
and engaged; making myself available for extra help; trying to explain
concepts in such a way as to build students' intuition and conceptual
understanding; and building students' proficiency through examples,
quizzes, and assignments.

<p>I have experience teaching undergraduate courses, running tutorials
and labs, and coordinating and delivering outreach activities.  I am
technically saavy and can create novel and interactive online tools to
complement and enhance classroom activities.</p>

<h2>Experience</h2>

<table>
  <tr>
    <td style="width:70px;">Instructor</td>
    <td>Dept. of Mathemathics, <strong>University of North Carolina</strong>, Chapel Hill NC.</td>
  </tr>
  <tr>
    <td></td>
    <td>Differential equations and linear algebra (M383; upper level undergraduate class; class size: 35 students).</td>
  </tr>
  <tr><td>&nbsp;</td></tr>
  <tr>
    <td style="width:70px;">Instructor</td>
    <td>Dept. of Mathemathical and Statistical Sciences, <strong>University of Alberta</strong>, Edmonton AB.</td>
  </tr>
  <tr>
    <td></td>
    <td>Calculus II (M101; Winter 2008, class size: 80 students).</td>
  </tr>
  <tr>
    <td></td>
    <td>Calculus I (M100; Fall 2007, class size: 90 students).</td>
  </tr>
  <tr>
    <td></td>
    <td>Calculus II (M101; Fall 2006, class size: 90 students).</td>
  </tr>
  <tr><td>&nbsp;</td></tr>
  <tr><td>TA</td>
      <td>Dept. of Mathemathical and Statistical Sciences, <strong>University of Alberta</strong>, Edmonton AB.</td></tr>
  <tr>
    <td></td>
    <td>Calculus I, II, and III (M113, M100, M101, M209).  Differential
        Equations I (M201). Help sessions.  Class sizes typically 30 students.</td>
  </tr>
  <tr><td>&nbsp;</td></tr>
  <tr><td>TA</td>
      <td>Dept. of Mathemathics and Statistics, <strong>University of Calgary</strong>, Calgary AB.</td></tr>
  <tr>
    <td></td>
    <td>  Calculus I, II, and III (M249, M251, M253, M349); Linear Algebra I
  (M211, M221); Introduction to Fourier Analysis (M415); Continuous
  tutorials.  Class sizes ranging from 10 to 100 students.</td>
  </tr>
</table>

divert(-1)

\work{Instructor}{Dept. of Mathemathics, U. of North Carolina, Chapel
  Hill NC.}{Fall 2011}{Differential equations and linear algebra
  (M383).  Upper level undergraduate class; class size of 35
  students.}
\work{Instructor}{Dept. of Math and Stats, U. of Alberta, Edmonton AB.}{Winter 2008}{Calculus II (M101).  Class size roughly 80 students.}
\work{Instructor}{Dept. of Math and Stats, U. of Alberta, Edmonton AB.}{Fall 2007}{Calculus I (M100).  Class size roughly 90 students.}
\work{Instructor}{Dept. of Math and Stats, U. of Alberta, Edmonton AB.}{Fall 2006}{Calculus II (M101).  Class size roughly 90 students.}
\work{Teaching Assistant}{Dept. of Math and Stats, U. of Alberta, Edmonton AB.}{2005--2010}{%
  Calculus I, II, and III (M113, M100, M101, M209).  Differential
  Equations I (M201). Help sessions.  Class sizes roughly 30 students.}
\work{Teaching Assistant}{Dept. of Math and Stats, U. of Calgary, Calgary AB.}{2003--2005}{%
  Calculus I, II, and III (M249, M251, M253, M349); Linear Algebra I
  (M211, M221); Introduction to Fourier Analysis (M415); Continuous
  tutorials.  Class sizes ranging from 10 to 100 students.}

divert(0)


<h2>Outreach</h2>

divert(-1)
<img style="float: right; margin: 1em;" src="http://www.math.ualberta.ca/~adawson/kw/images/knapweed.gif"/>

<h3>The Invasive Spotted Knapweed Takeover</h3>

<p>As part of an outreach program at the University of Alberta, I
helped build an interactive web model for high-school students called
<a href="http://www.math.ualberta.ca/~adawson/kw/">The Invasive
Spotted Knapweed Takeover</a>.  This website teaches students about
matrix modelling, a type of mathematical model used in many fields
that can be understood with a basic background in Linear Algebra.

<p>The website has several interative features, including an
interative plot on the <a
href="http://www.math.ualberta.ca/~adawson/kw/controlling_growth.html">Controlling
Growth</a> page.</p>

<h2>Media</h2>

<p>The following is a shortened example of an interative tool that I
built to help students visualise the Riemann sum.</p>

<p>Technically, this tool is implemented using JavaScript and the <a
href="http://d3js.org/">d3</a> engine -- all one needs to view and
interact with this tool is a modern web browser (no extra plugins are
required).</p>
divert(0)

<h3>Integration as a Riemann sum</h3>

The Riemann integral given by

\[ \int_a^b f(x) \,dx = \lim_{N \rightarrow \infty} \sum_{i=1}^N f(x_i) \Delta x_i. \]

can be approximated by choosing a specific value for \(N\) and a regular
parition for the points \(x_i\).  The left, middle, and right Riemann
sums can be succinctly written as

\[ \int_a^b f(x) \,dx \approx R(\alpha, N) \equiv \Delta x \sum_{i=0}^{N-1} f\bigl(a + (i + \alpha) \Delta x\bigr), \qquad \Delta x = (b-a)/N \]

for \(\alpha = 0, 0.5, \) and \(1\) respectively.  For a specific
example we consider the function \[f(x) = 1 + \frac{8}{10} x^3\] drawn
in red and integrate it from -1 to 1.  The blue rectangles represent
the terms of the (approximate) Riemann sum.</p>

<p>Using the controls below to increase/decrease the number of terms
\(N\) in the Riemann sum, and to alter the \(\alpha\) parameter used
to determine where the function is sampled within each cell, we can
see a visual representation of the Riemann sum \(R(\alpha, N)\) above.</p>

<form action="#"><table>
<tr><td>\(N\):</td>
    <td><input type="range" id="n-input" min="5" max="200" step="5" value="10" onchange="update()" /></td>
    <td id="n-value">10</td></tr>
<tr><td>\(\alpha\):</td>
    <td><input type="range" id="a-input" min="0.0" max="1.0" step="0.25" value="0.0" onchange="update()"/></td>
    <td id="a-value">0.0</td></tr>
<tr><td>\(R(\alpha, N)\):</td><td id="ra-value"></td></tr>
</table></form>

<center>
  <div id="riemann"></div>
</center>

<script type="text/javascript" src="riemann.js"></script>

divert(-1)dnl
<p>Some things to consider:
<ul>
<li>What is the value of the integral?
<li>The function is monotonic (and increasing).  Show that \[ R(0, N) \leq \int_{-1}^{1} f(x) \,dx \leq R(1, N).\]
<li>Why does \(\alpha = 0.5\) do such a good job of approximating the integral, even for small \(N\)?
</ul>
divert(0)dnl
