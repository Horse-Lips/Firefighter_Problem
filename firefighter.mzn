include "alldifferent_except_0.mzn";
include "at_most.mzn";
include "count.mzn";

%======================== Pre-Defined Variables ========================%
int: maxTime;                       %Max time before game endds%        %
int: budget;                        %Num firefighters  placed per turn  %
                                                                        %
array[int] of int: fireLocations;   %Initial fire locations             %
array[int] of int: from;            %Edge representation                %
array[int] of int: to;              %of the graph                       %
%=======================================================================%

array[1..max(from)] of var 0..maxTime: defended;    %Time each node is defended
array[1..max(from)] of var 0..maxTime: onFire;      %Time each node becomes on fire

constraint forall(i in fireLocations)(onFire[i] == 1);              %Fires at initial locations
constraint at_most(length(fireLocations), onFire, 1);               %Most fires possible at t = 1
constraint forall(t in 1..maxTime)(at_most(budget, defended, t));   %Stay in budget for each time t

constraint forall(i in 1..max(from))(
    if     onFire[i]   != 0 then defended[i] == 0   %If the node is on fire it cannot be defended
    elseif defended[i] != 0 then onFire[i]   == 0   %If the node is defended it cannot be set on fire
    else true endif
);

constraint forall(t in 1..maxTime, i in 1..length(from))(           %For each t, for each edge
    if onFire[from[i]] == t then                                    %If node on fire at t
        if onFire[to[i]] == 0 \/ onFire[to[i]] > t then             %If adj node not on fire
            if defended[to[i]] == 0 \/ defended[to[i]] > t then     %If adj node not defended
                onFire[to[i]] == t + 1 endif endif endif            %Then adj node burns at t + 1
);

solve maximize count(onFire, 0);    %Maximise the number of "saved" nodes
output ["d: \(defended)\nf: \(onFire)"];
