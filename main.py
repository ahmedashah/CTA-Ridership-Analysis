#CS 341 Project 1
#Name: Ahmed Shah
#Console based Python program using input commands to retrieve data from
#the SQL CTA2 L daily ridership database
import sqlite3
import matplotlib.pyplot as plt
from datetime import date #imported to format date in one of the commands


##################################################################  
#
# print_stats
#
# Given a connection to the CTA database, executes various
# SQL queries to retrieve and output basic stats.
#
# Displayed at the start of the program to show stats

def print_stats(dbConn):

    #Shows total number of stations
    print("General stats:")
    dbCursor = dbConn.cursor()
    dbCursor.execute("Select count(*) From Stations;") #retrieve station count from database
    statTotal = dbCursor.fetchone();
    print("  # of stations:", f"{statTotal[0]:,}") 
    dbCursor.close()

    #shows total no. of stops
    dbCursor = dbConn.cursor()
    dbCursor.execute("Select count(*) From Stops;") # fetches total count of stops from database
    numOfStops = dbCursor.fetchone();
    print("  # of stops:", f"{numOfStops[0]:,}")
    dbCursor.close()

    #shows total number of entries made
    dbCursor = dbConn.cursor()
    dbCursor.execute("Select count(*) From Ridership;") #fetches total count of entries
    entriesTotal = dbCursor.fetchone();
    print("  # of ride entries:", f"{entriesTotal[0]:,}")
    dbCursor.close()

  #shows the range for time
    dbCursorTime1 = dbConn.cursor()
    #Quary to get the first entry of time
    sqlTimeBegin  = """Select Strftime('%Y',Ride_Date) as "Year",
                      strftime('%m',Ride_Date) as "Month",
                      strftime('%d',Ride_Date) as "Day"
                      from Ridership 
                     ORDER BY Ride_Date asc
                     LIMIT 1"""
    dbCursorTime1.execute(sqlTimeBegin) #gets the beginning
    timeStart =  dbCursorTime1.fetchall()
    #Quary to get the last entry of time in the database
    sqlTimeEnd  = """Select Strftime('%Y',Ride_Date) as "Year",
                      strftime('%m',Ride_Date) as "Month",
                      strftime('%d',Ride_Date) as "Day"
                  from Ridership 
                  ORDER BY Ride_Date desc
                  LIMIT 1 """
    dbCursorTime2 = dbConn.cursor()
    dbCursorTime2.execute(sqlTimeEnd)
    timeEnd = dbCursorTime2.fetchall()
    #joins results of both quaries to print time range statement
    print(  f"  date range: {timeStart[0][0]}-{timeStart[0][1]}-{timeStart[0][2]} - {timeEnd[0][0]}-{timeEnd[0][1]}-{timeEnd[0][2]}")

    #prints the total number of riderships
    dbCursor = dbConn.cursor()
    dbCursor.execute("Select SUM(Num_Riders) From Ridership;")
    ridersRows = dbCursor.fetchone();
    print(f"  Total ridership:", f"{ridersRows[0]:,}")
    dbCursor.close()
    totalRiderships = float(ridersRows[0]) #saves for later calculations

    #prints the total number of weekday riderships and the percentage out of total
    dbCursor = dbConn.cursor()
    dbCursor.execute("Select SUM(Num_Riders) From Ridership WHERE Type_Of_Day = 'W';")
    weekdayRidersRows = dbCursor.fetchone();
    weekdayRiders = float(weekdayRidersRows[0])
    weekdayPercent = (weekdayRiders/totalRiderships)*100 #calculates percentage of weekday riderships
    print(f"  Weekday ridership:", f"{int(weekdayRiders):,} ({weekdayPercent:.2f}%)")
    dbCursor.close()

    #prints saturday riderships with percentage of saturday riderships
    dbCursor = dbConn.cursor()
    dbCursor.execute("Select SUM(Num_Riders) From Ridership WHERE Type_Of_Day = 'A';")
    saturdayRidersRows = dbCursor.fetchone();
    saturdayRiders = float(saturdayRidersRows[0])
    saturdayPercent = (saturdayRiders/totalRiderships)*100 #calulation for percentage of saturday riderships
    print(f"  Saturday ridership: ", f"{int(saturdayRiders):,} ({saturdayPercent:.2f}%)")
    dbCursor.close()

     #prints sunday/holiday riderships with percentage of sunday/holiday riderships
    dbCursor = dbConn.cursor()
    dbCursor.execute("Select SUM(Num_Riders) From Ridership WHERE Type_Of_Day = 'U';")
    sundayRidersRows = dbCursor.fetchone();
    sundayRiders = float(sundayRidersRows[0])
    sundayPercent = (sundayRiders/totalRiderships)*100 #calulation for percentage of sunday/holiday riderships
    print(f"  Sunday/holiday ridership:", f"{int(sundayRiders):,} ({sundayPercent:.2f}%)")
    dbCursor.close()
  
  ############################################################################
