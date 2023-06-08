# world-clock
An almost working Python GUI to display the time in multiple timezones. 

TODO: create proper python package, fix threading so clocks run consistently

world-clock uses it config.json to create all GUI elements. Time zones are derived from /usr/share/zoneinfo. For more details see the python documentation for time.tzset(). The country code field should be in lowercase to play nicely with flagcdn.com

