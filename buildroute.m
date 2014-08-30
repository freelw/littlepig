function buildroute(x, y, route_begin, route_end)
    size = length(route_begin)
    for i = 1:size
        xarr = [x(route_begin(i)), x(route_end(i))]
        yarr = [y(route_begin(i)), y(route_end(i))]
        plot(xarr, yarr)
    end
end