######RetrieveQuary
#####Read the SQL Quary passed and returns what was retrieved
def RetrieveQuary(sqlQuary,dbConn):
   dbCursor = dbConn.cursor() #retrieve a cursor to work with the database
   dbCursor.execute(sqlQuary) #inputs the quary
   rows = dbCursor.fetchall() #retrieves the output of the quary
   dbCursor.close() #done its purpose
   return rows 
############################################################################
######RetrieveQuaryWParameters
#####Read the SQL Quary passed and certain parameters to search quary from, 
##and returns what was retrieved
def RetrieveQuaryWParameters(sqlQuary,parameter,dbConn):
   dbCursor = dbConn.cursor() #retrieve a cursor to work with the database
   dbCursor.execute(sqlQuary, [parameter]) #inputs the quary
   #if (dbCursor)
   rows = dbCursor.fetchall() #retrieves the output of the quary
   dbCursor.close() #done its purpose
   return rows 

#############################################################################
#######RetrieveQuaryWTwoParameters
#####Read the SQL Quary passed and 2 certain parameters to search quary from, 
##and returns what was retrieved
def RetrieveQuaryWTwoParameters(sqlQuary,parameter1,parameter2,dbConn):
   dbCursor = dbConn.cursor() #retrieve a cursor to work with the database
   dbCursor.execute(sqlQuary, (parameter1,parameter2)) #inputs the quary
   rows = dbCursor.fetchall() #retrieves the output of the quary
   dbCursor.close() #done its purpose
   return rows 

  
############################################################################
######PrintsResultsWTwoColumns
####Prints whatever was recieved from the SQL Quary  
def PrintsResultsWTwoColumns(rows):
  for row in rows:
    if(type((row[1]) == 'int' )): #checks if we are dealing with numbers
      print(row[0],":", f"{row[1]:,d}") #prints the quary
    else: #if we are dealing with letters
      print(row[0], ":", row[1]) #prints the quary


def PrintsResultsWTwoColumns2(rows):
  for row in rows:
     #if we are dealing with letters
      print(row[0], ":", row[1]) #prints the quary

      
############################################################################
######PrintsResultsWPercent
####Prints whatever was recieved from the SQL Quary and the percentage of each row 
def PrintsResultsWPercent(rows, sum):
  for row in rows:
      #dataVal = float(row[1]) 
      percent = float(row[1]/sum) *100 #finds the percentage each station makes of all the rides
      print(row[0], ":", f"{row[1]:,}", f"({percent:.2f}%)") #prints name, id and percentage
    
#############################################################################
########SumACol
########Calulates the total of a purticular column indexed
def SumACol(rows,colNum):
 sumVar = 0 
 for row in rows: #calculates the total number of rides from all stations
     sumVar +=  row[colNum] #adds each number in the col
 return sumVar

############################################################################
#######ConstructAndPrintStringCommandFive  
#######outputs all the stops, direction of the train leaving, and if they are handicap accessible
def ConstructAndPrintStringCommandFive(rows):
  for row in rows :
          #constructs string to output for each stop with all information
          if(row[2] ==1):
           adaString = "(accessible? yes)"
          else: 
            adaString = "(accessible? no)"
       #all information for a stop printed
          print(row[0], ": direction =", row[1],adaString)
######################################################################
#######PlotGraph: General Graphing function 
def PlotGraph(x,y,xAxis,yAxis,graphTitle,plt):
    # setting the labels and titles for the plot
      plt.xlabel(xAxis) #labeling the x axis
      plt.ylabel(yAxis)
      plt.title(graphTitle) 
      plt.plot(x,y) #setting the x and y axis to the two arrays 
      plt.plot()
      plt.show()
######################################################################
#######PlotTwoGraphs: Plots 2 graphs side by side 
def PlotTwoGraphs(x1,y1,label1, x2,y2,label2,xAxis,yAxis,legendLoc,graphTitle,plt):
    # setting the labels and titles for the plot
      plt.xlabel(xAxis)
      plt.ylabel(yAxis)
      plt.title(graphTitle)
      plt.plot(x1,y1,label= label1)
      plt.plot(x2,y2, label = label2)
      plt.legend(loc=legendLoc)
      plt.show()  
    
     
    
