# WA Electricity Demand Forecast

## CURRENT STATUS
Still a work in progress, however the data is almost prepared a

## What I've done so far

### Data preparation

- I put the years into a "years" array, then has it loop through each "year" in the "years" array to read the csv file and append the csv values to an empty array called "frames", then used the concat function to stack the data vertically into one panda data frame called df. Then ensured to only include the columns: "Trading Interval" an "Operational Demand (MW)" as those are the ones useful in this scenario, and renamed them "time" and "demand_mw". Then I had to change the time value to a readable time value for panda as it appeared as a string initially, then sorted the "df" data frame by the time of the demand.

Then I retrieved the weather information for that time period from Open Meteo API, in which I told it to ignore the first 3 rows as it was information that was not relevant to this scenario, whilst reading the csv file into the data frame "weather". Then I changed the column names to "time" and "temp_c" and once again made the time readable by panda.

As the time values in "df" were taken every 30 minutes, whilst the time values in "weather" were every hour, I had to turn the "df" time values to be every hour before joining the two data frames, so I used resample to store them by the hour and giving the mean of the two 30 minute values as the demand, and stored that in the "demand_hourly" data frame.

Then I joined the two dataframes by using the inner parameter, so that if a time didnt exist in one of the data frames, it was just cut out.

Throughout I checked for duplicates and null values in the data, but there were none


# TEMPERATURE VS DEMAND GRAPH
To discover the features for the model I put temperature against demand to see if the temperature of the day affects the electricity demand. This produced a tick shape, where many things were revealed:

- The highest demand tends to come from the highest temperatures, assumingly due to air-conditioning, and the second highest demand comes from lower temperatures, assumingly due to heating, whereas the lowest demand comes from neutral temperatures. 

- Most days in Perth experience 15 - 25 degrees

# TIME OF DAY GRAPH

However there was another hypothesis, where the time of day affected the demand aswell, and after making each dot have a colour reflecting the time of day it was evident it did:

- The middle of the day had the lowest demand, due to solar energy being used
- The evenings had the highest, regardless of the temperature and that once again strengthens the solar argument

Thi confirms that the temperature and the time are both features in what causes demand of electricity

# WEEKEND VS WEEKDAY GRAPH

To see whether the weekend or weeday affected the demand, I created a graph, which showed a clear difference

- there seems to be the largest difference, meaning that the airconditioning and electricity use in workplaces and schools seems to be higher than at home
- The evening time is also higher on weekdays, assumingly because people are out more at evening at dinners or events on weekends.

# SAME AS YESTERDAY MODEL
I have built a same as yesterday and same as last week model to use as my baseline to improve from with my future trained models

The 'same as yesterday' score to beat is: 8.9%
The 'same as last week' score to beat is: 12.3%

## IDEAS TO TEST

- After looking at the demand vs temperature plot, there is a large vertical spread around 15 - 25 degrees, and my belief is that it could also be the type of day aswell, because you can have 20 degree days in almost all seasons, yet the humidity, windyness etc all affect how the temperature feels.