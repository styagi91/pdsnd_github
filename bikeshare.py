# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a script to analyze the bikeshare data.
Script will prompt you to enter the city, month and day to analyze the data.

"""
import time
import pandas as pd
import numpy as np


#CITY_DATA = { 'chicago': 'C://Users//styagi//Documents//2019_projects//Training//DataScience//python//bikeshare-2//chicago.csv',
#              'new york city': 'C://Users//styagi//Documents//2019_projects//Training//DataScience//python//bikeshare-2//new_york_city.csv',
#             'washington': 'C://Users//styagi//Documents//2019_projects//Training//DataScience//python//bikeshare-2//washington.csv' }

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

months = ['all','january','february','march','april','may','june']
days = ['all','monday','tuesday','wednessday','thursday','friday','saturday','sunday']
          
def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city  = ""
    month = ""
    day   = ""
    while city not in CITY_DATA:
        city = input("Enter any of these city name (chicago, new york city, washington) \n").lower()
    
    # get user input for month (all, january, february, ... , june)
    while month not in months:
        month = input("Enter the name of the month (all, january, february, march, april, may, june) to filter by, or 'all' to apply no month filter  \n").lower()
        
    # get user input for day of week (all, monday, tuesday, ... sunday)
    while day not in days:
        day = input("Enter the day of week (all, monday, tuesday, ... sunday) to filter by, or 'all' to apply no day filter \n").lower()

    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        #months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) 

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract hour from the Start Time column to create an hour column
    df['hour'] = df['Start Time'].dt.hour
    df['month'] = df['Start Time'].dt.month
    df['dayofweek'] = df['day_of_week']
    # find the most popular month
    popular_month = df['month'].mode()[0]
    print('Most Popular Start Month: <{} - {}>'.format(popular_month,months[popular_month]))
    # find the most popular hour
    popular_hour = df['hour'].mode()[0]
    print('Most Popular Start Hour:', popular_hour)
    
    # display the most common day of week
    popular_day = df['day_of_week'].mode()[0]
    print('Most Popular day:', popular_day)
 
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_start_station = df['Start Station'].mode()[0]
    popular_end_station = df['End Station'].mode()[0]

    print("Most popular start station : ",popular_start_station)

    # display most commonly used end station
    print("Most popular End station : ",popular_end_station,"\n")
    # display most frequent combination of start station and end station trip
    popular_route = df.groupby(['Start Station','End Station'])['End Station'].count().nlargest(1)
    print("Most popular route  : ",popular_route)
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time

    print("Total travel time in secs :",df['Trip Duration'].sum())
    # display mean travel time
    print("Mean travel time in secs :",df['Trip Duration'].mean())

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    # print value counts for each user type
    user_types = df['User Type'].value_counts()
    print(user_types,"\n")

    # Display counts of gender
    if 'Gender' in df.columns:
        gender_type = df['Gender'].value_counts()
        print(gender_type,"\n")
    else:
        print("No Gender information in this data \n")

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        earliest_birth_year = df['Birth Year'].min()
        recent_birth_year = df['Birth Year'].max()
        most_common_birth_year = df['Birth Year'].mode()[0]
        print("Earliest year : % 4d Recent Year : % 4d Most common Birth year : % 4d " % (earliest_birth_year,recent_birth_year,most_common_birth_year))
    else:
        print("No Birth data available")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_data(df):
    """Displays row bikeshare data interactively. """
    current_index=0;
    print(len(df.index))
    display_data = input('\nWould you like to display raw data ? Enter yes or no.\n') 
    if display_data.lower() == 'yes':
        while True:
            end_index = current_index+5
            if end_index > len(df.index):
                end_index = len(df.index)
                print("Reached end of data ",df.iloc[current_index:end_index])
                break
            print(df.iloc[current_index:end_index])
            current_index +=5
            display_more = input('\nWould you like to display more raw data ? Enter yes or no.\n') 
            if display_more.lower() != 'yes':
                break
        

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day )
        print("Analyzing the data for city {} for month : {}  days : {}  ".format(city,month,day))

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_data(df)
        
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()

