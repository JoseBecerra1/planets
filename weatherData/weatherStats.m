% Exploratory data analysis
% Read the data of the weather stations from AZMET:
% https://cals.arizona.edu/azmet/az-data.htm
%  DAILY FILES  (2003 - Present) :
% =======================================
%
%    DATA POINT
%    NUMBERS -->    1  2  3  4    5    6    7    8   9   10   11  12 13  14
%                   |  |  |  |    |    |    |    |   |    |    |   |  |   |
%    DATA -->    2003,254,6,40.2,15.1,27.6,69.9,7.9,33.5,3.1,23.45,0,38,22.4,
%                           29.3,34.1,24.7,29.1,1.3,.5,14,66,4.2,12,6.2,6,.4,.2
%                            |    |    |    |   |  |   |  |  |   |   |  |  |  |
%    DATA POINT NUMBERS --> 15   16   17   18  19 20  21 22 23  24  25  26 27 28
%
%  * NOTE: Daily data is actually all on one line per day,
%          it has been put on two lines here to label each data point by number.
%
%   Data
%   Point    Description
%   ------  ---------------------
%    1   A   Year
%    2   B   Day of Year (DOY)
%    3   C   Station Number
%    4   D   Air Temp - Max
%    5   E   Air Temp - Min
%    6   F   Air Temp - Mean
%    7   G   RH - Max
%    8   H   RH - Min
%    9   I   RH - Mean
%   10   J   VPD - Mean
%   11   K   Solar Rad. - Total
%   12   L   Precipitation - Total
%   13   M    4" Soil Temp - Max  ( = 2" prior to 1999 )
%   14   N    4" Soil Temp - Min  ( = 2" prior to 1999 )
%   15   O    4" Soil Temp - Mean ( = 2" prior to 1999 )
%   16   P   20" Soil Temp - Max  ( = 4" prior to 1999 )
%   17   Q   20" Soil Temp - Min  ( = 4" prior to 1999 )
%   18   R   20" Soil Temp - Mean ( = 4" prior to 1999 )
%   19   S   Wind Speed - Mean
%   20   T   Wind Vector Magnitude for Day
%   21   U   Wind Vector Direction for Day
%   22   V   Wind Direction Standard Deviation for Day
%   23   W   Max Wind Speed
%   24   X   Heat Units (30/12.8 C) (86/55 F)                      | positions
%   25   Y   Reference Evapotranspiration (ETo) = Original AZMET   | switched 2003
% --------------------------------------------------------------------------------------
%   26   Z   Reference Evapotranspiration (ETos) = Penman-Monteith  'New' 2003-Present
%   27  AA   Actual Vapor Pressure - Daily Mean                     'New' 2003-Present
%   28  AB   Dewpoint, Daily Mean                                   'New' 2003-Present
%

clc;
clear;
close all;

% Stations names
station_name_vect = {'Phx Encanto'};
station_ID_vect = 15;
years_vect = 1988:2021;
N_years = length(years_vect);

path_read = './Encanto Data/'; % This has to be modified based on your directory

ind_stat = 1;
station_name = station_name_vect{ind_stat};
station_ID = station_ID_vect(ind_stat);

% Generate a vector with dates of each day, days since BC
datenum_vect = datenum(years_vect(1),1,1):datenum(years_vect(end),12,31);

% Initialize the matrix
N_variables = 28;
MAT_STATION = NaN(length(datenum_vect),N_variables);
day_index = 0; %initialize

