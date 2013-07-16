
import interpolate;
import graph;

size(4.75inch, 1.5inch, false);
defaultpen(fontsize(10pt));

real x1 = 0;
real x2 = 1;
real h = 0.075;

real[] gl3 = { 0.00000000,
                0.50000000,
                1.00000000 };

real[] gl5 = { 0.00000000,
                0.17267316,
                0.50000000,
                0.82732684,
                1.00000000 };

real[] gl9 = { 0.00000000,
               0.05012100,
               0.16140686,
               0.31844127,
               0.50000000,
               0.68155873,
               0.83859314,
               0.94987900,
               1.00000000 };


real[] gl95 = { 0.00000000,
                0.16140686,
                0.50000000,
                0.83859314,
                1.00000000 };

real y = 0;


void draw_pts(real[] pts, real x1, real x2, real y, marker mark) {
  for (int i=0; i<pts.length; ++i) {
    real x = x1 + (x2-x1) * pts[i];
    draw((x,y), mark);
  }
}

marker circle   = marker(scale(3.8)*unitcircle, Fill(black));
marker triangle = marker(scale(4.5)*polygon(3), Fill(black));
marker diamond  = marker(scale(4.5)*rotate(45)*polygon(4), Fill(black));


/*
 * proper subsets
 */

x1 = 0.0;
x2 = 0.4;

draw((x1-h,y)--(x2+h,y), Arrows);

label("$t_n$",     (x1,y+h), S);
label("$t_{n+1}$", (x2,y+h), S);
draw((x1,y+h/4)--(x1,y-h/4));
draw((x2,y+h/4)--(x2,y-h/4));

draw_pts(gl9, x1, x2, y-3h, diamond);
draw_pts(gl95, x1, x2, y-2h, triangle);
draw_pts(gl3, x1, x2, y-1h, circle);

label("$\ell=1$", (x1-h, y-h), W);
label("$\ell=2$", (x1-h, y-2h), W);
label("$\ell=3$", (x1-h, y-3h), W);

