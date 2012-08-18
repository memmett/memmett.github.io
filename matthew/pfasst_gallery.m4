divert(-1)dnl
include(`defaults.m4')

define(`_title', `PFASST gallery')
define(`_description', `Gallery of PDEs that PFASST has been applied to.')
define(`_keywords', `PFASST')

divert(0)dnl
include(`head.m4')dnl

<p>
  PFASST has been successfully applied to various PDEs including:
  <ul>
    <li>1D
      <ul>
        <li>Advection/diffusion</li>
        <li>Viscous Burger's</li>
        <li>Kuramoto-Silvashinsky</li>
        <li>Thin-film core-annular flow</li>
        <li>Geostrophic adjustment</li>
      </ul>
    </li>
    <li>2D
      <ul>
        <li>Advection/diffusion</li>
        <li>Kuramoto-Silvashinsky</li>
        <li>Shallow-water</li>
        <li>Boussinesq</li>
        <li>Incompressible Navier-Stokes (vorticity formulation)</li>
      </ul>
    </li>
    <li>3D
      <ul>
        <li>Advection/diffusion</li>
        <li>Incompressible Navier-Stokes (spectral projection method)</li>
      </ul>
  </ul>
</p>

<h2>Selected results</h2>

<h3>1D Kuramoto-Silvashinsky (KS)</h3>

<p>
  The 1D KS equation is
  \[  u_t + u u_x + u_{xx} + u_{xxxx} = 0.  \]
</p>

<h3>2D Kuramoto-Silvashinsky (KS)</h3>

<p>
  The 2D KS equation is
  \[  u_t + \tfrac{1}{2}|\nabla u|^2 + \nabla^2 u + \nabla^4 u = 0.  \]

  The simulation below was run on a square domain of length 100 with
  an initial condition consisting of several Fourier modes.  The fine
  discretisation consisted of 512x512 spatial points and 9
  Gauss-Lobatto SDC nodes.  The course discretisation consisted of
  256x256 spatial points and 5 Gauss-Lobatto SDC nodes.  The PFASST
  algorithm was run with 32 processors, and a parallel-speedup of
  roughly 50% was achieved.
</p>

<center>
  <embed src="movies/ks.mpg" type="video/mpeg" width="400" height="400" autostart="false"/>
</center>


<h3>2D Vorticity</h3>

<p>
  The 2D vorticity formulation of the incompressible Navier-Stokes
  equation is
  \[  \partial_t \omega + u \cdot \nabla \omega
         = \nu \nabla^2 \omega + f_{\omega}  \]
</p>
where \(\omega\) is the vorticity, \(u\) is the velocity,
\(\nu\) is the viscosity, and \(f_\omega\) represents external
forcing.  The vorticity is related to the stream function \(\psi\)
through \(\omega = -\nabla^2 \psi\), and the stream function is
subsequently related to the velocity \(u\) through \(u =
(\partial_y \psi, -\partial_x \psi)\).

<h2>Visualising the PFASST algorithm in action</h2>

<p>
  The movie below was generated from timing information obtained
  from running the 3D incompressible Navier-Stokes equation on three
  PFASST levels with 16 processors.  It shows function evaluations
  (white dots) at SDC nodes, restriction (blue bars) between levels,
  and interpolation (red bars) between levels.
</p>

<p>
  Note that the function evaluations on the finest level occur in
  parallel, while the function evaluations on the coarsest levels
  occur in serial.
</p>

<center>
  <embed src="movies/nstl.mpg" type="video/mpeg" width="530" height="100" autostart="false"/>
</center>


include(`foot.m4')
