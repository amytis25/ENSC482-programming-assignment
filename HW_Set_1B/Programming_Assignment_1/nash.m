clc;
clear;
close all;

P1_AC = 10; P1_BC = 15; P1_AD = 14; P1_BD = 6;
P2_AC = 16; P2_BC = 20; P2_AD = 24; P2_BD = 12;
AC = [P1_AC, P2_AC];
BC = [P1_BC, P2_BC];
AD = [P1_AD, P2_AD];
BD = [P1_BD, P2_BD];

matrix = [AC AD;
          BC BD];
P1_A = [P1_AC, P1_AD]; P1_B = [P1_BC, P1_BD];
P2_C = [P2_AC; P2_BC]; P2_D = [P2_AD; P1_BD];
P1 = [P1_A; P1_B];
P2 = [P2_C, P2_D];

% Dimensions
[m, n] = size(P1);
% Build cell array with headers
M = cell(m+1, n+1);  % Extra row & column for headers
% Set column headers (Player 2)
M{1,2} = 'Player 2 (C)';
M{1,3} = 'Player 2 (D)';
% Set row headers (Player 1)
M{2,1} = 'Player 1 (A)';
M{3,1} = 'Player 1 (B)';
% Fill the formatted payoffs
for i = 1:m
    for j = 1:n
        M{i+1, j+1} = sprintf('[%d,%d]', P1(i,j), P2(i,j));
    end
end
% Display in command window
disp('Payoff Matrix:')
for i = 1:size(M,1)
    for j = 1:size(M,2)
        if isempty(M{i,j})
            fprintf('%15s', '');
        else
            fprintf('%15s', M{i,j});
        end
    end
    fprintf('\n');
end

if P1_AC > P1_BC && P1_AD > P1_BD
    disp ("Player 1's Dominant Strategy is to Pick A.")
elseif P1_AC < P1_BC && P1_AD < P1_BD
    disp ("Player 1's Dominant Strategy is to Pick B.")
else
    disp ("Player 1 has no dominant strategy.");
end

if P2_AC > P2_AD && P2_BC > P2_BD
    disp ("Player 2's Dominant Strategy is to Pick C.")
elseif P2_AC < P2_AD && P2_BC < P2_BD
    disp ("Player 2's Dominant Strategy is to Pick D.")
else
    disp ("Player 2 has no dominant strategy.");
end
AD_eq = false; AC_eq = false; BD_eq = false; BC_eq = false;
if P2_AD > P2_AC && P1_AD > P1_BD
    AD_eq = true; 
    disp ("Player 1 picking A and Player 2 Picking D is a Nash Equilibrium.")
end
if P2_AD < P2_AC && P1_AC > P1_BC
    AC_eq = true;
    disp ("Player 1 picking A and Player 2 Picking C is a Nash Equilibrium.")
end
if P2_BD > P2_BC && P1_AD < P1_BD
    BD_eq = true;
    disp ("Player 1 picking B and Player 2 Picking D is a Nash Equilibrium.")
end
if P2_BD < P2_BC && P1_AC < P1_BC
    BC_eq = true;
    disp ("Player 1 picking B and Player 2 Picking C is a Nash Equilibrium.")
end
if ~AD_eq && ~AC_eq && ~BD_eq && ~BC_eq
    disp("There is no Nash Equilibrium.")
end
%% Mixed Nash Equilibrium 
% for Player 2 indifference
p2 = (P1_AD - P1_BD) / (P1_BC - P1_BD - P1_AC + P1_AD);
% for Player 2 indifference
p1 = (P2_AD - P2_BD) / (P2_BC - P2_BD - P2_AC + P2_AD);

% Clamp values to [0, 1] in case of numeric instability
p1 = max(min(p1, 1), 0);
p2 = max(min(p2, 1), 0);

fprintf('Player 1 plays A with probability of %.2f, and B with probability of %.2f\n', p2, 1-p2);
fprintf('Player 2 plays C with probability of %.2f, and D with probability of %.2f\n', p1, 1- p1);

% Visualization of Expected Utility for Player 1
[x, y] = meshgrid(0:0.01:1);

% Expected payoff of Player 1 given mixed strategies
U1 = x.*(y*P1(1,1) + (1-y)*P1(1,2)) + (1-x).*(y*P1(2,1) + (1-y)*P1(2,2));

figure
contourf(x, y, U1, 20); colorbar
hold on
plot(p1, p2, 'ro', 'MarkerSize', 10, 'LineWidth', 2)
title('Expected Payoff for Player 1 with Mixed Strategies')
xlabel('(P1 plays A)')
ylabel('(P2 plays C)')
grid on