for ind_year = 1:N_years
    
    year = years_vect(ind_year);

    if year >= 2003
        N_variables = 28; % total number of variables after 2003 included
    else
        N_variables = 25; % total number of variables before 2003
    end

    year_string = sprintf('%d',year);
    filename = sprintf('%02d%srd.txt',station_ID,year_string(3:4));
    
    fid = fopen([path_read,filename],'r');

    if fid > 0
        C = textscan(fid,'%f ','delimiter',',');
        fclose(fid);
        MAT_STATION_DUM = C{1};
        MAT_STATION_DUM = reshape(MAT_STATION_DUM,N_variables,length(MAT_STATION_DUM)/N_variables);
        MAT_STATION_DUM = MAT_STATION_DUM';
        % Assign values at the right position
        % Read the DOY of the first and last value

        if rem(year,4) == 0
            N_days_months = [31,29,31,30,31,30,31,31,30,31,30,31]; % Leap year
        else
            N_days_months = [31,28,31,30,31,30,31,31,30,31,30,31]; % Non leap year
        end
          
        N_days_months_cum = cumsum(N_days_months);
        % First value
        DOY_first = MAT_STATION_DUM(1,2);
        IND_DUM = find(DOY_first < N_days_months_cum);
        month_first = IND_DUM(1);

        if month_first == 1
            day_first = DOY_first;
        else
            day_first = DOY_first - N_days_months_cum(month_first - 1);
        end

        % Last value
        DOY_last = MAT_STATION_DUM(end,2);
        IND_DUM = find(DOY_last <= N_days_months_cum);
        month_last = IND_DUM(1);

        if month_last == 1
            day_last = DOY_last;
        else
            day_last = DOY_last - N_days_months_cum(month_last - 1);
        end

        IND_first = find(datenum_vect == datenum(year,month_first,day_first));
        IND_last = find(datenum_vect == datenum(year,month_last,day_last));
        display(sprintf('year = %d; Number of days is: %d',year,IND_last - IND_first + 1));
        
        MAT_STATION_DUM(MAT_STATION_DUM == 999) = NaN; %Clean data and remove 999
        %MAT_STATION_DUM(MAT_STATION_DUM == 000) = NaN; %Clean data and remove 999
        %MAT_STATION(IND_first:IND_last,1:N_variables) = MAT_STATION_DUM

        for x = 1:height(MAT_STATION_DUM)
            index = MAT_STATION_DUM(x,2) + day_index;
            MAT_STATION(index,1:N_variables) = MAT_STATION_DUM(x,:);
        end

        day_index = day_index + sum(N_days_months);

    end
end

[Y,M,D,~,~,~] = datevec(datenum_vect);
year_vect = unique(Y);
N_years = length(year_vect);
datenum_label = datenum(year_vect,6,15);
DV = datevec(datenum_vect); % give three vectors seperating in day and year

% can use retime function to seperate values based on dd, mm , yyyy
year_vect = unique(Y);
COL_PRECIP = 12;
N_years = length(year_vect);
N_months = 12;
% Initialize matrices
PrecipMonthly = NaN(12,N_years);
      
%    compute mean (monthly) - ignore missing data
for ind_year = 1:N_years
    for ind_month = 1:12
            IND_DUM = find(Y==year_vect(ind_year) & M == ind_month);
            PrecipMonthly(ind_month,ind_year) = sum(MAT_STATION(IND_DUM, COL_PRECIP), 'omitnan'); % function  
    end
end

%Considering all months with Precip maybe 0
%PrecipJan=rmmissing(nonzeros(PrecipMonthly(1,:)));
%Only considering months with Precip greater than 0
PrecipJan=rmmissing(nonzeros(PrecipMonthly(1,:)));

%Gamma distribution
% Using MLE to estimate alpha and beta from PrecipJan
AlphaBeta=gamfit(PrecipJan);

%Emperical CDF, hazen plot is incorrect
 j=1:length(PrecipJan);
 EmpericalCDF=(j-0.5)./length(PrecipJan);
 EmpericalCDF=transpose(EmpericalCDF);

%GammaCDF
 FittingGamma= gamcdf(sort(PrecipJan),AlphaBeta(1), AlphaBeta(2));% GammaCDF

 %Dn obs
 DnGammaobs= abs(EmpericalCDF-FittingGamma);
 DnGammaobs=max(DnGammaobs);

 figure
 plot(sort(PrecipJan),sort(FittingGamma),'g',LineWidth=2)
 hold on
 plot(sort(PrecipJan),EmpericalCDF,'.k',LineWidth=2)
 grid on
 xlabel('January Precipitation, mm','FontSize',12)
 ylabel('Cumulative Probabilty','FontSize',12)
 title('January Precipiation, Gamma Distribution v. ECDF',FontSize=12)
 legend('Gamma Distribution','ECDF','Location','southeast')

 %Storing Dn from variates
 k=0;
 iter= 1000; %1000 samples
 VariatesAlphaBeta= zeros(1000,2); %storing variates
 DnGammaMax=zeros(1000,1);

 for i=1:iter
    NVariatesGamma=gamrnd(AlphaBeta(1), AlphaBeta(2), [30 1]);
    GammaFit=gamfit(NVariatesGamma);
    AlphaVar=GammaFit(1);
    BetaVar=GammaFit(2);
    VariatesAlphaBeta(1+k,1)=AlphaVar(end,1);
    VariatesAlphaBeta(1+k,2)=BetaVar(end,1);
   
    FittingGamma= gamcdf(sort(NVariatesGamma),GammaFit(1), GammaFit(2)); %Theo CDF
    DnGamma= abs(EmpericalCDF-FittingGamma);
    DnGamma =max(DnGamma);
    DnGammaMax(1+k,1)=DnGamma(end,1);
    k=k+1;
 end

