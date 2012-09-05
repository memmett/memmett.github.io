divert(-1)dnl
include(`defaults.m4')

divert(0)dnl
include(`head.m4')dnl

<img style="margin: 0; padding 0; margin-right: 1em; float: right;"
     alt="portrait"
     src="memmett.gif"
     width="200"
     height="150"/>

<p style="font: 80% sans; margin-left: 3em; margin-top: -1em;">
  Postdoc. Lawrence Berkeley National Lab (Computational Mathematics).<br/>
  Postdoc. University North Carolina at Chapel Hill (Applied Mathematics).<br/>
  PhD. University of Alberta (Applied Mathematics, 2010).<br/>
  MSc. University of Calgary (Applied Mathematics, 2005).<br/>
  BSc. Simon Fraser University (Mathematical Physics, 2001).
</p>


<h2>Contact</h2>

<iframe src="http://www.google.com/talk/service/badge/Show?tk=z01q6amlqq3bl427r5i9kfuguh9tjr3atgk2n0i6stvuuk5aune5cjqmcmrkq2h9q9e57rjs802tbemthceehh5j4chmbd5pabiesjpr8mlj3f935262fprbhvd608abis8g6hvb2t28gqakcrgudmn9d7esl550e4bu7vuhd&amp;w=200&amp;h=60" frameborder="0" allowtransparency="true" width="200" height="60"></iframe>

<pre>
divert(-1)dnl
Office:  Chapman Hall, 448
Phone:   919-843-7901
divert(0)dnl
Email:   <a href="mailto:memmett@gmail.com">memmett@gmail.com</a>
divert(-1)dnl
Mail:    Department of Mathematics
         CB #3250, Phillips Hall
         Chapel Hill, NC, 27599
divert(0)dnl
CV:      <a href="MWE_CV.pdf">PDF</a>
</pre>
divert(0)dnl

divert(-1)dnl
<h2>Teaching</h2>

<p>Currently, I am not teachingy courses.</p>

<ul>
  <li><a href="m101_09w/">MATH 101 (EV1) - Winter 2009</a></li>
</ul>
divert(0)dnl

<h2>Current research</h2>

<p>
  I am a postdoc at the
  <a href="https://ccse.lbl.gov/">Center for Computational Sciences and Engineering</a> at the
  <a href="http://www.lbl.gov/">Lawrence Berkeley National Laboratory</a> in Berkeley CA.
</p>

<h3>SDC + AMR</h3>

<h3>Time-parallel schemes</h3>

<p>
  My previous postdoc was at the University of North Carolina at
  Chapel Hill under the supervision of 
  <a href="http://amath.unc.edu/Minion/Minion">Michael Minion</a>.
  My research there was primarily focused on the <i>parallel full
  approximation scheme in space and time</i> </a> (<a
  href="http://pypfasst.readthedocs.org/">PFASST</a>) scheme for parallel-in-time integration
  of PDEs.
</p>

<p>
  PFASST is a novel approach to time parallelism that iteratively
  improves the solution on each time slice by applying deferred
  correction sweeps to a hierarchy of discretizations at different
  spatial and temporal resolutions.  The coarse resolution problems
  are formulated using a time-space analog of the full approximation
  scheme used in multi-grid methods.
</p>

divert(-1)dnl
<p>
  PFASST has been tested on a suite PDEs in simple geometries.  Please
  see the <a href="pfasst_gallery.html">PFASST gallery</a> for examples.
  Preliminary tests have yielded parallel efficiencies typically
  between 40-60% on various numbers of processors from 4 to 512.
</p>
divert(0)dnl

<p>
  We are currently collaborating with:
  <ul>
    <li>
    Dr. J. Bell and the <a href="http://ccse.lbl.gov">CCSE</a> group
    at LBNL.  We hope to apply SDC and PFASST techniques to various
    codes developed at the CCSE.

    <li>
    Dr. D. Ruprecht at the USI in Lugano, CH.  We have successfully
    applied PFASST to several geophysical flow examples, and
    ultimately hope to apply PFASST techniques to climate and weather
    codes.

    <li>
    Dr. R. Speck at the USI in Lugano, CH.  We have successfully
    used PFASST in conjunction with the Pretty Efficient Parallel
    Coulomb Solver
    (<a href="http://wwwgsb.fz-juelich.de/ias/jsc/EN/AboutUs/Organisation/ComputationalScience/Simlabs/slpp/SoftwarePEPC/_node.html">PEPC</a>)
    to solve large N-body problems on JUGENE.
  </ul>
</p>

<h3>High-order spatial reconstructions</h3>

<p>
  I have collaborated with
  <a href="http://www.kaust.edu.sa/academics/faculty/ketcheson.html">David Ketcheson</a> <i>et al.</i>
  to incorporate high-order Weighted Essentially Non-oscillatory
  (WENO) schemes into
  <a href="http://numerics.kaust.edu.sa/pyclaw/">PyClaw</a>.
</p>

<p>
  <a href="http://memmett.github.com/PyWENO/">PyWENO</a>
  (of which I am the primary author) was used to generate
  Fortran 90 routines that perform WENO reconstructions within PyClaw.
  The routines can perform WENO reconstructions from 5th to 17th
  order.
</p>

<p>
  The PyWENO project provides a set of open source tools for
  constructing high-order Weighted Essentially Non-oscillatory (WENO)
  methods and performing high-order WENO reconstructions.
</p>

<h2>Publications</h2>

<p>
  Please see my <a href="http://www.mendeley.com/profiles/matthew-emmett/">Mendeley page</a> for a list of my publications.
</p>

divert(-1)dnl
<h2>Local resources</h2>

<ul>
  <li><a href="unix.html">UN*X</a> notes for the Dept. of Math & Stats at the U. of Alberta.</li>
  <li><a href="outreach/">Outreach</a> puzzles for the GAME Outreach program.</li>
dnl  <li><a href="tex.html">TeX</a> notes for assignments, labs, and presentations.</li>
</ul>
divert(0)dnl

<h2>Software projects</h2>

<p>
  I maintain the following software projects:
</p>

<ul>
  <li><a href="http://pypfasst.readthedocs.org">PFASST</a>- the PFASST (parallel-in-time) project.</li>
  <li><a href="http://pyweno.readthedocs.org">PyWENO</a>- a Python implementation of WENO approximations.</li>
dnl  <li><a href="http://memmett.github.com/PyBLAW">PyBLAW</a>- a Python framework for numerically solving systems of balance laws (conservation laws).</li>
  <li><a href="http://memmett.github.com/PyAsy">PyAsy</a>- a Python module for creating plots with Asymptote.</li>
</ul>

<p>
  I have also contributed to:
</p>

<ul>
  <li><a href="http://numerics.kaust.edu.sa/pyclaw/">PyClaw</a> - A Python based solver for hyperbolic PDEs that includes the algorithms of ClawPack and SharpClaw.</li>
</ul>

<a id="research"><h2>Other research interests</h2></ha>

<p>My other research interests include:</p>

<ul>

  <li>Numerical Analysis - Efficient implementation of Finite Volume
  schemes.  Weighted Essentially Non-Oscillatory schemes for
  hyperbolic systems.</li>

  <li>Partial Differential Equations - Systems of hyperbolic
  conservation and balance laws, perturbation theory, Sobolev spaces,
  and weak solutions.</li>

  <li>Fluid Mechanics - Fluid dynamics, geophysical and environmental
  flows, gravity currents and sediment transport, free boundary flows
  and surface tension, turbulence, and applications in biology.</li>

  <li>Non-linear Dynamics and Chaos - Fixed point stability,
  bifurcations, and simple examples of the onset of chaos.</li>

  <li>Differentiable Manifolds - Hamiltonian mechanics, Lie groups,
  holonomic and non-holonomic reduction of constraints.</li>

  <li>Traffic Modeling - Incorporating stochastic phenomena into
  hyperbolic models of traffic flow.</li>

  <li>Dendrochronology - Analysing tree-ring width data to determine
  the time of death of dead trees.</li>

</ul>

include(`foot.m4')
