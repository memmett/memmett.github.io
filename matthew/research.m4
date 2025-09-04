include(`defaults.m4')dnl
define(`_title', `Matthew Emmett - Research')dnl
include(`head.m4')dnl

<h2>Publications</h2>

<p>
  Please see my <a href="http://scholar.google.com/citations?user=Ko4HnnQAAAAJ&hl=en">Google scholar page</a> for a list of my publications.
</p>

<h2>Previous research</h2>

In the news at LBL: <a href="https://crd.lbl.gov/news-and-publications/news/2014/crd-researchers-give-combustion-system-design-a-boost/">CRD Researchers Give Combustion System Design a Boost -- Optimized Algorithms Help Methane Flame Simulations Run 6x Faster on NERSC Supercomputer</a>.

<h3>MLSDC + AMR</h3>

<p>Spectral Deferred Correction (SDC) schemes are iterative methods for
marching time-dependent problems through time.  SDC methods construct
high-order solutions within one timestep by iteratively approximating
a series of correction equations at collocation nodes using low-order
substepping methods.  SDC schemes converge to the collocation solution
(implicit Runge-Kutta schemes).

<p>Multi-level SDC (MLSDC) schemes use a hierarchy of SDC schemes with
varying number of collocation nodes to solve the collocation equation
on the finest MLSDC level (ie, the level with the most SDC nodes) by
cycling throught the MLSDC hierarchy in a V-cycle.  Coarse and fine
resolution SDC solutions on different MLSDC levels are coupled in the
same manner as used in the full approximation scheme (FAS) method
popular in multigrid methods for nonlinear problems.

<p>For example, the collocation nodes of a three level MLSDC scheme
with 3, 5, and 9 Gauss-Lobatto collocation nodes on the coarse,
middle, and fine levels has the following node hierarchy:

<center>
  <img src="mlpts.png"/><br/>
</center>

divert(-1)dnl
<p>The benefit of MLSDC in an AMR setting is that the coupling of the
AMR is increased due to iterative nature of MLSDC and the
incorporation of FAS corrections between levels: boundary conditions
between refinement patches become higher order.
divert(0)dnl

<p>I am currently developing an MLSDC+AMR solver for the
multicomponent, compressible reacting Navier-Stokes equation called
RNS.  RNS will be fourth order accurate in both space and time and
will showcase the MLSDC+AMR technique for combustion problems.  A
preliminary version of the code was used to create the movie below,
which shows a volume rendering of the vorticity resulting from a
turbulent jet.  This simulation was run across several thousand cores
of the Edison supercomputer at NERSC.

<center>
  <iframe width="420" height="315" src="https://www.youtube.com/embed/X984oHaQYcE" frameborder="0" allowfullscreen></iframe>
</center>

divert(-1)dnl
<h3>Multirate SDC</h3>
divert(0)dnl

<h3>Time-parallel schemes</h3>

<p>
  My previous postdoc was at the University of North Carolina at
  Chapel Hill under the supervision of
  <a href="https://crd.lbl.gov/departments/applied-mathematics/departmental-staff/michael-minion/">Michael Minion</a>.
  My research there was primarily focused on the <i>parallel full
  approximation scheme in space and time</i> </a> (<a
  href="https://pfasst.lbl.gov/">PFASST</a>) scheme for parallel-in-time integration
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
divert(0)dnl

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

<h2>Other research interests</h2>

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

  <li>Population Dynamics - Modeling population dynamics using
  Integral Projection Models (IPMs).</li>

</ul>

include(`foot.m4')