%one-sided tests, because the test statistic Dn is...
% the absolute value of the largest difference between...
% the parametric and empirical cumulative probabilities

%Guassian
Gauss_Param = fitdist(PrecipJan,'Normal');
mu = Gauss_Param.ParameterValues(1,1);
sigma = Gauss_Param.ParameterValues(1,2);
FittingGauss=normcdf(sort(PrecipJan),mu,sigma);
DnGaussObs=abs(EmpericalCDF-FittingGauss);
DnGaussObs=max(DnGaussObs);

figure
plot(sort(PrecipJan),sort(FittingGauss),'Color',[0.8500 0.3250 0.0980],LineWidth=2)
hold on
plot(sort(PrecipJan),EmpericalCDF,'.k',LineWidth=2)
grid on
xlabel('January Precipitation, mm','FontSize',12)
ylabel('Cumulative Probabilty','FontSize',12)
title('January Precipiation, Gaussian Distribution v. ECDF',FontSize=12)
legend('Gaussian Distribution','ECDF','Location','southeast')

P=0;
iter= 1000; %1000 samples
VariatesMuSigma= zeros(1000,2); %storing variates
DnGaussMax=zeros(1000,1);

 for i=1:iter
 NVariatesGauss=normrnd(mu, sigma, [30 1]);

    GuassFit=fitdist(NVariatesGauss,'Normal');
    muVar=GuassFit.ParameterValues(1,1);
    sigmaVar=GuassFit.ParameterValues(1,2);
    VariatesSigmaMu(1+P,1)=muVar(end,1);
    VariatesSigmaMu(1+P,2)=sigmaVar(end,1);
   
    FittingGauss= normcdf(sort(NVariatesGauss), muVar, sigmaVar); %Theo CDF
    DnGuass= abs(EmpericalCDF-FittingGauss);
    DnGuass =max(DnGuass);
    DnGaussMax(1+P,1)=DnGuass(end,1);
    P=P+1;
 end


figure 
plot(1:1000,sort(DnGaussMax))
 %null hypothesis: the precipitation data were from the fitted distribution
 %alternative hypothesis: the precipation data was not drawn from fitted
 %distribution
 %One sided test, since dn is abs value of largest differnce 
 %values on far right tail, large discrepaniceis unfavorable to H0
 %values on left tail, Dn=0 supports H0

%Emperical quantiles
Gammacrit01= quantile(DnGammaMax,0.99)
Gammacrit05= quantile(DnGammaMax,0.95)
Gammacrit10= quantile(DnGammaMax,0.9)

Gausscrit01= quantile(DnGaussMax,0.99)
Gausscrit05= quantile(DnGaussMax,0.95)
Gausscrit10= quantile(DnGaussMax,0.9)

figure
histogram(DnGammaMax,FaceColor=[0.4660 0.6740 0.1880])
hold on
xline(DnGammaobs,'k', LineWidth=2)
xline(Gammacrit01,'-.g',LineWidth=2)
xline(Gammacrit05,'-.b',LineWidth=2)
xline(Gammacrit10,'-.r',LineWidth=2)
legend('D_n Max Frequency','D_n Gamma Obs','1% Critial Value','5% Critical Value', '10% Critical Value')
title('Stochastic Simulations of D_n Max for Gamma Distribution',FontSize=12)
xlabel('D_n Max Values',FontSize=12)
ylabel('Frequency',FontSize=12)
grid on

figure
histogram(DnGaussMax,FaceColor=[0.8500 0.3250 0.0980])
hold on
xline(DnGaussObs,'k', LineWidth=2)
xline(Gausscrit01,'-.g',LineWidth=2)
xline(Gausscrit05,'-.b',LineWidth=2)
xline(Gausscrit10,'-.r',LineWidth=2)
legend('D_n Max Frequency','D_n Gauss Obs','1% Critial Value','5% Critical Value', '10% Critical Value')
title('Stochastic Simulations of D_n Max for Gaussian Distribution',FontSize=12)
xlabel('D_n Max Values',FontSize=12)
ylabel('Frequency',FontSize=12)
grid on

% Calpha
C_alpha_10= 1.224/(sqrt(length(PrecipJan))+0.12+(0.11/sqrt(length(PrecipJan))));
C_alpha_05= 1.358/(sqrt(length(PrecipJan))+0.12+(0.11/sqrt(length(PrecipJan))));
C_alpha_01= 1.628/(sqrt(length(PrecipJan))+0.12+(0.11/sqrt(length(PrecipJan))));
% from these values H0 is not rejected since Dnobs for gamma and gauss is
% less than Ca
%but on the 1000 simulations, there are some dn that reject the null



