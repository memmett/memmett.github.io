include(`defaults.m4')dnl
define(`_title', `Matthew Emmett - Research')dnl
include(`head.m4')dnl

<h2>Publications</h2>

<p>
  Please see my <a href="http://scholar.google.com/citations?user=Ko4HnnQAAAAJ&hl=en">Google scholar page</a> for a list of my publications.
</p>

<h2>Current research</h2>

<h3>SDC + AMR</h3>

<p>Spectral Deferred Correction (SDC) scheme are iterative methods for
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

<p>For Adaptive Mesh Refinement (AMR) schemes with many levels of
spatial refinement, a plain MLSDC scheme would suffer from exponential
growth of SDC nodes as new levels of spatial refinement are added.

<p>However, the benefit of MLSDC in an AMR setting is that the
coupling of the AMR is increased due to iterative nature of MLSDC and
the incorporation of FAS corrections between levels: boundary
conditions between refinement patches become higher order.

<p>My research in this area is currently focused on creating a new
MLSDC hierarchy that includes the benefits of the MLSDC FAS
corrections, but without the exponential growth of SDC nodes.

<h3>Time-parallel schemes</h3>

<p>
  My previous postdoc was at the University of North Carolina at
  Chapel Hill under the supervision of
  <a href="http://amath.unc.edu/Minion/Minion">Michael Minion</a>.
  My research there was primarily focused on the <i>parallel full
  approximation scheme in space and time</i> </a> (<a
  href="http://libpfasst.readthedocs.org/">PFASST</a>) scheme for parallel-in-time integration
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