##################################################################  
#
# main
#
print('** Welcome to CTA L analysis app **')
print()
#taking data from the ridership database
dbConn = sqlite3.connect('CTA2_L_daily_ridership.db') 
print_stats(dbConn)#function call for the opening display

loopRun = True # the condition to run our command menu 
while loopRun == True:
  #Prompt user input to pick a command
  print("\nAll commands:")
  print("1. Retrieve Station ID and Station Name")
  print("2. Retrieve all stations, no. of rides and percentage")
  print("3. top10 busiest stations, no. of riders and percentage")
  print("4. top10 least busiest stations, no. of riders and percentage")
  print("5. Search CTA Line and outputs all stops, train direction and handicap accessibility")
  print("6. Outputs all the ridership in a month")
  print("7. Outputs all the ridership in a year")
  print("8. Compares daily riderships of two stations.")
  print("9. Outputs stations that are under a line.")
  command = input("\nPlease enter a command (1-9, x to exit): ") 
  
###########################################################################
##########Command X Exit the Loop
  
  if command ==  'x': #ends the program
    loopRun = False #condition to run the loop is no more
    
###########################################################################
##########Command 1: Retreives Station ID and Name. Part or all of the name is entered and command outputs the name and ID from the database
    
  elif command == "1":
    #prompts user input to get the right station name and id
    stationName = input("\nEnter partial station name (wildcards _ and %): ") 
    #stationName = stationName.lower()
    
    #SQL Quary that takes the input and tries to find the full Station name and its ID. Alphabetical order
    rows = RetrieveQuaryWParameters(""" SELECT Station_ID, Station_Name
              FROM Stations 
              WHERE Station_Name LIKE ? 
              ORDER BY Station_Name
    """, stationName ,dbConn)
    
    if len(rows) ==0 : # if the entered station does not exist. exits out of command 1
       print("**No stations found...")

    else:  #if stations are found
      PrintsResultsWTwoColumns2(rows) #input their names and Ids one by one
      continue  
        
###########################################################################
#############Command 2:Outputs all the stations, total no. of rides from there and the percentage of all riderships they make up
        
  elif command == '2':
    print("** ridership all stations **")
    #SQL quary to retrieve all the stations and the total number of rides on them. Stations ordered in ascending order
    rows = RetrieveQuary("""  
                SELECT Station_Name, SUM(Num_Riders)
                FROM Stations
                JOIN Ridership ON Stations.Station_ID = Ridership.Station_ID
                GROUP BY Stations.Station_Name
                ORDER BY Stations.Station_Name asc                
          """,dbConn)

    sumRiders = SumACol(rows,1) #calculates the total number of rides from all stations
    sumRiders = float(sumRiders) 
    PrintsResultsWPercent(rows, sumRiders) # prints out the quary with the name, id, Percentage
    
###########################################################################
########Command 3: Outputs the top10 busiest stations, their no. of riders and percentage
      
  elif command == '3': 
    print("** top-10 stations **")
    #SQL quary to retrieve the stations ordered by the most busiest to least 
    rows = RetrieveQuary("""  SELECT Station_Name, SUM(Num_Riders)
                FROM Stations
                JOIN Ridership ON Stations.Station_ID = Ridership.Station_ID
                GROUP BY Stations.Station_Name            
                ORDER BY SUM(Ridership.Num_Riders) desc 
           """,dbConn)
    sumRiders = SumACol(rows,1) #calculates the total number of rides from all stations
    sumRiders = float(sumRiders) 
    busy10 = rows[0:10:1] #takes only the top 10 busiest
    PrintsResultsWPercent(busy10,sumRiders)  #prints only the 10 busiest with their percentages
    
#################################################################################Command 4: Outputs the least busiest stations, their no. of riders and percentage     
  elif command == '4': 
    print("** least-10 stations **")
    #SQL quary to retrieve all stations starting from least busiest to most
    rows = RetrieveQuary("""  SELECT Station_Name, SUM(Num_Riders)
                FROM Stations
                JOIN Ridership ON Stations.Station_ID = Ridership.Station_ID
                GROUP BY Stations.Station_Name            
                ORDER BY SUM(Ridership.Num_Riders) asc 
           """, dbConn)
    
    sumRiders = SumACol(rows,1) #calculates the total number of rides from all stations
    sumRiders = float(sumRiders)
    leastBusy10 = rows[0:10:1] #takes only the top 10 busiest
    PrintsResultsWPercent(leastBusy10,sumRiders)  #prints only the 10 busiest with their percentages
   #################################################################################command 5: Searches by CTA Line and outputs all the stops,
