#!/usr/bin/env python
# coding: utf-8


import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    
    # get user input for city (chicago, new york city, washington)
    while True:
        try:
            city = str(input('\nWould you like to see data for Chicago, New York City, or Washington? Please, enter the name of the city.')).lower()
      
            # offer a choise to break the game
            if (city == 'chicago' or city == 'new york city' or city == 'washington'):
                print('\nLooks like you want to hear about {}! \nIf your are interested in another city, restart the program.'.format(city.title()))        
                break
            else: 
                    raise ValueError
        except ValueError:
            print('\nEnter a valid city name.')
        
    # get user input about filtering the database by month, day or no filter
    while True:
        try: 
            filt = str(input('\nWould you like to filter the data by month, day, or not at all? Type "none" for no time filter.')).lower()
            
            if filt == "month":
                day = 0
                print('\nYou betcha! We will make sure to filter by {}!'.format(filt))
                months = ['january', 'february', 'march', 'april', 'may', 'june']
                # get user input for month (january, february, ... , june)
                while True:
                    try: 
                        month = str(input('\nWhich month - January, February, March, April, May, June?')).lower()
                        
                        if month in months:
                            month = months.index(month)+1
                            
                            break
                     
                        else:
                            raise ValueError
                    except ValueError:
                        print("\nPlease enter valid month name or type in all.")   
                break
                
            elif filt == "day":
                month = 0
                print('\nYou betcha! We will make sure to filter by {}!'.format(filt))
                # get user input for day of week (monday, tuesday, ... sunday)
                while True:
                    try: 
                        day = str(input('\nWhich day - Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, or Sunday?')).lower()

                        if day in [ "monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]:
                            break
                        else:
                            raise ValueError
                    except ValueError:
                        print("\nPlease enter valid day name!")
                break
                
            elif filt == "none":
                month = 0
                day = 0
                print('\nYou betcha! We won\'t filter the data!')
                break
                
            else:
                raise ValueError
        # get user input for ValueError
        except ValueError:
            print("\nPlease enter one of the three options")      

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
    df['Start Time DT'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time DT'].dt.month
    df['day_of_week'] = df['Start Time DT'].dt.day_name()
    df['hour'] = df['Start Time DT'].dt.hour
    df['start_end_station'] = df['Start Station'] + ' ' + df['End Station']

    # filter by 'none'
    if (month == 0) & (day == 0):
        return df
        
    # filter by month if applicable
    elif (day == 0):
        
        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    else:
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df

def time_stats(df,month,day):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    
    if (month == 0) & (day == 0):
    
        # display the most common month
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        popular_month = df['month'].mode()[0]
        print('Most Frequent Month:', (months[popular_month-1]).title())

        # display the most common day of week
        popular_day = df['day_of_week'].value_counts().index[0]
        print('Most Frequent Day:', popular_day)
        
    elif month != 0:
        
        # display the most common day of week
        popular_day = df['day_of_week'].value_counts().index[0]
        print('Most Frequent Day:', popular_day)
    
    elif day != 0:
        
        # display the most common month
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        popular_month = df['month'].mode()[0]
        print('Most Frequent Month:', (months[popular_month-1]).title())

    # display the most common start hour
    popular_hour = df['hour'].mode()[0]
    count_popular_hour = df['hour'].count()
    print('Most Frequent Hour:', popular_hour)
    print('Count:', count_popular_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_start = df['Start Station'].value_counts().index[0]
    print('Most commonly used start station:', popular_start)

    # display most commonly used end station
    popular_end = df['End Station'].value_counts().index[0]
    print('Most commonly used end station:', popular_end)

    # display most frequent combination of start station and end station trip
    popular_start_end = df['start_end_station'].value_counts().index[0]
    count_popular_start_end = df['start_end_station'].count()
    print('Most popular combination of start station and end station trip:', popular_start_end)
    print('Count:', count_popular_start_end)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()
    count_total_travel_time = df['Trip Duration'].count()
    print('Total travel time:', total_travel_time)

    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print('Average duration of trips:', mean_travel_time)
    print('Count:', count_total_travel_time)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df,city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    if city == 'chicago' or city == 'new york city':
        # Display counts of user types
        total_user_types = df['User Type'].count()
        print('Total number of users:', total_user_types)
        
        # Display counts of each user types
        number_user_types = df['User Type'].value_counts()
        print('\nWhat is the breakdown of users?')
        print(number_user_types)
    
        # Display counts of gender
        counts_gender = df['Gender'].value_counts()
        print('\nWhat is the breakdown of genders?')
        print(counts_gender)
         
        # Display earliest, most recent, and most common year of birth
        earliest_birth = df['Birth Year'].min()
        latest_birth = df['Birth Year'].max()
        most_common_birth = df['Birth Year'].value_counts().index[0]
        print('\nThe oldest rider\'s year of birth:', earliest_birth)
        print('The youngest rider\'s year of birth:', latest_birth)
        print('Most common year of birth:', most_common_birth)
             
    elif city == 'washington':
         # Display counts of user types
        total_user_types = df['User Type'].count()
        print('Total number of users:', total_user_types)
        # Display counts of each user types
        number_user_types = df['User Type'].value_counts()
        print(number_user_types)
        print('\nNo gender data to share.')
        print('\nNo birth year data to share.')
    
   
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df,month,day)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df,city)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()




