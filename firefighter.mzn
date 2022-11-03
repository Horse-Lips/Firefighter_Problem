%======================== Pre-Defined Variables ========================%
include "count.mzn";                                                    %
                                                                        %
int:                       n;      %Number of nodes in G                %
int:                       T;      %Max time before game endds%         %
array[int] of int:         f;      %Initial fire locations              %
array[1..n, 1..n] of 0..1: G;      %Adjancey matrix Graph               %
int:                       budget; %Num firefighters  placed per turn   %
%=======================================================================%
array[1..n] of var 0..T: d;   %Time each node is defended
array[1..n] of var 0..T: b;   %Time each node is burned

constraint forall(i in f)(b[i] == 1);   %Initial fire locations
constraint count(b, 1, length(f));      %Max fires at t = 1
constraint count(d, 1, 0);              %No nodes defended at t = 1

constraint forall(i in 1..length(f))(
    if     b[i] != 0 then d[i] == 0     %Cannot defend burning nodes
    elseif d[i] != 0 then b[i] == 0     %Cannot burn defended nodes
    else true endif
);

constraint forall(t in 1..T)(
    count(j in d)(j == t) <= budget %Remain in budget for each time t
);

constraint forall(x in 1..n)(
    forall(y in 1..length(row(G, x)))(
        if G[x, y] == 1 /\ b[y] != 0 then
            if b[x] == 0 \/ b[x] > b[y] then
                if d[x] == 0 \/ d[x] > b[y] then
                    b[x] + d[x] == b[y] + 1
                endif
            endif
        endif
    )
);

solve maximize count(b, 0);    %Maximise the number of "saved" nodes