####direction of the train leaving, and if they are handicap accessible
      
  elif command == '5':
    #prompt to input CTA line
    color = input("\nEnter a line color (e.g. Red or Yellow): ")
    color = color.lower() #so that input is case-insensitive
    
    #if statement ahead to check if a valid line is entered
    if(color == "red" or color == "yellow" or color == "brown" or color == "orange" or color == "green" or color == "blue" or color == "purple" or color == "purple-express" or color == "pink"): 
      #SQL quary to retrieve all the stops for the line, train direction, if they are handicap accessible or not
      rows = RetrieveQuaryWParameters("""  
              SELECT Stop_Name, Direction, ADA FROM Stops  
              JOIN StopDetails ON Stops.Stop_ID = StopDetails.Stop_ID
              JOIN Lines ON StopDetails.Line_ID = Lines.Line_ID 
              WHERE Lines.Color LIKE ?  
              ORDER BY Stop_Name asc
           """,color,dbConn)
      #constructs string to output for each stop with all information
      ConstructAndPrintStringCommandFive(rows)
    else: #if invalid line color entered
      print("**No such line...")

###########################################################################
####### Command 6: Outputs all the ridership in a month by ascending order
## graph can also be plotted to show the trend
      
  elif command == '6':
    print("** ridership by month **")
    #SQL quary retrieve all the months and their total rides
    #Output is in ascending order
    rows = RetrieveQuary("""  
                SELECT strftime('%m', Ride_Date) As Month, SUM(Num_Riders)
                FROM Ridership 
                WHERE Month BETWEEN '01'AND '12'
                GROUP BY Month
                ORDER BY Month asc
           """, dbConn)
    
   # for row in rows:#prints all the months and their no. of rides   
    PrintsResultsWTwoColumns(rows)
      
    wannaPlot = input("\nPlot? (y/n) ") 
    #user is prompted whether they want to plot or not
    if(wannaPlot == 'y'): #they want to plot
      x = [] #x axis storing the months 
      y = [] #y axis storing the number of rides
      for row in rows:
        x.append(row[0]) # takes in each month value by each iteration
        y.append(row[1]) # takes in each monthly rides by each iteration
        
      #Plots the graph with approriate x and y axis, along with labels and a title for monthly ridership
      PlotGraph(x,y,"month","number of riders (x * 10^8)","monthly ridership",plt)
    
###########################################################################
####### Command 7: Outputs ridership by yearly
### user can also plot to see the trend
  elif command == '7':
    print("** ridership by year **")
    #sql quary to retrieve year and no. of riders
    rows = RetrieveQuary("""  
                SELECT strftime('%Y', Ride_Date) As Year, SUM(Num_Riders)
                FROM Ridership 
                WHERE Year BETWEEN '2001'AND '2021'
                GROUP BY Year
                ORDER BY Year asc
           """,dbConn)
    #outputs the rows
    PrintsResultsWTwoColumns(rows)
      
    wannaPlot = input("\nPlot? (y/n) ") #prompts user to plot or not 
    if(wannaPlot == 'y'): #they want to plot
      x = [] #x axis storing the year 
      y = [] #y axis storing the number of rides
      for row in rows:
        #print("check")
        x.append(row[0][2:4]) # takes in each year (last 2 digits) value by each iteration
        y.append(row[1]) # takes in each yearly rides by each iteration
         #Plots the graph with approriate x and y axis, along with labels and a title for yearly ridership
      PlotGraph(x,y,"year","number of riders (x * 10^8)","yearly ridership",plt)
      continue
    
