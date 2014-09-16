function littlepig
    figure(1)
    hold on
    x = getsectorx
    y = getsectory
    route_begin = getroutebegin
    route_end = getrouteend
    circleinfo = getcircleinfo
    circlex = circleinfo(1)
    circley = circleinfo(2)
    circleR = circleinfo(3)
    buildsector(x,y)
    circle(circlex, circley, circleR)
    buildroute(x, y, route_begin, route_end)
    axis equal    
    hold off
    
    figure(2)
    hold on
    showflightnumarr
    hold off

    figure(3)
    hold on
    showcost
    hold off
end