function ret = circle(x, y, r)

    alpha = 0:pi/50:2*pi
    xarr = cos(alpha)*r + x
    yarr = sin(alpha)*r + y
    plot(xarr, yarr)

end