#######################################################################
###########################Command 8: Takes two different stations and compares their daily riderships. Can also show comparison with a plot 
####### 
  elif command == '8':
    #prompts user what year to compare
    yearCompare = input("\nYear to compare against? ")
    #prompts user to choose which station to choose for station1
    station1 = input("\nEnter station 1 (wildcards _ and %): ")
    #Quary to get the station with the name and ID
    rowstat1 = RetrieveQuaryWParameters(""" SELECT Station_ID, Station_Name
              FROM Stations 
              WHERE Station_Name LIKE ? 
              GROUP BY Station_Name
              ORDER BY Station_Name
    """, station1,dbConn)
    
    if len(rowstat1) == 0: #invalid station. no comparision happens
      print("**No station found...")
      continue
    elif len(rowstat1) > 1 : #too many stations. no comparision happens
      print("**Multiple stations found...")
      continue
      #prompts user for station 2
    station2 = input("\nEnter station 2 (wildcards _ and %): ")
    rowstat2 =  RetrieveQuaryWParameters(""" SELECT Station_ID, Station_Name
              FROM Stations 
              WHERE Station_Name LIKE ? 
              GROUP BY Station_Name
              ORDER BY Station_Name
    """, station2,dbConn)
    
    if len(rowstat2) == 0: #invalid station2. no comparision happens
      print("**No station found...")
      continue
    elif len(rowstat2) > 1 : #too many station2s. no comparision happens
      print("**Multiple stations found...")
      continue
          
    #list with all riderships for station 1  
    allDaysStation1 = RetrieveQuaryWTwoParameters(""" SELECT date(Ride_Date), SUM(Num_Riders)
              FROM Stations
              INNER JOIN Ridership ON Ridership.Station_ID = stations.Station_ID
              WHERE Stations.Station_Name LIKE ? 
              AND strftime('%Y',Ride_Date) LIKE ?
              GROUP BY date(Ride_Date)
              ORDER BY date(Ride_Date) asc
    """,station1, yearCompare,dbConn)
    
    #list with all riderships for station 1
    allDaysStation2 = RetrieveQuaryWTwoParameters(""" SELECT date(Ride_Date), SUM(Num_Riders)
              FROM Stations
              INNER JOIN Ridership ON Ridership.Station_ID = stations.Station_ID
              WHERE Stations.Station_Name LIKE ? 
              AND strftime('%Y',Ride_Date) LIKE ?
              GROUP BY date(Ride_Date)
              ORDER BY date(Ride_Date) asc
    """, station2, yearCompare, dbConn)
    
    #first 5 days for station 1
    dateAndRideStat1 = RetrieveQuaryWTwoParameters(""" SELECT date(Ride_Date), SUM(Num_Riders)
              FROM Stations
              INNER JOIN Ridership ON Ridership.Station_ID = stations.Station_ID
              WHERE Stations.Station_Name LIKE ? 
              AND strftime('%Y',Ride_Date) LIKE ?
              GROUP BY date(Ride_Date)
              ORDER BY date(Ride_Date) asc
              LIMIT 5
    """, station1,yearCompare, dbConn)
    
    #first 5 days for station 2
    dateAndRideStat2 = RetrieveQuaryWTwoParameters(""" SELECT date(Ride_Date), SUM(Num_Riders)
              FROM Stations
              INNER JOIN Ridership ON Ridership.Station_ID = stations.Station_ID
              WHERE Stations.Station_Name LIKE ? 
              AND strftime('%Y',Ride_Date) LIKE ?
              GROUP BY date(Ride_Date)
              ORDER BY date(Ride_Date) asc
              LIMIT 5
    """,station2,yearCompare,dbConn)

    #last 5 days for station 1
    dateAndRideStatLast1 = RetrieveQuaryWTwoParameters(""" SELECT date(Ride_Date), SUM(Num_Riders)
              FROM Stations
              INNER JOIN Ridership ON Ridership.Station_ID = stations.Station_ID
              WHERE Stations.Station_Name LIKE ? 
              AND strftime('%Y',Ride_Date) LIKE ?
              GROUP BY date(Ride_Date)
              ORDER BY date(Ride_Date) desc
              LIMIT 5
    """, station1,yearCompare,dbConn)
    dateAndRideStatLast1.reverse() #setting them in order
   
    #last 5 days for station 2
    dateAndRideStatLast2 = RetrieveQuaryWTwoParameters(""" SELECT date(Ride_Date), SUM(Num_Riders)
              FROM Stations
              INNER JOIN Ridership ON Ridership.Station_ID = stations.Station_ID
              WHERE Stations.Station_Name LIKE ? 
              AND strftime('%Y',Ride_Date) LIKE ?
              GROUP BY date(Ride_Date)
              ORDER BY date(Ride_Date) desc
              LIMIT 5
    """,station2,yearCompare,dbConn)
    dateAndRideStatLast2.reverse() #settiing them in order

    stationOneList = [] #adding the first and last 5 days for output in an array for Station1
    for row in dateAndRideStat1:
      stationOneList.append(row) 
    for row in dateAndRideStatLast1:
      stationOneList.append(row) 

    stationTwoList = []#adding the first and last 5 days for output in an array for Station2
    for row in dateAndRideStat2:
      stationTwoList.append(row)
    for row in dateAndRideStatLast2:
      stationTwoList.append(row)
    
    #print daily ridership for station1
    print("Station 1:", rowstat1[0][0], rowstat1[0][1])
    for row in stationOneList:
      print(row[0], row[1])
    #print daily ridership for station2  
    print("Station 2:", rowstat2[0][0], rowstat2[0][1])
    for row in stationTwoList:
      print(row[0], row[1])

    #asks user to plot or not
    wannaPlot = input("\nPlot? (y/n) ")
    wannaPlot = wannaPlot.lower() #case insensitive
    if wannaPlot == "y":    
      x1 = [] #day numbers for station1
      y1 = [] #daily ridership for station1

      for row in allDaysStation1: 
        dateVar1 = date( int(row[0][0:4]), int(row[0][5:7]) , int(row[0][8:10]) ) #gets date in a proper format
        dayNum = int(dateVar1.strftime('%j')) #day number out of 365
        x1.append(dayNum)
        y1.append(row[1])
      x2 = [] #day numbers for station1
      y2 = [] #daily ridership for station1
      for row in allDaysStation2:
         dateVar2 = date( int(row[0][0:4]), int(row[0][5:7]) , int(row[0][8:10]) ) #gets date in a proper format
         dayNum = int(dateVar2.strftime('%j')) #day number out of 365
         x2.append(dayNum)
         y2.append(row[1])
        #Plot both graphs side by side
      titlePrint = "riders each day of " + yearCompare 
      PlotTwoGraphs(x1,y1,rowstat1[0][1], x2,y2,rowstat2[0][1], "day", "number of riders", 'upper right' ,titlePrint, plt)
    
     
