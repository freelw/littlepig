function littlepig
    subplot(1, 3, 1)
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
    
    subplot(1, 3, 2)
    hold on
    showflightnumarr
    hold off
    
    subplot(1, 3, 3)
    hold on
    showcost
    hold off
end