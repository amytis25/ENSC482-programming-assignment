clc
clear
close all

%% define decision matrix
a1 = [20, 20, 0, 10];
a2 = [10, 10, 10, 10];
a3 = [0, 40, 0, 0];
a4 = [0, 40, 0, 0];

decision_matrix = [a1; a2; a3; a4]

%% maximin
% get the minimum of each act
a1_min = min(a1);
a2_min = min(a2);
a3_min = min(a3);
a4_min = min(a4);

% get the index of which act has the maximum of the set of minimums
[maximin_Util, idx_maximin] = max([a1_min, a2_min, a3_min, a4_min]);
disp (['according to the maximin rule, you would choose act ' num2str(idx_maximin) '.']);

%% maximax
% get the maximum of each act
a1_max = max(a1);
a2_max = max(a2);
a3_max = max(a3);
a4_max = max(a4);

% get the index of which act has the maximum of the set of minimums
[maximax_Util, idx_maximax] = max([a1_max, a2_max, a3_max, a4_max]);
disp (['according to the maximax rule, you would choose act ' num2str(idx_maximax) '.']);

%% minimax regret
% loop through each column creating a regret matrix
for i= 1: length(a1)
    ColMax(i) = max([a1(i), a2(i), a3(i), a4(i)]);
    a1_regret(i) = a1(i)-ColMax(i);
    a2_regret(i) = a2(i)-ColMax(i);
    a3_regret(i) = a3(i)-ColMax(i);
    a4_regret(i) = a4(i)-ColMax(i);
end 

% get the maximum of each act in regret matrix
a1_min_regret = min(a1_regret);
a2_min_regret = min(a2_regret);
a3_min_regret = min(a3_regret);
a4_min_regret = min(a4_regret);

% get the index of which act has the maximum of the set of minimums
[regret_Util, idx_regret] = max([a1_min_regret, a2_min_regret, a3_min, a4_min_regret]);
disp (['according to the minimax regret rule, you would choose act ' num2str(idx_regret) '.']);

%% optimism pessimism rule 
alpha = 0.3; % alpha > 0.25

% do calculations
a1_alpha = alpha * max(a1) + (1 - alpha) * min(a1);
a2_alpha = alpha * max(a2) + (1 - alpha) * min(a2);
a3_alpha = alpha * max(a3) + (1 - alpha) * min(a3);
a4_alpha = alpha * max(a4) + (1 - alpha) * min(a4);

% get the index of which act has the maximum of the set of minimums
[alpha_Util, idx_alpha] = max([a1_alpha, a2_alpha, a3_alpha, a4_alpha]);
disp (['according to the minimax regret rule, you would choose act ' num2str(idx_alpha) '.']);

%% principle of insufficient reason

a1_mean = mean(a1);
a2_mean = mean(a2);
a3_mean = mean(a3);
a4_mean = mean(a4);

[insufficient_Util, idx_insufficient] = max([a1_mean, a2_mean, a3_mean, a4_mean]);
disp (['according to the principle of insufficient reason, you would choose act ' num2str(idx_insufficient) '.']);