#####################################################################Command 9: Outputs stations that are under a line    
#######  User can also plot stations on a map for a line

  elif command == '9':
    lineColor = input("\nEnter a line color (e.g. Red or Yellow): ")
    lineColor = lineColor.lower()
    if(lineColor == "red" or lineColor == "yellow" or lineColor == "brown" or lineColor == "orange" or lineColor == "green" or lineColor == "blue" or lineColor == "purple" or lineColor == "purple-express" or lineColor == "pink"): 
      #retrieves data for a line
      rows = RetrieveQuaryWParameters("""  
              SELECT DISTINCT Station_Name, Longitude, Latitude FROM Stops 
              JOIN Stations ON Stations.Station_ID = Stops.Station_ID
              JOIN StopDetails ON Stops.Stop_ID = StopDetails.Stop_ID
              JOIN Lines ON StopDetails.Line_ID = Lines.Line_ID 
              WHERE Lines.Color LIKE ?  
              ORDER BY Station_Name
           """,lineColor,dbConn)
      x = [] # longitude 
      y = [] # latitude 
      for row in rows :     
          statName = row[0] #saves the station name
          long = row[1] #to print longitude later
          lat =  row[2] #to print latitude later
          x.append(float(row[1])) #stores the longitude 
          y.append(float(row[2])) #stores the latitude
          print(f"{statName} : ({lat}, {long})") #prints station with its longitude and latitude

      wannaPlot = input("\nPlot? (y/n) ") #prompts user if they want to plot on the map
      wannaPlot = wannaPlot.lower() #case insensituve
      if wannaPlot == 'y':
        image = plt.imread("chicago.png") #opens the map image
        xydims = [-87.9277, -87.5569, 41.7012, 42.0868] # area covered by the map:
        plt.imshow(image, extent=xydims) #displays map
        plt.title(lineColor + " line")
        if(lineColor == "purple-express"):
          lineColor = "purple"
        # color is the value input by user, we can use that to plot the
# figure *except* we need to map Purple-Express to Purple:  
       
        plt.plot(x,y, "o" , c = lineColor)  
        
        for row in rows:
          statName = row[0]
          plt.annotate(statName,(row[1],row[2])) #plots labels
        plt.xlim([-87.9277, -87.5569])
        plt.ylim([41.7012, 42.0868])
        plt.show() 
        
    else: 
      print("**No such line...")
  
  else: #Error message 
    print("**Error, unknown command, try again...\n")

#
# done
#
dbConn.close()