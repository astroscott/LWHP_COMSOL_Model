%% LHP Parametric Sweeper:

% Author: Aaron Scott (GRC-LTE0)[GRC-LERCIP] Spring 2020 NASA Intern
% Date Created: 4/19/2020
% Last Modified: 4/22/2020

clear; clc;

%% Parameters:

filepath = "C:\Users\amscott3\Desktop\GRC Projects\COMSOL\Lattice Heat Pipe\lattice_hp_v03_Experimental.mph";
l_c = 4:2:20;
l_e = [4, 20];
Q_w = 1:80;

%% Main Script:

% Import dependencies:
import com.comsol.model.*
import com.comsol.model.util.*

% Make current directory match LHP_Iterator.m directory:
cd(fileparts(which(mfilename)));

% Initialize/check for data output files (prevents accidental overwrite):
if isfile('success_data.csv') || isfile('fail_data.csv')
    fprintf('\n! Script cancelled: please rename or move existing success_data.csv and fail_data.csv files.\n\n');
    return;
else
    success_data = fullfile('success_data.csv');
    fail_data = fullfile('fail_data.csv');
    write_to_csv(success_data, 'l_cv/l_ev', 'l_cv', 'l_ev', 'Q_wv', 'max_T', 'min_T');
    write_to_csv(fail_data, 'l_cv/l_ev', 'l_cv', 'l_ev', 'Q_wv', 'max_T', 'min_T');
end

% Load the model:
model = mphload(filepath);
model.hist.disable;

% Initialize variables:
progress = waitbar(0, 'Initializing...');
num_iter = length(l_c) * length(l_e) * length(Q_w);

progress_count = 0;
success_count = 1;
failure_count = 1;
success_array = [];
failure_array = [];

%% Perform parametric sweep:
fprintf('Initializing sweep: %g simulations to be completed...\n\n', num_iter);
for i = 1:length(l_c)
    for j = 1:length(l_e)
        for k = 1:length(Q_w)
            try
            % Update each parameter:
                model.param.set('L_c', num2str(l_c(i)) + "[mm]");
                model.param.set('L_e', num2str(l_e(j)) + "[mm]");
                model.param.set('Q_w', num2str(Q_w(k)) + "[W]");

            % Run the simulation:
                model.mesh.run;
                model.sol('sol1').runAll;

            % Retrieve results:
                l_cv = mphglobal(model,'L_c'); % verification that l_c has been updated properly
                l_ev = mphglobal(model,'L_e'); % verification that l_e has been updated properly
                Q_wv = mphglobal(model,'Q_w'); % verification that Q_w has been updated properly
                max_T = mphglobal(model, 'maxop1(T)');
                min_T = mphglobal(model, 'minop1(T)');

            % Log Sucesses:
                fprintf(['Success: LR %g (l_c = %d mm, l_e = %d mm, Q_w = %d' ...
                        ' W ::: Max Temp = %.2f K, Min Temp = %.2f K)\n'], ...
                        l_cv/l_ev, l_cv, l_ev, Q_wv, max_T, min_T);
                success_array(success_count, 1:6) = [l_cv/l_ev, l_cv, l_ev, Q_wv, max_T, min_T];
                write_to_csv(success_data, l_cv/l_ev, l_cv, l_ev, Q_wv, max_T, min_T);
                success_count = success_count + 1;

            % Log Failures & Skip remaining cases:
            catch error
                fprintf('Failure: LR %g (l_c = %d mm, l_e = %d mm, Q_w = %d W)\n', l_c(i)/l_e(j), l_c(i), l_e(j), Q_w(k))
                failure_array(failure_count, 1:4) = [l_c(i)/l_e(j), l_c(i), l_e(j), Q_w(k)];
                write_to_csv(fail_data, l_c(i)/l_e(j), l_c(i), l_e(j), Q_w(k), max_T, min_T);
                failure_count = failure_count + 1;
                progress_count = progress_count + 1 + length(Q_w) - k;
                waitbar(progress_count / num_iter, progress, 'Running...');
                break; % <- Skips remaining cases after failure
            end
            progress_count = progress_count + 1;
            waitbar(progress_count / num_iter, progress, 'Running...');
        end
    end
end

fprintf('\n\n Parametric Sweep Complete.\n');
waitbar(progress_count / num_iter, progress, 'Complete.');

%% Function Defintions

function write_to_csv(file, varargin)
    fid = fopen(file, 'at+');
    for i = 1:length(varargin)
      if i == length(varargin)
        fprintf(fid, '%s', num2str(varargin{i}));
      else
      	fprintf(fid, '%s,', num2str(varargin{i}));
      end
    end
    fprintf(fid, '\n');
    fclose(fid);
end